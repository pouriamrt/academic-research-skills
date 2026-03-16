# Randomization Methods — Allocation Schemes with Python Code

## Purpose

A comprehensive reference for randomization methods in experimental research. Covers simple random, stratified, block, cluster, and adaptive randomization with complete Python code using `numpy.random.Generator` (NOT legacy `RandomState`). Includes seed management best practices and guidance on when NOT to randomize. Used by the randomization_agent.

---

## Critical Rule: Use Modern RNG API

**ALWAYS** use `numpy.random.Generator` via `numpy.random.default_rng()`.

**NEVER** use:
- `numpy.random.RandomState` (deprecated)
- `numpy.random.seed()` (global state, not reproducible across threads)
- `numpy.random.randint()`, `numpy.random.choice()`, etc. (legacy top-level functions)

```python
# CORRECT
import numpy as np
rng = np.random.default_rng(seed=42)
result = rng.choice(['Treatment', 'Control'], size=100)

# WRONG - DO NOT USE
np.random.seed(42)                    # Global state
np.random.choice(['T', 'C'], size=100)  # Legacy API
rs = np.random.RandomState(42)        # Deprecated class
```

**Why**: The Generator API uses the PCG64 algorithm, which has better statistical properties, is faster, and supports reproducible parallel streams. Legacy RandomState uses Mersenne Twister with known weaknesses for simulation work.

---

## Method 1: Simple Random Assignment

### Description
Every participant has an equal, independent probability of being assigned to each group. The simplest and most fundamental method.

### When to Use
- Large sample sizes (N > 200 per group)
- Exact balance between groups is not critical
- No important prognostic variables to control for

### When NOT to Use
- Small samples (N < 50 total) where imbalance is likely
- When exact group balance is required for analysis (e.g., factorial designs)
- When there are known important covariates

### Python Code

```python
import numpy as np

def simple_random_assignment(n_total, groups, allocation_ratio=None, seed=42):
    """
    Simple random assignment to groups.

    Parameters:
        n_total: int — Total number of participants
        groups: list[str] — Group labels (e.g., ['Treatment', 'Control'])
        allocation_ratio: list[int] — Allocation ratios (e.g., [1, 1] for equal)
                         If None, equal allocation is used.
        seed: int — Random seed for reproducibility

    Returns:
        np.ndarray — Array of group assignments
    """
    rng = np.random.default_rng(seed)
    n_groups = len(groups)

    if allocation_ratio is None:
        allocation_ratio = [1] * n_groups

    probs = np.array(allocation_ratio, dtype=float)
    probs /= probs.sum()

    assignments = rng.choice(groups, size=n_total, p=probs)

    # Report balance
    unique, counts = np.unique(assignments, return_counts=True)
    print("Group balance:")
    for g, c in zip(unique, counts):
        print(f"  {g}: n={c} ({c/n_total*100:.1f}%)")

    return assignments


# Example: 100 participants, 1:1 ratio
assignments = simple_random_assignment(
    n_total=100,
    groups=['Treatment', 'Control'],
    seed=42
)

# Example: 150 participants, 2:1 ratio (treatment:control)
assignments_unequal = simple_random_assignment(
    n_total=150,
    groups=['Treatment', 'Control'],
    allocation_ratio=[2, 1],
    seed=42
)
```

---

## Method 2: Block Randomization

### Description
Divides the participant sequence into blocks of fixed size. Within each block, the number of assignments to each group is predetermined, ensuring balance after every complete block.

### When to Use
- Small to medium samples (N < 200)
- When approximate balance is needed at all points during enrollment (not just at the end)
- When interim analyses are planned

### Critical Rule: Varying Block Sizes
If block size is fixed and known, the last assignment in each block is predictable (potentially biasing enrollment decisions). **Always use varying block sizes** to prevent this.

### Python Code

```python
import numpy as np

def block_randomization(n_total, groups, block_sizes=None, seed=42):
    """
    Block randomization with varying block sizes.

    Parameters:
        n_total: int — Total number of participants
        groups: list[str] — Group labels
        block_sizes: list[int] — Possible block sizes (must be multiples of n_groups).
                    If None, uses [2*k, 3*k, 4*k] where k = len(groups).
        seed: int — Random seed

    Returns:
        np.ndarray — Array of group assignments
    """
    rng = np.random.default_rng(seed)
    n_groups = len(groups)

    if block_sizes is None:
        block_sizes = [n_groups * m for m in [2, 3, 4]]

    # Validate block sizes
    for bs in block_sizes:
        if bs % n_groups != 0:
            raise ValueError(f"Block size {bs} is not a multiple of {n_groups} groups")

    assignments = []

    while len(assignments) < n_total:
        # Randomly select a block size
        bs = rng.choice(block_sizes)
        reps_per_group = bs // n_groups

        # Create block with equal representation
        block = []
        for g in groups:
            block.extend([g] * reps_per_group)

        # Shuffle the block
        rng.shuffle(block)
        assignments.extend(block)

    # Trim to exact n_total
    assignments = np.array(assignments[:n_total])

    # Report
    unique, counts = np.unique(assignments, return_counts=True)
    print("Block randomization result:")
    for g, c in zip(unique, counts):
        print(f"  {g}: n={c} ({c/n_total*100:.1f}%)")
    print(f"  Block sizes used: {block_sizes} (varying)")

    return assignments


# Example: 60 participants, 2 groups, varying blocks of 4, 6, 8
assignments = block_randomization(
    n_total=60,
    groups=['Treatment', 'Control'],
    block_sizes=[4, 6, 8],
    seed=42
)

# Example: 90 participants, 3 groups, varying blocks of 6, 9, 12
assignments_3g = block_randomization(
    n_total=90,
    groups=['GroupA', 'GroupB', 'GroupC'],
    block_sizes=[6, 9, 12],
    seed=42
)
```

---

## Method 3: Stratified Randomization

### Description
Combines stratification (grouping by important prognostic variables) with block randomization within each stratum. Ensures balance on known important variables across groups.

### When to Use
- Known prognostic variables that could confound results (e.g., gender, baseline severity, site)
- Small to medium samples where random chance could produce meaningful imbalance

### Rule of Thumb
Stratify on **no more than 2-3 variables**. With k variables having l levels each, the number of strata = product of all levels. Too many strata with small N leads to incomplete blocks.

### Python Code

```python
import numpy as np
import pandas as pd

def stratified_randomization(participants_df, strata_columns, groups,
                              block_sizes=None, seed=42):
    """
    Stratified block randomization.

    Parameters:
        participants_df: pd.DataFrame — Must have columns for strata_columns
        strata_columns: list[str] — Columns to stratify by
        groups: list[str] — Group labels
        block_sizes: list[int] — Block sizes (multiples of len(groups))
        seed: int — Base seed (each stratum gets seed + stratum_index)

    Returns:
        pd.DataFrame — Input DataFrame with added 'group' column
    """
    rng = np.random.default_rng(seed)
    n_groups = len(groups)

    if block_sizes is None:
        block_sizes = [n_groups * m for m in [2, 3, 4]]

    df = participants_df.copy()
    df['group'] = ''

    # Group by strata
    strata = df.groupby(strata_columns)

    print(f"Stratified randomization:")
    print(f"  Strata columns: {strata_columns}")
    print(f"  Number of strata: {len(strata)}")
    print()

    stratum_seed = seed
    for stratum_name, stratum_df in strata:
        stratum_seed += 1
        n_stratum = len(stratum_df)

        # Block randomize within this stratum
        stratum_rng = np.random.default_rng(stratum_seed)
        assignments = []

        while len(assignments) < n_stratum:
            bs = stratum_rng.choice(block_sizes)
            reps = bs // n_groups
            block = []
            for g in groups:
                block.extend([g] * reps)
            stratum_rng.shuffle(block)
            assignments.extend(block)

        assignments = assignments[:n_stratum]
        df.loc[stratum_df.index, 'group'] = assignments

        # Report per stratum
        unique, counts = np.unique(assignments, return_counts=True)
        balance_str = ", ".join(f"{g}={c}" for g, c in zip(unique, counts))
        print(f"  Stratum {stratum_name}: n={n_stratum}, {balance_str}")

    print()
    # Overall balance
    overall = df['group'].value_counts()
    print("Overall balance:")
    for g, c in overall.items():
        print(f"  {g}: n={c} ({c/len(df)*100:.1f}%)")

    return df


# Example: Stratify by gender and year
rng_demo = np.random.default_rng(0)
participants = pd.DataFrame({
    'id': [f'P{i:03d}' for i in range(1, 81)],
    'gender': rng_demo.choice(['M', 'F'], 80),
    'year': rng_demo.choice(['Freshman', 'Sophomore', 'Junior', 'Senior'], 80)
})

result = stratified_randomization(
    participants_df=participants,
    strata_columns=['gender', 'year'],
    groups=['Treatment', 'Control'],
    seed=42
)
```

---

## Method 4: Cluster Randomization

### Description
Randomize entire clusters (classrooms, clinics, communities) rather than individuals. All individuals within a cluster receive the same treatment.

### When to Use
- Individual randomization would cause contamination (e.g., students in the same classroom)
- The intervention is delivered at the group level (e.g., teacher training)
- Logistically infeasible to randomize individuals

### Important: Power Analysis Adjustment
Cluster designs have fewer independent units (clusters, not individuals). The power analysis must account for the design effect. See `references/power_analysis_guide.md` for details.

### Python Code

```python
import numpy as np

def cluster_randomization(clusters, groups, seed=42):
    """
    Cluster-level randomization.

    Parameters:
        clusters: dict[str, int] — Mapping of cluster_id -> cluster_size
        groups: list[str] — Group labels
        seed: int — Random seed

    Returns:
        dict[str, str] — Mapping of cluster_id -> group assignment
    """
    rng = np.random.default_rng(seed)
    n_groups = len(groups)
    cluster_ids = list(clusters.keys())
    n_clusters = len(cluster_ids)

    # Block randomize clusters for balance
    assignments = []
    bs = n_groups * 2  # block size
    while len(assignments) < n_clusters:
        block = groups * (bs // n_groups)
        rng.shuffle(block)
        assignments.extend(block)

    assignments = assignments[:n_clusters]
    cluster_assignments = dict(zip(cluster_ids, assignments))

    # Report
    print(f"Cluster randomization (seed={seed}):")
    for g in groups:
        g_clusters = [c for c, a in cluster_assignments.items() if a == g]
        g_n = sum(clusters[c] for c in g_clusters)
        print(f"  {g}: {len(g_clusters)} clusters, {g_n} individuals")
        for c in g_clusters:
            print(f"    {c}: n={clusters[c]}")

    return cluster_assignments


# Example: 8 classrooms
clusters = {
    'Class_A': 25, 'Class_B': 28, 'Class_C': 22, 'Class_D': 30,
    'Class_E': 26, 'Class_F': 24, 'Class_G': 27, 'Class_H': 23,
}

result = cluster_randomization(
    clusters=clusters,
    groups=['Treatment', 'Control'],
    seed=42
)
```

---

## Method 5: Adaptive Randomization (Minimization)

### Description
Dynamically assigns each new participant to the group that minimizes imbalance across multiple prognostic factors. Not purely random — the allocation probability is biased toward the group that would create better balance.

### When to Use
- Small trials (N < 50) with multiple important prognostic variables
- When stratified randomization would create too many strata for the available N

### Controversy
Some methodologists argue that minimization is not truly random and therefore standard statistical tests may not be valid. Counter-argument: adding a random element (e.g., assigning to the preferred group with p = 0.75 rather than p = 1.0) preserves unpredictability while maintaining balance.

### Python Code

```python
import numpy as np
import pandas as pd

def minimization_assignment(allocated_df, new_participant, factor_columns,
                             groups, p_preferred=0.75, rng=None):
    """
    Assign a single new participant using minimization.

    Parameters:
        allocated_df: pd.DataFrame — Already-allocated participants with
                     factor columns and 'group' column
        new_participant: dict — Factor values for the new participant
        factor_columns: list[str] — Columns to balance on
        groups: list[str] — Group labels
        p_preferred: float — Probability of assigning to the most-balanced group
                    (1.0 = deterministic; 0.5 = simple random)
        rng: np.random.Generator — Random number generator

    Returns:
        str — Group assignment for the new participant
    """
    if rng is None:
        rng = np.random.default_rng()

    # Calculate marginal imbalance for each possible assignment
    group_scores = {}

    for candidate_group in groups:
        total_imbalance = 0

        for factor in factor_columns:
            factor_value = new_participant[factor]
            # Participants in the same stratum
            same_stratum = allocated_df[allocated_df[factor] == factor_value]

            for g in groups:
                count = len(same_stratum[same_stratum['group'] == g])
                if g == candidate_group:
                    count += 1  # Hypothetical assignment

            # Calculate range (max - min across groups) for this factor
            counts = []
            for g in groups:
                c = len(same_stratum[same_stratum['group'] == g])
                if g == candidate_group:
                    c += 1
                counts.append(c)
            total_imbalance += max(counts) - min(counts)

        group_scores[candidate_group] = total_imbalance

    # Find the group with minimum imbalance
    min_score = min(group_scores.values())
    preferred_groups = [g for g, s in group_scores.items() if s == min_score]

    if len(preferred_groups) == 1:
        preferred = preferred_groups[0]
    else:
        preferred = rng.choice(preferred_groups)

    # Apply randomized element
    if rng.random() < p_preferred:
        return preferred
    else:
        others = [g for g in groups if g != preferred]
        return rng.choice(others)


# Example usage: sequential enrollment
rng = np.random.default_rng(42)
groups = ['Treatment', 'Control']
factors = ['gender', 'severity']

# Simulate incoming participants
incoming = pd.DataFrame({
    'id': [f'P{i:03d}' for i in range(1, 41)],
    'gender': rng.choice(['M', 'F'], 40),
    'severity': rng.choice(['Mild', 'Moderate', 'Severe'], 40)
})

allocated = pd.DataFrame(columns=['id', 'gender', 'severity', 'group'])

for _, row in incoming.iterrows():
    assignment = minimization_assignment(
        allocated_df=allocated,
        new_participant=row.to_dict(),
        factor_columns=factors,
        groups=groups,
        p_preferred=0.75,
        rng=rng
    )
    new_row = row.to_dict()
    new_row['group'] = assignment
    allocated = pd.concat([allocated, pd.DataFrame([new_row])], ignore_index=True)

# Report balance
print("Overall balance:")
print(allocated['group'].value_counts())
print("\nBalance by gender:")
print(pd.crosstab(allocated['gender'], allocated['group']))
print("\nBalance by severity:")
print(pd.crosstab(allocated['severity'], allocated['group']))
```

---

## Seed Management Best Practices

### Rules

1. **Record the seed BEFORE generating any sequence**: The seed is part of the experimental record
2. **Use a single master seed**: Derive deterministic sub-seeds for strata or phases
3. **Use integer seeds**: Avoid string seeds, float seeds, or system-time seeds
4. **Document the algorithm**: "PCG64 via numpy.random.default_rng, numpy version X.Y.Z"
5. **Never reuse seeds across studies**: Each study gets a unique seed
6. **Store seeds in three places**: protocol document, analysis code, and a separate seed log

### Seed Documentation Template

```markdown
## Randomization Seed Record

**Study**: [Study title]
**Protocol ID**: [EXP-YYYYMMDD-NNN]
**Date**: [YYYY-MM-DD]

**Master Seed**: [integer]
**Algorithm**: PCG64 via numpy.random.default_rng()
**NumPy Version**: [X.Y.Z]
**Python Version**: [X.Y.Z]

**Derived Seeds** (if stratified):
| Purpose | Seed | Derivation |
|---------|------|-----------|
| Overall | 42 | Master seed |
| Stratum: Male/Freshman | 43 | Master + 1 |
| Stratum: Male/Sophomore | 44 | Master + 2 |
| ... | ... | ... |

**Verification**: Run the code below to reproduce the exact sequence.
```

### Reproducibility Verification

```python
import numpy as np

# Verify: this code must produce the EXACT same sequence as the original
rng = np.random.default_rng(seed=42)  # Same master seed

# Generate the same assignments
assignments = rng.choice(['Treatment', 'Control'], size=100)
print(f"First 10 assignments: {assignments[:10]}")
print(f"SHA-256 of assignments: {hashlib.sha256(assignments.tobytes()).hexdigest()[:16]}")
```

---

## When NOT to Randomize

| Situation | Reason | Alternative |
|-----------|--------|------------|
| Quasi-experimental design | Intact groups cannot be randomized | Propensity score matching, ANCOVA, DiD |
| Correlational study | No manipulation, only measurement | N/A (no allocation needed) |
| Single-subject design (optional) | Randomization of phase onset is optional | Visual analysis of phase changes |
| Ethical prohibition | Withholding effective treatment is unethical | Waitlist control, stepped wedge |
| Practical impossibility | Cannot control who receives treatment | Natural experiment, ITS, RDD |
| Pilot study | Exploring feasibility, not testing hypotheses | Convenience sampling is acceptable |

When randomization is skipped, the protocol must document:
1. **Why randomization is not possible** (specific reason)
2. **What alternative bias-reduction strategy is used** (matching, ANCOVA, DiD, etc.)
3. **What selection bias remains** and how it will be discussed in the limitations
