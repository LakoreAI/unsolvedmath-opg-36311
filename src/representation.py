"""Candidate worst-case `{0,1}` subset sum via HGJ representations.

Implements the attack pipeline of `docs/research/subset-sum-n3/ATTACK.md`:

  * structural branch: divide a common factor, and solve superincreasing
    (powers-of-two-like) instances greedily -- the "easy" side of the mixing
    dichotomy;
  * representation branch: the HGJ modular filter plus an exact disjointness
    (sparse Orthogonal Vectors) match, on the balanced-solution regime;
  * exact fallback: meet-in-the-middle, so the result is always correct.

The mixed (larger) branch's worst-case speed needs the target-problem mixing
dichotomy, which is open; this module is a correct candidate and testbed, not a
proof of a `2^((1/2-eps)n)` bound.
"""

from dataclasses import dataclass
from itertools import combinations
from math import gcd
from typing import Sequence

from src.hgj import hgj_search
from src.subset_sum import meet_in_middle


@dataclass(frozen=True)
class RepresentationResult:
    indices: tuple[int, ...] | None
    strategy: str
    enumerated: int

    @property
    def feasible(self) -> bool:
        return self.indices is not None


def superincreasing_solve(values: Sequence[int], target: int) -> tuple[int, ...] | None:
    """Solve a positive superincreasing instance by greedy from the largest.

    Returns the occurrence indices, ``None`` if the target is unreachable, or
    raises ``ValueError`` if the instance is not superincreasing.
    """
    order = sorted(range(len(values)), key=values.__getitem__)
    running = 0
    for position in order:
        if values[position] <= running:
            raise ValueError("instance is not superincreasing")
        running += values[position]
    chosen: list[int] = []
    remaining = target
    for position in reversed(order):
        if remaining < 0:
            return None
        if values[position] <= remaining:
            chosen.append(position)
            remaining -= values[position]
    if remaining != 0:
        return None
    return tuple(sorted(chosen))


def mixing_coverage(
    values: Sequence[int], solution: Sequence[int], weight: int, modulus: int
) -> float:
    """Fraction of residues hit by the weight-``weight`` representations of a
    solution's support (the HGJ mixing condition). One valued at a single point.
    """
    support = list(solution)
    if weight < 0 or weight > len(support):
        raise ValueError("weight must be between 0 and the solution size")
    residues = {
        sum(values[support[i]] for i in comb) % modulus
        for comb in combinations(range(len(support)), weight)
    }
    return len(residues) / modulus


def _reduce_common_factor(
    values: tuple[int, ...], target: int
) -> tuple[tuple[int, ...], int, int] | None:
    """Divide out the gcd of all values; ``None`` if the target is unreachable."""
    factor = 0
    for value in values:
        factor = gcd(factor, value)
    if factor == 0:
        return values, target, 1
    if target % factor:
        return None
    return tuple(value // factor for value in values), target // factor, factor


def representation_subset_sum(
    values: Sequence[int],
    target: int,
    weight: int | None = None,
    residues: int = 8,
    seed: int = 0,
) -> RepresentationResult:
    """Solve `{0,1}` subset sum by the candidate representation pipeline.

    Branches: gcd reduction, superincreasing greedy, HGJ representation search,
    and a meet-in-the-middle fallback. Always correct (the fallback is exact).
    """
    values = tuple(values)
    reduced = _reduce_common_factor(values, target)
    if reduced is None:
        return RepresentationResult(None, "infeasible", 0)
    scaled, scaled_target, _factor = reduced

    try:
        greedy = superincreasing_solve(scaled, scaled_target)
    except ValueError:
        greedy = None
    if greedy is not None:
        return RepresentationResult(greedy, "superincreasing", len(scaled))
    # A non-superincreasing instance can still be infeasible; only trust the
    # greedy result when it succeeds.

    search = hgj_search(
        scaled,
        scaled_target,
        weight=weight if weight is not None else len(scaled) // 2,
        residues=residues,
        seed=seed,
    )
    if search.feasible:
        return RepresentationResult(search.indices, "representation", search.enumerated)

    fallback = meet_in_middle(scaled, scaled_target)
    return RepresentationResult(fallback.indices, "mitm", fallback.states)
