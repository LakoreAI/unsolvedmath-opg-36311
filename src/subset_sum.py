"""Exact signed-integer subset sum; no claim to solve OPG-36311's open bound.

Run without ML dependencies: python3 -m src.subset_sum --values 3 -2 7 --target 5
"""

import argparse
from bisect import bisect_left
from dataclasses import asdict, dataclass
import heapq
import json
from typing import Iterator, Sequence


@dataclass(frozen=True)
class Result:
    algorithm: str
    indices: tuple[int, ...] | None
    states: int

    @property
    def feasible(self) -> bool:
        return self.indices is not None


def _validate(values: Sequence[int], target: int) -> tuple[int, ...]:
    values = tuple(values)
    if type(target) is not int or any(type(a) is not int for a in values):
        raise TypeError("values and target must be Python integers")
    return values


def _entries(values: tuple[int, ...]) -> list[tuple[int, int]]:
    entries = [(0, 0)]
    for i, a in enumerate(values):
        entries += [(s + a, mask | (1 << i)) for s, mask in entries]
    return entries


def meet_in_middle(values: Sequence[int], target: int) -> Result:
    """Deterministic O*(2^(n/2)) solver with an occurrence-index witness.

    Sorting and binary search avoid assuming constant-time hash operations.
    Bit arithmetic and witness materialization contribute polynomial factors.
    """
    values = _validate(values, target)
    k = len(values) // 2
    left = _entries(values[:k])
    right = sorted(_entries(values[k:]))
    totals = [s for s, _ in right]
    for u, left_mask in left:
        pos = bisect_left(totals, target - u)
        if pos < len(right) and totals[pos] == target - u:
            mask = left_mask | (right[pos][1] << k)
            indices = tuple(i for i in range(len(values)) if mask & (1 << i))
            return Result("mitm", indices, len(left) + len(right))
    return Result("mitm", None, len(left) + len(right))


def _ascending_pairs(
    first: list[tuple[int, int]],
    second: list[tuple[int, int]],
    pops: list[int],
) -> Iterator[tuple[int, int]]:
    """Stream ``first[i] + second[j]`` in nondecreasing order.

    ``first`` and ``second`` are sorted by sum. Merging ``len(first)`` sorted
    lists through a heap keeps only ``O(len(first))`` live entries, so the
    ``len(first) * len(second)`` pair set is never materialized. ``pops`` counts
    yielded pairs for work reporting.
    """
    heap = [(first[i][0] + second[0][0], i, 0) for i in range(len(first))]
    heapq.heapify(heap)
    while heap:
        total, i, j = heapq.heappop(heap)
        pops[0] += 1
        yield total, first[i][1] | second[j][1]
        if j + 1 < len(second):
            heapq.heappush(heap, (first[i][0] + second[j + 1][0], i, j + 1))


def _descending_pairs(
    first: list[tuple[int, int]],
    second: list[tuple[int, int]],
    pops: list[int],
) -> Iterator[tuple[int, int]]:
    """Stream ``first[i] + second[j]`` in nonincreasing order (max-heap)."""
    last = len(second) - 1
    heap = [(-(first[i][0] + second[last][0]), i, last) for i in range(len(first))]
    heapq.heapify(heap)
    while heap:
        neg, i, j = heapq.heappop(heap)
        pops[0] += 1
        yield -neg, first[i][1] | second[j][1]
        if j - 1 >= 0:
            heapq.heappush(heap, (-(first[i][0] + second[j - 1][0]), i, j - 1))


def schroeppel_shamir(values: Sequence[int], target: int) -> Result:
    """O*(2^(n/2))-time, O*(2^(n/4))-space exact solver with a witness.

    Four blocks of about ``n/4`` entries are enumerated and sorted (this is the
    ``2^(n/4)`` space). The ``2^(n/2)`` pair sums of blocks 0+1 and blocks 2+3
    are then compared by a two-pointer sweep over two lazily heap-generated
    streams, so the pair lists are never stored. A match yields a witness by
    OR-ing the two global occurrence masks. Constant factors here exceed the
    sorted meet-in-the-middle matcher; the gain is space.
    """
    values = _validate(values, target)
    n = len(values)
    block = n // 4
    cuts = (0, block, 2 * block, 3 * block, n)
    offsets = (0, block, 2 * block, 3 * block)
    blocks = [
        sorted(
            (s, mask << offset) for s, mask in _entries(values[cuts[i] : cuts[i + 1]])
        )
        for i, offset in enumerate(offsets)
    ]
    pops = [0]
    left = _ascending_pairs(blocks[0], blocks[1], pops)
    right = _descending_pairs(blocks[2], blocks[3], pops)
    low = next(left, None)
    high = next(right, None)
    while low is not None and high is not None:
        total = low[0] + high[0]
        if total == target:
            mask = low[1] | high[1]
            indices = tuple(i for i in range(n) if mask >> i & 1)
            return Result("ss", indices, pops[0])
        if total < target:
            low = next(left, None)
        else:
            high = next(right, None)
    return Result("ss", None, pops[0])


def bounded_dp(values: Sequence[int], target: int) -> Result:
    """Dense DP over [-W,W], W=sum(abs(a)), including negative integers.

    Uses two buffers so an item is never reused within its own iteration.
    O(n*(2W+1)) cell visits; storing index masks adds polynomial bit costs.
    Only call this method when the numeric width fits available memory.
    """
    values = _validate(values, target)
    width = sum(abs(a) for a in values)
    if abs(target) > width:
        return Result("dp", None, 0)
    reachable: list[int | None] = [None] * (2 * width + 1)
    reachable[width] = 0
    for i, a in enumerate(values):
        updated = reachable.copy()
        for pos, mask in enumerate(reachable):
            new_pos = pos + a
            if mask is not None and 0 <= new_pos < len(updated):
                if updated[new_pos] is None:
                    updated[new_pos] = mask | (1 << i)
        reachable = updated
    mask = reachable[target + width]
    indices = (
        None
        if mask is None
        else tuple(i for i in range(len(values)) if mask & (1 << i))
    )
    return Result("dp", indices, len(values) * (2 * width + 1))


def solve(values: Sequence[int], target: int, method: str = "auto") -> Result:
    """Dispatch to a solver. ``ss`` is explicit only; ``auto`` picks DP or MITM.

    The automatic choice compares operation-count estimates and makes no
    optimality claim. Schroeppel-Shamir has the same time order as MITM with
    lower space but a larger constant, so it is selected explicitly.
    """
    values = _validate(values, target)
    if method not in {"auto", "mitm", "dp", "ss"}:
        raise ValueError("method must be auto, mitm, dp, or ss")
    if method == "auto":
        n = len(values)
        dp_work = max(n, 1) * (2 * sum(abs(a) for a in values) + 1)
        mitm_work = max(n, 1) * ((1 << (n // 2)) + (1 << ((n + 1) // 2)))
        method = "dp" if dp_work <= mitm_work else "mitm"
    if method == "dp":
        return bounded_dp(values, target)
    if method == "ss":
        return schroeppel_shamir(values, target)
    return meet_in_middle(values, target)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--values", nargs="*", type=int, required=True)
    parser.add_argument("--target", type=int, required=True)
    parser.add_argument(
        "--method", choices=("auto", "mitm", "dp", "ss"), default="auto"
    )
    args = parser.parse_args()
    result = solve(args.values, args.target, args.method)
    print(json.dumps({**asdict(result), "feasible": result.feasible}))


if __name__ == "__main__":
    main()
