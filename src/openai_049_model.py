"""Small reference components from OpenAI's October 2026 Subset Sum preprint.

This is deliberately *not* an implementation of its ``O(2^(0.49n))``
algorithm. The full result combines the isolation reduction below with a
Fourier checksum estimator, filtered high/low-digit data structures, and a
randomized modular-alias extractor. Those procedures are not reproduced here.

The shared-mask construction models the Section 5 compatibility relation: two
records represent a subset precisely when their masks in the shared block are
disjoint. It is a small oracle for developing an alias extractor and carries
no exponent claim.
"""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class IsolatedInstance:
    """The polynomial family of targets from equation (2.1)."""

    weights: tuple[int, ...]
    targets: tuple[int, ...]
    scale: int


@dataclass(frozen=True)
class SharedMaskRecord:
    """A side subset and the subset it selects from the shared block."""

    side_mask: int
    shared_mask: int
    total: int


def isolation_family(
    values: Sequence[int], target: int, tie_weights: Sequence[int]
) -> IsolatedInstance:
    """Build the paper's exact isolation family for positive integer inputs.

    ``tie_weights`` must lie in ``[1, N0]`` for a power of two ``N0`` satisfying
    ``12n <= N0 < 24n``. Every solution to an emitted target is a solution to
    the original instance; an original solution is represented by its tie sum.
    """
    values = tuple(values)
    tie_weights = tuple(tie_weights)
    if len(values) != len(tie_weights) or not values or target < 0:
        raise ValueError("need nonempty positive values and one tie weight per value")
    if any(type(x) is not int or x <= 0 for x in values) or any(
        type(u) is not int for u in tie_weights
    ):
        raise TypeError("values must be positive integers and ties must be integers")
    n0 = 1
    while n0 < 12 * len(values):
        n0 <<= 1
    if any(not 1 <= u <= n0 for u in tie_weights):
        raise ValueError("tie weights must be in [1, N0]")
    scale = 1 + len(values) * n0
    return IsolatedInstance(
        tuple(scale * a + u for a, u in zip(values, tie_weights)),
        tuple(scale * target + s for s in range(len(values) * n0 + 1)),
        scale,
    )


def masks_compatible(left: SharedMaskRecord, right: SharedMaskRecord) -> bool:
    """Section 5 compatibility: records form a true subset iff masks are disjoint."""
    return not left.shared_mask & right.shared_mask


def shared_mask_records(
    values: Sequence[int], side: Sequence[int], shared: Sequence[int]
) -> list[SharedMaskRecord]:
    """Enumerate the paper's unfiltered record shape for one side."""
    values = tuple(values)
    side = tuple(side)
    shared = tuple(shared)
    if (
        len(set(side)) != len(side)
        or len(set(shared)) != len(shared)
        or set(side) & set(shared)
        or any(i < 0 or i >= len(values) for i in side + shared)
    ):
        raise ValueError("side and shared must be disjoint valid indices")
    out: list[SharedMaskRecord] = []
    for side_bits in range(1 << len(side)):
        side_total = sum(values[i] for j, i in enumerate(side) if side_bits >> j & 1)
        side_mask = sum(1 << side[j] for j in range(len(side)) if side_bits >> j & 1)
        for shared_bits in range(1 << len(shared)):
            shared_total = sum(
                values[i] for j, i in enumerate(shared) if shared_bits >> j & 1
            )
            out.append(SharedMaskRecord(side_mask, shared_bits, side_total + shared_total))
    return out


def recover_shared_mask_subset(
    values: Sequence[int],
    target: int,
    left: Sequence[int],
    right: Sequence[int],
    shared: Sequence[int],
) -> tuple[int, ...] | None:
    """Reference recovery using shared-mask compatibility for small inputs."""
    values = tuple(values)
    blocks = tuple(left) + tuple(right) + tuple(shared)
    if sorted(blocks) != list(range(len(values))):
        raise ValueError("left, right, and shared must partition the input indices")
    right_by_total: dict[int, list[SharedMaskRecord]] = {}
    for record in shared_mask_records(values, right, shared):
        right_by_total.setdefault(record.total, []).append(record)
    for first in shared_mask_records(values, left, shared):
        for second in right_by_total.get(target - first.total, ()):
            if masks_compatible(first, second):
                mask = first.side_mask | second.side_mask
                for j, index in enumerate(shared):
                    if (first.shared_mask | second.shared_mask) >> j & 1:
                        mask |= 1 << index
                return tuple(i for i in range(len(values)) if mask >> i & 1)
    return None
