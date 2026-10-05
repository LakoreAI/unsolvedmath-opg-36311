"""Broadened-representation subset sum (Becker-Coron-Joux, ePrint 2011/474).

Ports the *broadened representation* of Section 3.1 of BCJ. A balanced solution
``epsilon in {0,1}^n`` of weight ``n/2`` is written as ``y + z`` with
``y, z in {-1,0,1}^n``, each containing ``(1/4 + alpha) n`` ones and
``alpha n`` minus-ones. The solution's ones split as ``(1,0)``/``(0,1)`` and its
zeros carry cancelling ``(1,-1)``/``(-1,1)`` gadgets; a modulus
``M ~ N_D = C(n/2,n/4) C(n/2; alpha n, alpha n, ...)`` filters the pieces. A
candidate pair is a **pseudo-solution** unless ``y + z in {0,1}^n``, which is the
compatibility condition the certificate must enforce.

This module implements the two-piece (single-level) broadened search with an
exact compatibility check; it deliberately does **not** implement BCJ's
three-level, eight-list recursion (Section 3.3), which is the remaining
engineering step (see ``docs/research/subset-sum-n3/NEXT.md``).
"""

from dataclasses import dataclass
from itertools import combinations
from math import comb, gcd
from random import Random
from typing import Sequence

from src.subset_sum import meet_in_middle


@dataclass(frozen=True)
class BcjResult:
    indices: tuple[int, ...] | None
    strategy: str
    enumerated: int

    @property
    def feasible(self) -> bool:
        return self.indices is not None


def enumerate_profile(n: int, ones: int, minus: int):
    """All ``(plus_mask, minus_mask)`` with ``ones`` +1s and ``minus`` -1s."""
    if ones < 0 or minus < 0 or ones + minus > n:
        return
    for plus_positions in combinations(range(n), ones):
        rest = [i for i in range(n) if i not in plus_positions]
        plus_mask = 0
        for i in plus_positions:
            plus_mask |= 1 << i
        for minus_positions in combinations(rest, minus):
            minus_mask = 0
            for i in minus_positions:
                minus_mask |= 1 << i
            yield plus_mask, minus_mask


def compatible(y_plus: int, y_minus: int, z_plus: int, z_minus: int) -> bool:
    """True iff ``y + z in {0,1}^n`` for the pieces ``y=(y_plus,y_minus)``, ``z``."""
    if y_plus & y_minus or z_plus & z_minus:
        return False
    if y_plus & z_plus:  # coordinate sum 2
        return False
    if y_minus & z_minus:  # coordinate sum -2
        return False
    if (y_minus ^ z_minus) & ~(y_plus | z_plus):  # coordinate sum -1
        return False
    return True


def _solution_support(y_plus, y_minus, z_plus, z_minus) -> int:
    return (y_plus | z_plus) & ~(y_minus | z_minus)


def representation_count(n: int, alpha: float) -> int:
    """``N_D`` of BCJ Sect. 3.1: the number of broadened representations."""
    half = n // 2
    extra = round(alpha * n)
    base = comb(half, half // 2)
    if extra < 0 or 2 * extra > half:
        return base
    return base * comb(half, extra) * comb(half - extra, extra)


def _next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def broadened_subset_sum(
    values: Sequence[int],
    target: int,
    alpha: float = 0.10,
    residues: int = 8,
    seed: int = 0,
) -> BcjResult:
    """Two-piece broadened search for a balanced ``{0,1}`` solution.

    Enumerates weight profiles ``(1/4+alpha)n`` ones and ``alpha n`` minus-ones
    for each piece, filters by a random modulus, and accepts a pair only when it
    is compatible (``y+z in {0,1}^n``) and the exact sums add to ``target``.
    Falls back to meet-in-the-middle, so the result is always correct.
    """
    values = tuple(values)
    n = len(values)
    if n < 4:
        fallback = meet_in_middle(values, target)
        return BcjResult(fallback.indices, "mitm", fallback.states)

    ones = round((0.25 + alpha) * n)
    minus = round(alpha * n)
    if ones < 0 or minus < 0 or ones + minus > n:
        fallback = meet_in_middle(values, target)
        return BcjResult(fallback.indices, "mitm", fallback.states)

    pieces = list(enumerate_profile(n, ones, minus))
    per_piece = len(pieces)
    enumerated = 0
    rng = Random(seed)
    # BCJ choose the modulus near the representation count N_D so that a random
    # residue retains about one representation.
    modulus = _next_prime(max(2, min(representation_count(n, alpha), 1 << n)))
    for _ in range(residues):
        residue = rng.randrange(modulus)
        enumerated += 2 * per_piece
        left = []
        right = []
        for plus, minus_mask in pieces:
            total = sum(values[i] for i in range(n) if plus >> i & 1) - sum(
                values[i] for i in range(n) if minus_mask >> i & 1
            )
            if total % modulus == residue:
                left.append((plus, minus_mask, total))
            if total % modulus == (target - residue) % modulus:
                right.append((plus, minus_mask, total))
        by_sum: dict[int, list[tuple[int, int]]] = {}
        for plus, minus_mask, total in right:
            by_sum.setdefault(total, []).append((plus, minus_mask))
        for y_plus, y_minus, y_total in left:
            for z_plus, z_minus in by_sum.get(target - y_total, ()):
                if compatible(y_plus, y_minus, z_plus, z_minus):
                    support = _solution_support(y_plus, y_minus, z_plus, z_minus)
                    indices = tuple(i for i in range(n) if support >> i & 1)
                    return BcjResult(indices, "bcj", enumerated)

    fallback = meet_in_middle(values, target)
    return BcjResult(fallback.indices, "mitm", enumerated + fallback.states)


def reduce_common_factor(
    values: Sequence[int], target: int
) -> tuple[tuple[int, ...], int] | None:
    """Divide out the gcd of all values; ``None`` if the target is unreachable."""
    factor = 0
    for value in values:
        factor = gcd(factor, value)
    if factor == 0:
        return tuple(values), target
    if target % factor:
        return None
    return tuple(value // factor for value in values), target // factor
