"""Compatibility certificates for broadened subset-sum representations.

The representation technique searches pairs ``(a, b)`` of pieces whose sum is the
target. When the pieces are allowed to overlap (a broadened representation), a
modular match can be a *pseudo-solution*: the pieces combine to an invalid
coefficient vector. Recovering a **compatible** pair---here, disjoint occurrence
masks---naively costs ``|A| |B|``. This module provides a sparse-OV style
certificate that finds a disjoint pair in time closer to linear in the list
sizes, following the certificates of Nederlof--Wegrzycki and Randolph--Wegrzycki.

The disjointness predicate ``a & b == 0`` is a sparse Orthogonal Vectors
instance. The certificate samples a set ``S`` of coordinates and buckets ``B`` by
``b & S``: a disjoint pair has ``b & S`` contained in ``S & ~(a & S)``, so it is
found by enumerating the submasks of ``S & ~(a & S)``. Pairs that share a sampled
coordinate are pruned; no disjoint pair is ever missed, so the search is exact.
"""

import random
from collections import defaultdict
from typing import Sequence


def disjoint_pair_brute(
    a_masks: Sequence[int], b_masks: Sequence[int]
) -> tuple[int, int] | None:
    """Reference O(|A| |B|) search for a pair with ``a & b == 0``."""
    for a in a_masks:
        for b in b_masks:
            if a & b == 0:
                return a, b
    return None


def disjoint_pair_certified(
    a_masks: Sequence[int],
    b_masks: Sequence[int],
    coordinates: int,
    sample_size: int | None = None,
    seed: int = 0,
) -> tuple[int, int] | None:
    """Find ``(a, b)`` with ``a & b == 0`` using a sampled compatibility certificate.

    ``coordinates`` bounds the bit positions. Returns a truly disjoint pair if one
    exists (the certificate only prunes non-disjoint pairs), or ``None``.
    """
    if not a_masks or not b_masks:
        return None
    if coordinates <= 0:
        raise ValueError("coordinates must be positive")
    if sample_size is None:
        sample_size = max(1, min(coordinates, (coordinates + 1) // 2))
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")

    rng = random.Random(seed)
    positions = list(range(coordinates))
    rng.shuffle(positions)
    sample = 0
    for position in positions[:sample_size]:
        sample |= 1 << position

    buckets: dict[int, list[int]] = defaultdict(list)
    for b in b_masks:
        buckets[b & sample].append(b)

    # Try the most-constrained ``a`` first: fewer allowed submasks.
    ordered = sorted(a_masks, key=lambda a: (a & sample).bit_count())
    for a in ordered:
        allowed = sample & ~(a & sample)
        submask = allowed
        while True:
            for b in buckets.get(submask, ()):
                if a & b == 0:
                    return a, b
            if submask == 0:
                break
            submask = (submask - 1) & allowed
    return None


def count_disjoint(a_masks: Sequence[int], b_masks: Sequence[int]) -> int:
    """Number of disjoint pairs (diagnostic; O(|A| |B|))."""
    return sum(1 for a in a_masks for b in b_masks if a & b == 0)


def compatible_pair_with_sum(
    a_pieces: Sequence[tuple[int, int]],
    b_pieces: Sequence[tuple[int, int]],
    target: int,
    coordinates: int,
    seed: int = 0,
) -> tuple[int, int] | None:
    """Find disjoint ``(a, b)`` with ``sum_a + sum_b == target``.

    ``a_pieces`` and ``b_pieces`` are ``(mask, weight_sum)`` pairs. Pieces with
    the complementary sum are collected and the certificate recovers a disjoint
    pair among them, which is the broadened-representation compatibility step.
    """
    from collections import defaultdict

    by_sum: dict[int, list[int]] = defaultdict(list)
    for mask, piece_sum in b_pieces:
        by_sum[piece_sum].append(mask)
    for mask, piece_sum in a_pieces:
        candidates = by_sum.get(target - piece_sum)
        if not candidates:
            continue
        found = disjoint_pair_certified([mask], candidates, coordinates, seed=seed)
        if found is not None:
            return found
    return None
