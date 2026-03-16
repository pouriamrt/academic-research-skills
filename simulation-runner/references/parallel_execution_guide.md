# Parallel Execution Guide — joblib, multiprocessing, and When to Parallelize

## Purpose

A practical reference for parallelizing simulation workloads. Covers `joblib.Parallel` with `delayed` (the primary tool for simulation-runner), `multiprocessing.Pool` as a fallback, decision criteria for when parallelization helps vs. hurts, and overhead estimation.

---

## Primary Tool: joblib

### Why joblib?

`joblib` is the recommended parallelization library for simulation-runner because:
1. Simple API that wraps common patterns cleanly
2. Automatic memory mapping for large numpy arrays (reduces serialization cost)
3. Process-based backend by default (avoids Python's GIL)
4. Built-in progress support when combined with `tqdm`
5. Graceful fallback to sequential execution when `n_jobs=1`

### Basic Pattern

```python
from joblib import Parallel, delayed

def single_iteration(rng, params):
    """One iteration of the simulation. Pure function."""
    data = dgp(rng, params)
    result = analyze(data, params)
    return result

# Create independent RNGs (see seed_management_guide.md)
from numpy.random import SeedSequence, default_rng
ss = SeedSequence(42)
rngs = [default_rng(s) for s in ss.spawn(n_iterations)]

# Parallel execution
results = Parallel(n_jobs=-1, prefer="processes")(
    delayed(single_iteration)(rngs[i], params)
    for i in range(n_iterations)
)
```

### Key Parameters

| Parameter | Default | Recommendation | Description |
|-----------|---------|----------------|-------------|
| `n_jobs` | 1 | -1 (all cores) | Number of parallel workers; -1 = all available cores |
| `prefer` | — | "processes" | Backend: "processes" (no GIL) or "threads" (shared memory) |
| `backend` | "loky" | Keep default | "loky" (default, robust), "multiprocessing", or "threading" |
| `batch_size` | "auto" | "auto" or explicit | Number of tasks per dispatch; "auto" adapts |
| `verbose` | 0 | 0 or 10 | Verbosity level; 10 prints per-task progress |
| `pre_dispatch` | "2*n_jobs" | Keep default | Controls memory usage by limiting queued tasks |
| `max_nbytes` | "1M" | Increase for large arrays | Threshold for memory mapping (larger = more shared memory) |

### Backend Selection

```python
# For CPU-bound simulation work (most simulations)
Parallel(n_jobs=-1, prefer="processes")

# For I/O-bound work (rare in simulations)
Parallel(n_jobs=-1, prefer="threads")

# Force a specific backend
from joblib import parallel_backend
with parallel_backend("loky", n_jobs=-1):
    results = Parallel()(delayed(func)(x) for x in inputs)
```

### Batch Execution for Convergence Monitoring

The simulation-runner executes in batches to enable convergence checking between batches:

```python
from joblib import Parallel, delayed
from tqdm import tqdm

def run_batched_parallel(
    single_iteration_func,
    rngs,
    params,
    n_iterations,
    check_interval=500,
    n_jobs=-1,
    convergence_threshold=0.01,
):
    """
    Run simulation in parallel batches with convergence monitoring.

    Instead of dispatching all iterations at once, dispatch in batches of
    check_interval size. Between batches, check convergence and potentially
    stop early.
    """
    all_results = []
    convergence_history = []

    pbar = tqdm(total=n_iterations, desc="Simulation", unit="iter")

    for batch_start in range(0, n_iterations, check_interval):
        batch_end = min(batch_start + check_interval, n_iterations)
        batch_indices = list(range(batch_start, batch_end))

        # Dispatch this batch in parallel
        batch_results = Parallel(n_jobs=n_jobs, prefer="processes")(
            delayed(single_iteration_func)(rngs[i], params)
            for i in batch_indices
        )

        all_results.extend(batch_results)
        pbar.update(len(batch_results))

        # Check convergence
        mcse = compute_running_mcse(all_results)
        convergence_history.append({
            'iteration': batch_end,
            'mcse': mcse,
        })

        # Early stopping
        if all(v < convergence_threshold for v in mcse.values()):
            pbar.set_description("Converged!")
            break

    pbar.close()

    return {
        'results': all_results,
        'convergence_history': convergence_history,
        'converged': len(all_results) < n_iterations,
    }
```

### Memory Management with joblib

```python
# For large data objects, use memory mapping
from joblib import Parallel, delayed
import numpy as np
import tempfile
import os

# Option 1: Let joblib auto-mmap large arrays
# By default, arrays > 1MB are memory-mapped
results = Parallel(n_jobs=-1, max_nbytes="1M")(
    delayed(func)(large_array, i) for i in range(n)
)

# Option 2: Explicit shared memory via tempfile
temp_dir = tempfile.mkdtemp()
shared_data_path = os.path.join(temp_dir, "shared_data.npy")
np.save(shared_data_path, large_array)

def iteration_with_mmap(i, data_path, params):
    data = np.load(data_path, mmap_mode='r')
    # ... use data read-only ...
    return result

results = Parallel(n_jobs=-1)(
    delayed(iteration_with_mmap)(i, shared_data_path, params)
    for i in range(n)
)
```

---

## Alternative: multiprocessing.Pool

Use `multiprocessing.Pool` when joblib is unavailable or when you need lower-level control.

### Basic Pattern

```python
from multiprocessing import Pool
from functools import partial

def single_iteration(args):
    """Wrapper that unpacks a single argument tuple."""
    i, master_seed, params = args
    ss = SeedSequence(master_seed)
    rng = default_rng(ss.spawn(n_total)[i])  # Reconstruct specific RNG
    data = dgp(rng, params)
    return analyze(data, params)

# Create argument list
args_list = [(i, 42, params) for i in range(n_iterations)]

# Run in parallel
with Pool() as pool:
    results = pool.map(single_iteration, args_list)
```

### Comparison: joblib vs multiprocessing

| Feature | joblib | multiprocessing.Pool |
|---------|--------|---------------------|
| API simplicity | Very simple (Parallel + delayed) | Moderate (Pool + map/starmap) |
| Memory mapping | Automatic for large arrays | Manual |
| Serialization | Uses cloudpickle (more flexible) | Uses pickle (stricter) |
| Progress tracking | Combine with tqdm | Combine with tqdm via imap |
| Error handling | Clear error messages | Can be cryptic |
| Lambda/closure support | Yes (via cloudpickle) | No (pickle limitation) |
| Windows compatibility | Good (loky backend) | Requires `if __name__ == '__main__'` guard |
| Recommended for | simulation-runner default | Fallback when joblib fails |

### multiprocessing with tqdm

```python
from multiprocessing import Pool
from tqdm import tqdm

with Pool() as pool:
    results = list(tqdm(
        pool.imap(single_iteration, args_list),
        total=len(args_list),
        desc="Simulation",
    ))
```

---

## When Parallelization Helps vs. Hurts

### Decision Matrix

| Condition | Parallelize? | Rationale |
|-----------|-------------|-----------|
| n_iterations > 1,000 AND iteration_time > 10ms | **Yes** | Startup overhead (~100ms/worker) amortized across many iterations |
| n_iterations > 100 AND iteration_time > 100ms | **Yes** | Moderate iterations but expensive; parallelism helps significantly |
| n_iterations < 100 AND iteration_time < 100ms | **No** | Total work < 10s; parallelism overhead dominates |
| n_iterations > 10,000 AND iteration_time < 1ms | **Maybe** | Very fast iterations; batch dispatching overhead may dominate |
| Iteration allocates > 100MB memory | **Caution** | Memory multiplied by n_workers; may cause swapping |
| Iteration uses GPU | **Usually No** | GPU already parallelizes; CPU parallelism adds overhead |
| Parameter sweep with > 50 cells | **Yes (across cells)** | Cells are independent; excellent parallelism |
| ABM with sequential steps | **No (per-run)** | Steps are sequential; parallelize across runs instead |
| Bootstrap resampling | **Yes** | Resamples are independent; trivially parallel |

### Overhead Estimation

Before parallelizing, estimate whether it is worth it:

```python
import time

# Measure single iteration time
start = time.perf_counter()
for _ in range(10):
    single_iteration(rngs[0], params)
iteration_time = (time.perf_counter() - start) / 10

# Estimate overhead per worker
worker_overhead = 0.1  # ~100ms per worker startup (joblib/loky)
n_workers = os.cpu_count()

# Sequential time
sequential_time = iteration_time * n_iterations

# Parallel time (ideal)
parallel_time = (iteration_time * n_iterations / n_workers) + (worker_overhead * n_workers)

# Decision
speedup = sequential_time / parallel_time
print(f"Estimated speedup: {speedup:.1f}x")
if speedup < 1.5:
    print("Parallelization not worth the overhead. Run sequentially.")
else:
    print(f"Parallelize with {n_workers} workers.")
```

### Amdahl's Law

The maximum speedup from parallelization is limited by the sequential fraction of the code:

```
Speedup = 1 / (s + (1-s)/p)

where:
  s = fraction of code that is sequential (convergence checking, setup, teardown)
  p = number of parallel workers
```

For simulation-runner:
- s is typically < 5% (convergence checking is fast)
- Near-linear speedup up to ~8 workers for most simulations
- Diminishing returns beyond 16 workers due to memory bandwidth

---

## Parallel Patterns for Specific Simulation Types

### Monte Carlo / Bootstrap

Trivially parallel. Each iteration is independent.

```python
results = Parallel(n_jobs=-1)(
    delayed(single_iteration)(rngs[i], params)
    for i in range(n_iterations)
)
```

### Parameter Sweep

Parallelize across grid cells. Each cell runs its own set of iterations.

```python
def run_cell(cell_params, cell_rngs, base_params, n_per_cell):
    """Run all iterations for one grid cell."""
    results = []
    for i in range(n_per_cell):
        params = {**base_params, **cell_params}
        data = dgp(cell_rngs[i], params)
        result = analyze(data, params)
        results.append(result)
    return results

# Parallelize across cells (not within cells)
cell_results = Parallel(n_jobs=-1)(
    delayed(run_cell)(grid[c], cell_rngs[c], base_params, n_per_cell)
    for c in range(len(grid))
)
```

### Agent-Based Model

Parallelize across independent runs. Within a run, steps are sequential.

```python
def single_run(rng, params, n_steps):
    """One complete ABM run."""
    agents = initialize_agents(params, rng)
    topology = build_topology(params, rng)
    history = []
    for t in range(n_steps):
        summary = abm_step(agents, topology, rng, params)
        history.append(summary)
    return history

# Parallelize across runs
all_runs = Parallel(n_jobs=-1)(
    delayed(single_run)(run_rngs[r], params, n_steps)
    for r in range(n_runs)
)
```

### Multiple Chains

Parallelize across chains. Within each chain, iterations are sequential (for autocorrelated chains) or parallelizable (for i.i.d.).

```python
def run_chain(chain_rng, params, n_iterations):
    """One chain of the simulation."""
    results = []
    for i in range(n_iterations):
        result = dgp_and_analyze(chain_rng, params)
        results.append(result)
    return results

# Parallelize across chains
chains = Parallel(n_jobs=n_chains)(
    delayed(run_chain)(chain_rngs[c], params, n_iterations_per_chain)
    for c in range(n_chains)
)
```

---

## Troubleshooting

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Pickle error | `Can't pickle <lambda>` | Use named functions, not lambdas; or switch to cloudpickle backend |
| Memory explosion | Workers use too much RAM | Reduce n_jobs, use memory mapping, reduce per-iteration allocations |
| Hung workers | Simulation appears frozen | Set timeout in joblib; check for deadlocks in custom code |
| Different results with different n_jobs | Results change when varying worker count | Ensure SeedSequence pattern is used; each iteration must have its own RNG |
| Windows `RuntimeError` | "freeze_support" error | Wrap parallel code in `if __name__ == '__main__'` guard |
| Slow with many tiny tasks | Overhead > computation time | Increase batch_size or switch to sequential |

### Debugging Parallel Code

```python
# Step 1: Verify sequential correctness first
results_sequential = [single_iteration(rngs[i], params) for i in range(10)]

# Step 2: Run parallel with n_jobs=1 (sequential, but through joblib machinery)
results_joblib_1 = Parallel(n_jobs=1)(
    delayed(single_iteration)(rngs[i], params) for i in range(10)
)

# Step 3: Run parallel with n_jobs=-1
results_parallel = Parallel(n_jobs=-1)(
    delayed(single_iteration)(rngs[i], params) for i in range(10)
)

# Step 4: Verify all three produce identical results
assert results_sequential == results_joblib_1 == results_parallel
```

---

## Performance Tips

1. **Pre-compute shared read-only data** outside the parallel loop; pass as argument
2. **Minimize return data size**: Return summary statistics, not full datasets
3. **Use numpy vectorization inside iterations**: Each iteration should be fast
4. **Profile first**: `time.perf_counter()` a single iteration before deciding on parallelism
5. **Monitor memory**: `psutil.virtual_memory()` during parallel runs
6. **Batch dispatching**: For convergence-monitored simulations, use the batch pattern above
7. **Avoid nested parallelism**: If iteration code uses parallel numpy (MKL/OpenBLAS), set `OMP_NUM_THREADS=1` per worker

```python
import os
os.environ['OMP_NUM_THREADS'] = '1'  # Prevent nested parallelism
os.environ['MKL_NUM_THREADS'] = '1'
```

---

## References

- joblib Documentation. https://joblib.readthedocs.io/
- Python multiprocessing Documentation. https://docs.python.org/3/library/multiprocessing.html
- Amdahl, G. M. (1967). Validity of the single processor approach to achieving large scale computing capabilities. *AFIPS Conference Proceedings*, 30, 483-485.
