"""Exact three-block reduction for signed-integer subset sum.

Splitting the input into three blocks reduces Subset Sum to three-set 3SUM.
This module deliberately implements the direct quadratic merge: it formalizes
the reduction and provides a reference witness solver, rather than claiming a
new subquadratic algorithm for the structured 3SUM instance.
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class ThreeBlockResult:
    indices: tuple[int, ...] | None
    states: int

    @property
    def feasible(self) -> bool:
        return self.indices is not None


def _validate(values: Sequence[int], target: int) -> tuple[int, ...]:
    values = tuple(values)
    if type(target) is not int or any(type(value) is not int for value in values):
        raise TypeError("values and target must be Python integers")
    return values


def _entries(values: tuple[int, ...], offset: int) -> list[tuple[int, int]]:
    entries = [(0, 0)]
    for local, value in enumerate(values):
        bit = 1 << (offset + local)
        entries += [(total + value, mask | bit) for total, mask in entries]
    return entries


def three_block_entries(values: Sequence[int]) -> tuple[list[tuple[int, int]], ...]:
    """Enumerate the three block subset-sum lists with global masks."""
    values = tuple(values)
    n = len(values)
    first = n // 3
    second = (2 * n) // 3
    return (
        _entries(values[:first], 0),
        _entries(values[first:second], first),
        _entries(values[second:], second),
    )


def solve_three_block(values: Sequence[int], target: int) -> ThreeBlockResult:
    """Solve the reduction by a direct O*(2^(2n/3)) 3SUM merge.

    The method is an executable specification for future structured-3SUM
    accelerators.  It is not a claimed improvement over meet-in-the-middle.
    """
    values = _validate(values, target)
    first, second, third = three_block_entries(values)
    table = {total: mask for total, mask in third}
    states = len(first) + len(second) + len(third)
    for left_total, left_mask in first:
        for middle_total, middle_mask in second:
            states += 1
            right_mask = table.get(target - left_total - middle_total)
            if right_mask is not None:
                mask = left_mask | middle_mask | right_mask
                return ThreeBlockResult(
                    tuple(i for i in range(len(values)) if mask >> i & 1), states
                )
    return ThreeBlockResult(None, states)
