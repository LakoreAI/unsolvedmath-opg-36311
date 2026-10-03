"""Exact Equal-Subset-Sum and Pigeonhole Equal-Subset-Sum baselines.

Equal-Subset-Sum (ESS): given integers w_1..w_n, find two distinct subsets with
equal sum, i.e. a nonzero c in {-1,0,1}^n with sum c_i w_i = 0.
Pigeonhole ESS (PESS): the same, under the promise sum_i w_i < 2^n - 1, which
guarantees such a pair exists.

The meet-in-the-middle baseline here enumerates signed half-sums, costing
O*(3^(n/2)). It is a correct baseline, not the known O*(2^(n/3)) pigeonhole
algorithm (Jin-Williams-Zhang, ESA 2025); that algorithm needs the structural
F = sum_t max(0, count(t) - 1) machinery and is not reimplemented.
"""

import argparse
from dataclasses import asdict, dataclass
import json
from typing import Sequence


@dataclass(frozen=True)
class EqualSumResult:
    plus: tuple[int, ...] | None
    minus: tuple[int, ...] | None
    states: int

    @property
    def feasible(self) -> bool:
        return self.plus is not None


def _validate(values: Sequence[int]) -> tuple[int, ...]:
    values = tuple(values)
    if any(type(a) is not int for a in values):
        raise TypeError("values must be Python integers")
    return values


def _signed_entries(values: tuple[int, ...]) -> list[tuple[int, int, int]]:
    """All (signed sum, plus mask, minus mask) for one half; 3^len entries."""
    entries = [(0, 0, 0)]
    for i, a in enumerate(values):
        bit = 1 << i
        entries = (
            entries
            + [(s + a, p | bit, m) for s, p, m in entries]
            + [(s - a, p, m | bit) for s, p, m in entries]
        )
    return entries


def _witness(plus_mask: int, minus_mask: int, n: int) -> tuple[tuple[int, ...], ...]:
    plus = tuple(i for i in range(n) if plus_mask >> i & 1)
    minus = tuple(i for i in range(n) if minus_mask >> i & 1)
    return plus, minus


def equal_subset_sum(values: Sequence[int]) -> EqualSumResult:
    """Find two distinct equal-sum subsets by signed meet-in-the-middle.

    Sound by construction: every returned pair has equal subset sums. Complete:
    any nonzero zero-sum coefficient vector has a left and a right part that the
    hash matches. Works for negative entries; returns disjoint index tuples.
    """
    values = _validate(values)
    n = len(values)
    k = n // 2
    left = _signed_entries(values[:k])
    right = _signed_entries(values[k:])

    states = len(left) + len(right)

    # A zero-sum relation contained entirely in one half is already a witness.
    for entries, offset in ((left, 0), (right, k)):
        for s, p, m in entries:
            if s == 0 and (p or m):
                plus, minus = _witness(p << offset, m << offset, n)
                return EqualSumResult(plus, minus, states)

    table: dict[int, tuple[int, int]] = {}
    for s, p, m in left:
        table.setdefault(s, (p, m))
    for s, p, m in right:
        match = table.get(-s)
        if match is None:
            continue
        lp, lm = match
        plus_mask = lp | (p << k)
        minus_mask = lm | (m << k)
        if plus_mask or minus_mask:
            plus, minus = _witness(plus_mask, minus_mask, n)
            return EqualSumResult(plus, minus, states)
    return EqualSumResult(None, None, states)


def pigeonhole_equal_subset_sum(values: Sequence[int]) -> EqualSumResult:
    """ESS under the PESS promise sum|w_i| < 2^n - 1 (solution guaranteed).

    Uses the same O*(3^(n/2)) baseline; the promise is documented so callers do
    not mistake this for the O*(2^(n/3)) algorithm.
    """
    values = _validate(values)
    total = sum(abs(a) for a in values)
    if total >= (1 << len(values)) - 1:
        raise ValueError("not a PESS instance: sum|w_i| must be < 2^n - 1")
    return equal_subset_sum(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--values", nargs="*", type=int, required=True)
    parser.add_argument("--pigeonhole", action="store_true")
    args = parser.parse_args()
    solver = pigeonhole_equal_subset_sum if args.pigeonhole else equal_subset_sum
    result = solver(args.values)
    print(json.dumps({**asdict(result), "feasible": result.feasible}))


if __name__ == "__main__":
    main()
