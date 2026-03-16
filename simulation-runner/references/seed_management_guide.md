# Seed Management Guide — Reproducible Random Number Generation

## Purpose

A comprehensive reference for managing random seeds in simulations to ensure exact reproducibility. Covers the modern numpy `Generator` API, `SeedSequence` for parallel streams, recording seeds in output, and common pitfalls.

---

## Fundamental Rule

> **Always use `numpy.random.Generator`. Never use `numpy.random.RandomState` or `np.random.seed()`.**

The legacy `RandomState` API has known issues with parallel reproducibility, poor statistical quality for some distributions, and global state that creates hidden dependencies. The modern `Generator` API solves all of these.

---

## numpy.random.Generator vs Legacy RandomState

### Comparison

| Feature | Generator (Modern) | RandomState (Legacy) |
|---------|-------------------|---------------------|
| API | `rng = default_rng(seed)` | `np.random.seed(seed)` or `RandomState(seed)` |
| State management | Explicit object, no global state | Global state via `np.random.seed()` |
| Parallel safety | Guaranteed independence via SeedSequence | No guarantee; seed collisions possible |
| Statistical quality | PCG64 (default), superior randomness | Mersenne Twister, adequate but older |
| Distribution quality | Uses improved algorithms (e.g., Lemire for integers) | Older algorithms |
| Reproducibility | Exact, per-Generator object | Global state can be corrupted by library code |
| Thread safety | Each Generator is independent | Global state is not thread-safe |

### Migration Examples

| Legacy Code (DO NOT USE) | Modern Code (USE THIS) |
|--------------------------|----------------------|
| `np.random.seed(42)` | `rng = np.random.default_rng(42)` |
| `np.random.normal(0, 1, 100)` | `rng.normal(0, 1, 100)` |
| `np.random.choice(arr, 50)` | `rng.choice(arr, 50)` |
| `np.random.randint(0, 10, 50)` | `rng.integers(0, 10, 50)` |
| `np.random.random(100)` | `rng.random(100)` |
| `np.random.shuffle(arr)` | `rng.shuffle(arr)` |
| `np.random.permutation(arr)` | `rng.permutation(arr)` |
| `np.random.uniform(0, 1, 100)` | `rng.uniform(0, 1, 100)` |
| `np.random.RandomState(42)` | `np.random.default_rng(42)` |

### Important API Differences

```python
import numpy as np
from numpy.random import default_rng

rng = default_rng(42)

# Generator uses 'integers' instead of 'randint'
# Generator's 'integers' has an exclusive upper bound by default
rng.integers(0, 10, size=5)  # values in [0, 10)
rng.integers(0, 10, size=5, endpoint=True)  # values in [0, 10]

# Generator's 'random' is equivalent to legacy 'random_sample'
rng.random(5)  # Uniform [0, 1)

# Generator's 'standard_normal' is the preferred way
rng.standard_normal(5)  # N(0,1)

# Boolean arrays
rng.choice([True, False], size=100, p=[0.3, 0.7])
```

---

## SeedSequence: The Key to Parallel Reproducibility

### What SeedSequence Solves

The fundamental problem with parallel simulations: how to create multiple independent random streams from a single master seed, such that:
1. Streams are statistically independent (no correlation between parallel workers)
2. Results are exactly reproducible (same master seed -> same results)
3. Results are independent of the number of parallel workers

`SeedSequence` solves all three.

### How SeedSequence Works

```python
from numpy.random import SeedSequence, default_rng

# Create a master SeedSequence from a single seed
master_ss = SeedSequence(42)

# Spawn child SeedSequences for parallel streams
children = master_ss.spawn(4)  # 4 independent child seeds

# Create Generators from children
rngs = [default_rng(child) for child in children]

# Each Generator produces a completely independent stream
# rngs[0], rngs[1], rngs[2], rngs[3] are independent
# Running rngs[0] does NOT affect rngs[1]'s state
```

### Property: Worker-Count Independence

This is the critical property for simulation reproducibility:

```python
# With 4 workers
ss = SeedSequence(42)
rngs_4 = [default_rng(s) for s in ss.spawn(10000)]

# With 2 workers (but same seeds)
ss = SeedSequence(42)
rngs_2 = [default_rng(s) for s in ss.spawn(10000)]

# rngs_4[i] and rngs_2[i] produce IDENTICAL sequences for all i
# Result: same output regardless of worker count
```

### Hierarchical Spawning

For complex simulations with multiple levels of parallelism:

```python
# Level 0: Master seed
master = SeedSequence(42)

# Level 1: One child per chain
chain_seeds = master.spawn(4)

# Level 2: Within each chain, one child per iteration batch
for chain_idx, chain_seed in enumerate(chain_seeds):
    batch_seeds = chain_seed.spawn(100)  # 100 batches per chain
    for batch_idx, batch_seed in enumerate(batch_seeds):
        rng = default_rng(batch_seed)
        # This rng is unique to (chain_idx, batch_idx)
        # and reproducible from master seed 42
```

### Entropy and State

```python
ss = SeedSequence(42)
print(ss.entropy)        # The user-provided seed: 42
print(ss.spawn_key)      # Tuple tracking the spawn hierarchy: ()
print(ss.pool_size)      # Size of internal state: 4

child = ss.spawn(1)[0]
print(child.entropy)     # Same as parent: 42
print(child.spawn_key)   # (0,) — first child
```

---

## Seed Patterns for Different Simulation Types

### Pattern 1: Monte Carlo (One RNG per Iteration)

```python
def run_monte_carlo(dgp_func, params, n_iterations, master_seed=42):
    """Each iteration gets its own RNG for perfect reproducibility."""
    ss = SeedSequence(master_seed)
    rngs = [default_rng(s) for s in ss.spawn(n_iterations)]

    results = []
    for i in range(n_iterations):
        result = dgp_func(rngs[i], params)
        results.append(result)

    return results
```

**Why one RNG per iteration?** If iteration 5 changes (e.g., bug fix in DGP), only iteration 5's results change. All other iterations remain identical. This enables incremental debugging.

### Pattern 2: Bootstrap (One RNG per Resample)

```python
def run_bootstrap(data, stat_func, n_bootstrap, master_seed=42):
    """Each bootstrap resample gets its own RNG."""
    ss = SeedSequence(master_seed)
    rngs = [default_rng(s) for s in ss.spawn(n_bootstrap)]

    boot_stats = []
    for b in range(n_bootstrap):
        idx = rngs[b].choice(len(data), size=len(data), replace=True)
        resample = data[idx]
        boot_stats.append(stat_func(resample))

    return np.array(boot_stats)
```

### Pattern 3: Multiple Chains (One RNG per Chain)

```python
def run_chains(dgp_func, params, n_iterations_per_chain, n_chains=4, master_seed=42):
    """Each chain gets its own RNG stream."""
    ss = SeedSequence(master_seed)
    chain_rngs = [default_rng(s) for s in ss.spawn(n_chains)]

    chains = []
    for c in range(n_chains):
        chain_results = []
        for i in range(n_iterations_per_chain):
            result = dgp_func(chain_rngs[c], params)
            chain_results.append(result)
        chains.append(chain_results)

    return chains
```

### Pattern 4: Parameter Sweep (One RNG per Cell)

```python
def run_sweep(dgp_func, base_params, grid, n_per_cell, master_seed=42):
    """Each grid cell gets its own set of RNGs."""
    ss = SeedSequence(master_seed)
    cell_seeds = ss.spawn(len(grid))

    results = {}
    for cell_idx, (cell_params, cell_ss) in enumerate(zip(grid, cell_seeds)):
        cell_rngs = [default_rng(s) for s in cell_ss.spawn(n_per_cell)]
        cell_results = []
        for i in range(n_per_cell):
            params = {**base_params, **cell_params}
            result = dgp_func(cell_rngs[i], params)
            cell_results.append(result)
        results[cell_idx] = cell_results

    return results
```

### Pattern 5: Agent-Based Model (One RNG per Run, Internal per Step)

```python
def run_abm(agent_class, topology, params, n_steps, n_runs=100, master_seed=42):
    """Each run gets its own RNG that advances through steps."""
    ss = SeedSequence(master_seed)
    run_rngs = [default_rng(s) for s in ss.spawn(n_runs)]

    all_runs = []
    for r in range(n_runs):
        # Single RNG per run; advances through steps
        rng = run_rngs[r]
        agents = initialize_agents(agent_class, params, rng)
        history = []
        for t in range(n_steps):
            step_result = abm_step(agents, topology, rng, params)
            history.append(step_result)
        all_runs.append(history)

    return all_runs
```

---

## Seed Log Format

Every simulation must produce a seed log. This log is the single document that enables exact reproduction.

### Minimal Seed Log

```markdown
## Seed Log

**Master Seed**: 42
**Method**: numpy.random.SeedSequence
**Streams Created**: 10,000 (one per iteration)

**Reproduction**:
```python
from numpy.random import SeedSequence, default_rng
ss = SeedSequence(42)
rngs = [default_rng(s) for s in ss.spawn(10000)]
# rngs[i] reproduces iteration i exactly
```
```

### Full Seed Log (for complex simulations)

```markdown
## Seed Log

**Master Seed**: 42
**SeedSequence Entropy**: [42]
**numpy Version**: 1.26.4
**BitGenerator**: PCG64

### Stream Hierarchy

Level 0: SeedSequence(42)
Level 1: 4 chains, spawned from Level 0
Level 2: 2,500 iterations per chain, spawned from each Level 1

| Chain | Stream Index | SeedSequence Path | Purpose |
|-------|-------------|-------------------|---------|
| 0 | 0-2499 | ss.spawn(4)[0].spawn(2500)[i] | Chain 1 iterations |
| 1 | 2500-4999 | ss.spawn(4)[1].spawn(2500)[i] | Chain 2 iterations |
| 2 | 5000-7499 | ss.spawn(4)[2].spawn(2500)[i] | Chain 3 iterations |
| 3 | 7500-9999 | ss.spawn(4)[3].spawn(2500)[i] | Chain 4 iterations |

### Reproduction Command

```python
from numpy.random import SeedSequence, default_rng

master = SeedSequence(42)
chain_seeds = master.spawn(4)

# To reproduce chain c, iteration i:
chain_ss = chain_seeds[c]
iter_rngs = [default_rng(s) for s in chain_ss.spawn(2500)]
rng_for_iteration_i = iter_rngs[i]
```

### Verification

To verify seed correctness, the first 5 values from rngs[0].standard_normal(5) should be:
[list 5 values for verification]
```

---

## Common Pitfalls and Solutions

### Pitfall 1: Using Global Random State

```python
# BAD: Global state can be corrupted by imported libraries
np.random.seed(42)
result = np.random.normal(0, 1, 100)  # Some library may have called np.random.xxx in between!

# GOOD: Explicit Generator, no global state
rng = default_rng(42)
result = rng.normal(0, 1, 100)  # Always deterministic
```

### Pitfall 2: Sharing RNG Across Parallel Workers

```python
# BAD: All workers share the same RNG state -> race condition
rng = default_rng(42)
results = Parallel(n_jobs=4)(delayed(dgp)(rng, params) for _ in range(1000))

# GOOD: Each worker gets its own RNG
ss = SeedSequence(42)
rngs = [default_rng(s) for s in ss.spawn(1000)]
results = Parallel(n_jobs=4)(delayed(dgp)(rngs[i], params) for i in range(1000))
```

### Pitfall 3: Reusing Seeds Across Experiments

```python
# BAD: Same seed for different experiments makes results correlated
rng1 = default_rng(42)  # Experiment A
rng2 = default_rng(42)  # Experiment B -- correlated with A!

# GOOD: Unique seeds per experiment
rng1 = default_rng(42)    # Experiment A
rng2 = default_rng(12345) # Experiment B -- independent

# ALSO GOOD: Spawn from a master seed
master = SeedSequence(42)
rng_a, rng_b = [default_rng(s) for s in master.spawn(2)]
```

### Pitfall 4: Passing Seed Instead of Generator to networkx

```python
# networkx functions accept a seed parameter (integer or RandomState)
# but they do NOT accept Generator directly in older versions

# SAFE: Extract an integer seed from the Generator
seed_for_nx = int(rng.integers(0, 2**31))
graph = nx.watts_strogatz_graph(100, 4, 0.1, seed=seed_for_nx)
```

### Pitfall 5: Not Recording the Seed

```python
# BAD: Seed is lost
rng = default_rng()  # Random seed, not recorded

# GOOD: Always record the seed
master_seed = 42  # Or generate: int(SeedSequence().entropy)
rng = default_rng(master_seed)
# Record master_seed in seed log
```

---

## Testing Reproducibility

### Verification Protocol

After implementing seed management, verify reproducibility with this protocol:

```python
def verify_reproducibility(dgp_func, params, master_seed=42, n_test=5):
    """Run the simulation twice and verify identical results."""
    # Run 1
    ss1 = SeedSequence(master_seed)
    rngs1 = [default_rng(s) for s in ss1.spawn(n_test)]
    results1 = [dgp_func(rngs1[i], params) for i in range(n_test)]

    # Run 2 (identical seeds)
    ss2 = SeedSequence(master_seed)
    rngs2 = [default_rng(s) for s in ss2.spawn(n_test)]
    results2 = [dgp_func(rngs2[i], params) for i in range(n_test)]

    # Verify exact match
    for i in range(n_test):
        assert results1[i] == results2[i], f"Iteration {i} not reproducible!"

    print("Reproducibility verified.")
```

Run this verification before starting any full simulation.

---

## References

- NumPy Documentation: Random Generator. https://numpy.org/doc/stable/reference/random/generator.html
- NumPy Documentation: SeedSequence. https://numpy.org/doc/stable/reference/random/bit_generators/generated/numpy.random.SeedSequence.html
- O'Neill, M. E. (2014). PCG: A family of simple fast space-efficient statistically good algorithms for random number generation. Harvey Mudd College Technical Report HMC-CS-2014-0905.
- Salmon, J. K., Moraes, M. A., Dror, R. O., & Shaw, D. E. (2011). Parallel random numbers: As easy as 1, 2, 3. *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, Article 16.
