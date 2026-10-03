"""Dissection / generalized-birthday core for subset-sum research.

Wagner's k-tree algorithm for the modular four-sum problem: given four lists of
residues modulo 2^n, find one element from each list summing to 0 (mod 2^n).
The four-list case is the engine of the representation/dissection technique and
runs in O*(2^(n/3)) when each list holds about 2^(n/3) elements.

This is the average-case/heuristic core, not a worst-case subset-sum algorithm:
Wagner's list-balance analysis assumes random (or planted) lists, and the
reduction of {0,1} subset sum to this modular problem still requires the
representation machinery of Howgrave-Graham-Joux.
"""

from typing import Sequence


def _pairs_matching_zero(
    first: list[int], second: list[int], low_bits: int, modulus: int
) -> list[tuple[int, int, int]]:
    """All pairs with (a+b) = 0 mod 2^low_bits, returned as (high, ia, ib).

    ``high = ((a+b) mod modulus) >> low_bits``. Hashing the low residues keeps
    the work proportional to the number of matching pairs rather than |A|*|B|.
    """
    low = 1 << low_bits
    buckets: dict[int, list[int]] = {}
    for ib, vb in enumerate(second):
        buckets.setdefault(vb % low, []).append(ib)
    out: list[tuple[int, int, int]] = []
    for ia, va in enumerate(first):
        for ib in buckets.get((-va) % low, ()):
            out.append((((va + second[ib]) % modulus) >> low_bits, ia, ib))
    return out


def wagner_4sum_mod(
    lists: Sequence[Sequence[int]], modulus: int, filter_bits: int | None = None
) -> tuple[int, int, int, int] | None:
    """Find indices i0..i3 with sum(lists[t][it]) = 0 mod ``modulus``.

    ``modulus`` must be a power of two. ``filter_bits`` is the number of
    low-order bits filtered at the first merge (default: ~log2 of the smallest
    list, which balances the canonical 2^(n/3)-sized lists). Returns a witness
    tuple of indices, or ``None`` if the heuristic merge finds no match.
    """
    if len(lists) != 4:
        raise ValueError("expected exactly four lists")
    if modulus < 2 or modulus & (modulus - 1):
        raise ValueError("modulus must be a power of two")
    a, b, c, d = (list(x) for x in lists)
    n = modulus.bit_length() - 1

    if filter_bits is None:
        smallest = min(len(a), len(b), len(c), len(d))
        filter_bits = max(1, min(n - 1, smallest.bit_length() - 1))
    if not 0 < filter_bits < n:
        raise ValueError("filter_bits must satisfy 0 < filter_bits < n")

    left = _pairs_matching_zero(a, b, filter_bits, modulus)
    right = _pairs_matching_zero(c, d, filter_bits, modulus)
    half = 1 << (n - filter_bits)

    table: dict[int, tuple[int, int]] = {}
    for high, ia, ib in left:
        table.setdefault(high, (ia, ib))
    for high, ic, id_ in right:
        match = table.get((-high) % half)
        if match is not None:
            ia, ib = match
            return ia, ib, ic, id_
    return None


def verify_4sum(
    lists: Sequence[Sequence[int]], indices: Sequence[int], modulus: int
) -> bool:
    """Check that the chosen elements exist and sum to 0 modulo ``modulus``."""
    if indices is None or len(indices) != 4:
        return False
    total = 0
    for lst, idx in zip(lists, indices):
        if not 0 <= idx < len(lst):
            return False
        total += lst[idx]
    return total % modulus == 0
