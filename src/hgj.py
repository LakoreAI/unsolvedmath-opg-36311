"""Howgrave-Graham-Joux representation search for hard knapsacks.

Ports the representation + modular-filter mechanism of Howgrave-Graham-Joux
(EUROCRYPT 2010) and Becker-Coron-Joux (EUROCRYPT 2011), following the
construction recalled in ePrint 2011/474, Sect. 2.2.

A solution x in {0,1}^n of Hamming weight ~n/2 is represented as y + z with
y, z in {0,1}^n disjoint, each of weight n/4. For a chosen modulus 2^m and a
residue R, the algorithm enumerates

    Y = { y : |y| = n/4, a.y = R        (mod 2^m) }
    Z = { z : |z| = n/4, a.z = target-R (mod 2^m) }

and matches y + z = target with y, z disjoint. A solution has ~2^(n/2)
balanced representations and M = 2^(n/2) residues, so a random residue keeps
about one, which is why a few random residues suffice.

This is the heuristic / average-case mechanism. The sub-knapsack enumeration
here uses a balanced meet-in-the-middle, costing C(n/2, n/8) ~ 2^(0.4057n) per
half. That already beats the 2^(n/2) meet-in-the-middle on random instances,
but it is *not* the optimized 2^(0.291n) recursion of BCJ, which needs nested
sub-solvers and weight balancing that this port does not implement.
"""

import math
import random
from dataclasses import dataclass
from itertools import combinations
from typing import Sequence

from src.compatibility import compatible_pair_with_sum


@dataclass(frozen=True)
class HgjResult:
    indices: tuple[int, ...] | None
    enumerated: int
    residues_tried: int

    @property
    def feasible(self) -> bool:
        return self.indices is not None


def _subsets_fixed_weight(block: tuple[int, ...], weight: int):
    """Yield (sum, local_mask) for all ``weight``-subsets of ``block``."""
    for comb in combinations(range(len(block)), weight):
        total = 0
        mask = 0
        for i in comb:
            total += block[i]
            mask |= 1 << i
        yield total, mask


def weight_residue_subsets(
    values: Sequence[int], weight: int, modulus: int, residue: int
) -> list[tuple[int, int]]:
    """All ``weight``-subsets with sum = ``residue`` mod ``modulus``.

    Balanced split: exactly ``weight//2`` elements from each half. Returns
    (sum, global_mask) pairs. Work is C(n/2, weight/2) per half.
    """
    values = tuple(values)
    n = len(values)
    k = n // 2
    left_w = weight // 2
    right_w = weight - left_w
    if not (0 <= left_w <= k and 0 <= right_w <= n - k):
        return []

    right_by_residue: dict[int, list[tuple[int, int]]] = {}
    for total, mask in _subsets_fixed_weight(values[k:], right_w):
        right_by_residue.setdefault(total % modulus, []).append((total, mask))

    out: list[tuple[int, int]] = []
    for total, mask in _subsets_fixed_weight(values[:k], left_w):
        need = (residue - total) % modulus
        for rtotal, rmask in right_by_residue.get(need, ()):
            out.append((total + rtotal, mask | (rmask << k)))
    return out


def enumerated_size(n: int, weight: int) -> int:
    """Number of fixed-weight subsets enumerated by the balanced split."""
    left_w = weight // 2
    return 2 * math.comb(n // 2, left_w)


def hgj_search(
    values: Sequence[int],
    target: int,
    weight: int | None = None,
    modulus_bits: int | None = None,
    residues: int = 8,
    seed: int = 0,
    certificate: bool = False,
    modulus: int | None = None,
) -> HgjResult:
    """Heuristic HGJ search for a Hamming-``weight`` solution.

    Tries ``residues`` random residues; each pass enumerates Y and Z and looks
    for a disjoint exact match. ``weight`` defaults to n//2. With
    ``certificate=True`` the disjoint (compatibility) step goes through the
    sparse-OV primitive of ``src.compatibility`` instead of the inline scan.
    ``modulus`` overrides the default power-of-two filter modulus (a prime
    avoids the structure of inputs whose low bits are degenerate).
    """
    values = tuple(values)
    n = len(values)
    if weight is None:
        weight = n // 2
    block_weight = weight - weight // 2  # n/4 for a balanced solution
    if modulus_bits is None:
        # Target M ~ number of balanced representations, C(n/4, n/8)^2.
        if n % 8 == 0:
            representations = math.comb(n // 4, n // 8) ** 2
            modulus_bits = max(1, representations.bit_length() - 1)
        else:
            modulus_bits = max(1, n // 2)
    if modulus is None:
        modulus = 1 << modulus_bits
    rng = random.Random(seed)

    per_attempt = enumerated_size(n, block_weight)
    enumerated = 0
    tried = 0
    for _ in range(residues):
        tried += 1
        r = rng.randrange(modulus)
        y_list = weight_residue_subsets(values, block_weight, modulus, r)
        z_list = weight_residue_subsets(
            values, block_weight, modulus, (target - r) % modulus
        )
        enumerated += per_attempt
        pair: tuple[int, int] | None = None
        if certificate:
            pair = compatible_pair_with_sum(
                [(mask, total) for total, mask in y_list],
                [(mask, total) for total, mask in z_list],
                target,
                n,
                seed=seed,
            )
        else:
            z_table: dict[int, list[int]] = {}
            for total, mask in z_list:
                z_table.setdefault(total, []).append(mask)
            for total, mask in y_list:
                for zmask in z_table.get(target - total, ()):
                    if not mask & zmask:
                        pair = (mask, zmask)
                        break
                if pair is not None:
                    break
        if pair is not None:
            plus_mask, minus_mask = pair
            plus = tuple(i for i in range(n) if plus_mask >> i & 1)
            minus = tuple(i for i in range(n) if minus_mask >> i & 1)
            return HgjResult(plus + minus, enumerated, tried)
    return HgjResult(None, enumerated, tried)


def balanced_probability(n: int, weight: int) -> float:
    """Chance a random permutation puts a weight-``weight`` support balanced.

    The sub-solver sees a solution only if exactly ``weight // 2`` of its
    elements lie in each half (``weight`` even); for a uniformly random
    permutation this is ``C(n/2, w/2)^2 / C(n, w)``, which is ``Theta(1/sqrt(n))``
    at ``w = n/2`` -- polynomial, not exponential. Odd ``weight`` or odd ``n``
    are rounded to the nearest balanced split.
    """
    left = n // 2
    right = n - left
    want = weight // 2
    if not (0 <= want <= left and 0 <= weight - want <= right):
        return 0.0
    return (
        math.comb(left, want) * math.comb(right, weight - want) / math.comb(n, weight)
    )


def hgj_permuted_search(
    values: Sequence[int],
    target: int,
    weight: int | None = None,
    permutations: int = 8,
    residues: int = 8,
    seed: int = 0,
    modulus: int | None = None,
    certificate: bool = False,
) -> HgjResult:
    """``hgj_search`` retried over random permutations of the input.

    The balanced sub-solver is incomplete on a fixed order (it needs exactly
    ``weight // 2`` support elements in each half). Permuting the values
    repairs this with probability ``balanced_probability(n, weight)`` per
    permutation, so ``O(sqrt(n))`` permutations suffice for ``weight = n/2``.
    Indices in the result refer to the original order.
    """
    values = tuple(values)
    n = len(values)
    rng = random.Random(seed)
    enumerated = 0
    tried = 0
    for attempt in range(permutations):
        order = list(range(n))
        if attempt:  # first attempt keeps the natural order
            rng.shuffle(order)
        result = hgj_search(
            [values[i] for i in order],
            target,
            weight=weight,
            residues=residues,
            seed=seed + attempt,
            certificate=certificate,
            modulus=modulus,
        )
        enumerated += result.enumerated
        tried += result.residues_tried
        if result.feasible:
            indices = tuple(sorted(order[i] for i in result.indices))
            return HgjResult(indices, enumerated, tried)
    return HgjResult(None, enumerated, tried)
