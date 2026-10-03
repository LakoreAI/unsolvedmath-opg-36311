"""Additive-combinatorics probes for the worst-case representation dichotomy.

The Phase 1 hypothesis is: every subset-sum instance is either *structured*
(near-geometric / low-collision, so it collapses to a small subproblem) or has
*many representations* (so subsampling / dissection applies). These helpers
measure the quantities that make the dichotomy concrete:

  * ``subset_sums``          — the reachable-sum set S(A), |S(A)|;
  * ``collision_count``      — F = sum_t max(0, count(t) - 1), the PESS quantity;
  * ``additive_energy``      — E = sum_s r(s)^2 for the sum set;
  * ``near_geometric_distance`` — how far the sorted weights are from 2^i.

All routines are exact and intended for small n.
"""

from collections import Counter
from itertools import combinations
from typing import Sequence


def subset_sums(values: Sequence[int]) -> list[int]:
    """Sorted list of all 2^n subset sums (with duplicates removed)."""
    sums = {0}
    for a in values:
        sums |= {s + a for s in sums}
    return sorted(sums)


def subset_sum_counts(values: Sequence[int]) -> Counter:
    """Multiplicity of every reachable subset sum."""
    counts = Counter({0: 1})
    for a in values:
        updated = Counter(counts)
        for total, multiplicity in counts.items():
            updated[total + a] += multiplicity
        counts = updated
    return counts


def collision_count(values: Sequence[int]) -> int:
    """F = sum_t max(0, count(t) - 1): the number of colliding subset-sum pairs."""
    counts = subset_sum_counts(values)
    return sum(c - 1 for c in counts.values() if c > 1)


def representation_count(values: Sequence[int], target: int) -> int:
    """Number of subsets summing exactly to ``target``."""
    return subset_sum_counts(values).get(target, 0)


def additive_energy(elements: Sequence[int]) -> int:
    """E = sum_s r(s)^2 where r(s) = #{(a, b) : a + b = s} over ``elements``."""
    items = list(elements)
    pair_counts: Counter = Counter()
    for a in items:
        for b in items:
            pair_counts[a + b] += 1
    return sum(r * r for r in pair_counts.values())


def near_geometric_distance(values: Sequence[int]) -> int:
    """max_i |a_i - 2^i| over the sorted weights (0 means exactly geometric)."""
    ordered = sorted(values)
    if not ordered:
        return 0
    return max(abs(value - (1 << i)) for i, value in enumerate(ordered))


def cardinality_counts(values: Sequence[int], target: int) -> dict[int, int]:
    """Number of subsets of each cardinality summing to ``target``.

    ``counts[k]`` is the number of size-``k`` subsets with sum ``target``.
    Overlapping pairs in an HGJ merge correspond to target representations of
    cardinality below the solution's weight, so these counts lower-bound the
    pseudo-solution load.
    """
    values = list(values)
    n = len(values)
    dp = [Counter() for _ in range(n + 1)]
    dp[0][0] = 1
    for a in values:
        for k in range(n - 1, -1, -1):
            for total, multiplicity in dp[k].items():
                dp[k + 1][total + a] += multiplicity
    return {k: dp[k].get(target, 0) for k in range(n + 1)}


def representation_residues(
    values: Sequence[int], solution_mask: int, weight: int, modulus: int
) -> Counter:
    """Residues a.y mod ``modulus`` over weight-``weight`` sub-masks of a solution.

    These are the modular residues that the HGJ filter sees for the
    representations of one fixed solution. A spread-out profile (coverage near
    1) means a random residue picks up a representation with high probability.
    """
    ones = [i for i in range(len(values)) if solution_mask >> i & 1]
    residues: Counter = Counter()
    for comb in combinations(ones, weight):
        residues[sum(values[i] for i in comb) % modulus] += 1
    return residues


def residue_profile(
    values: Sequence[int], solution_mask: int, weight: int, modulus: int
) -> dict:
    """Coverage summary of the representations' modular residues."""
    residues = representation_residues(values, solution_mask, weight, modulus)
    decompositions = sum(residues.values())
    return {
        "decompositions": decompositions,
        "distinct_residues": len(residues),
        "coverage": len(residues) / modulus,
        "max_bucket": max(residues.values()) if residues else 0,
    }


def longest_arithmetic_progression(elements: Sequence[int], cap: int = 10**9) -> int:
    """Longest arithmetic progression inside a sorted set (brute force, small)."""
    ordered = sorted(set(elements))
    index = {v: i for i, v in enumerate(ordered)}
    best = 1
    for i in range(len(ordered)):
        for j in range(i + 1, len(ordered)):
            step = ordered[j] - ordered[i]
            if step == 0:
                continue
            length = 2
            nxt = ordered[j] + step
            while nxt in index and length < cap:
                length += 1
                nxt += step
            best = max(best, length)
    return best
