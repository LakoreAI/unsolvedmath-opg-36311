"""Exact Equal-Subset-Sum and Pigeonhole Equal-Subset-Sum baselines.

Equal-Subset-Sum (ESS): given integers w_1..w_n, find two distinct subsets with
equal sum, i.e. a nonzero c in {-1,0,1}^n with sum c_i w_i = 0.
Pigeonhole ESS (PESS): the same, under the promise sum_i w_i < 2^n - 1, which
guarantees such a pair exists.

The general ESS baseline enumerates signed half-sums, costing O*(3^(n/2)). The
PESS solvers are binary search with meet-in-the-middle counting, O*(2^(n/2)),
and the Jin-Wu O*(2^(0.4n)) algorithm (arXiv:2403.19117): structured
counting when weights are near 2^(i-1), modular-bucket subsampling otherwise.
The O*(2^(n/3)) PESS bound (Jin-Williams-Zhang, ESA 2025) is not implemented.
"""

import argparse
from bisect import bisect_right
from dataclasses import asdict, dataclass
import json
import random
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


def _subset_entries(values: tuple[int, ...]) -> list[tuple[int, int]]:
    entries = [(0, 0)]
    for i, value in enumerate(values):
        entries += [(total + value, mask | (1 << i)) for total, mask in entries]
    return entries


def sample_modular_bucket(
    values: Sequence[int],
    modulus: int,
    residue: int,
    sample_size: int,
    seed: int = 0,
) -> tuple[int, ...]:
    """Uniformly sample distinct subset masks from one modular sum bucket.

    The DP counts subsets by residue, and backtracking a uniformly sampled
    rank produces a uniform subset without enumerating the bucket. The returned
    masks are occurrence-index masks. This is a building block for randomized
    ESS/PESS algorithms, not a complete fast PESS solver.
    """
    values = _validate(values)
    if type(modulus) is not int or modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    if type(residue) is not int:
        raise TypeError("residue must be an integer")
    if type(sample_size) is not int or sample_size < 0:
        raise ValueError("sample_size must be a nonnegative integer")
    if type(seed) is not int:
        raise TypeError("seed must be an integer")

    counts = _residue_counts(values, modulus)
    target_residue = residue % modulus
    bucket_size = counts[-1][target_residue]
    rng = random.Random(seed)
    ranks = _distinct_ranks(rng, bucket_size, min(sample_size, bucket_size))
    return tuple(
        _backtrack_rank(values, counts, modulus, target_residue, rank)
        for rank in sorted(ranks)
    )


def _residue_counts(values: tuple[int, ...], modulus: int) -> list[list[int]]:
    counts = [[0] * modulus for _ in range(len(values) + 1)]
    counts[0][0] = 1
    for i, value in enumerate(values, start=1):
        previous = counts[i - 1]
        current = previous.copy()
        for prior_residue, count in enumerate(previous):
            if count:
                current[(prior_residue + value) % modulus] += count
        counts[i] = current
    return counts


def _distinct_ranks(rng: random.Random, population: int, take: int) -> set[int]:
    ranks: set[int] = set()
    for upper in range(population - take, population):
        rank = rng.randrange(upper + 1)
        ranks.add(upper if rank in ranks else rank)
    return ranks


def _backtrack_rank(
    values: tuple[int, ...],
    counts: list[list[int]],
    modulus: int,
    residue: int,
    rank: int,
) -> int:
    mask = 0
    for i in range(len(values), 0, -1):
        skip_count = counts[i - 1][residue]
        if rank >= skip_count:
            rank -= skip_count
            mask |= 1 << (i - 1)
            residue = (residue - values[i - 1]) % modulus
    return mask


def bucket_collision(
    values: Sequence[int],
    modulus: int,
    residue: int,
    sample_size: int,
    seed: int = 0,
) -> EqualSumResult:
    """Look for two sampled masks in one modular bucket with equal exact sum.

    One round of the large-slack PESS step: masks agreeing mod p are hashed by
    their exact sum. Returns an infeasible result if no sampled pair collides.
    """
    values = _validate(values)
    masks = sample_modular_bucket(values, modulus, residue, sample_size, seed)
    seen: dict[int, int] = {}
    for mask in masks:
        total = sum(value for i, value in enumerate(values) if mask >> i & 1)
        other = seen.setdefault(total, mask)
        if other != mask:
            plus, minus = _witness(mask & ~other, other & ~mask, len(values))
            return EqualSumResult(plus, minus, len(masks))
    return EqualSumResult(None, None, len(masks))


def close_pairs(values: Sequence[int], k: int) -> tuple[tuple[int, int], ...]:
    """Disjoint distinct suffix pairs (X, Y) with |w(X) - w(Y)| <= w([k]).

    Masks use full index positions and only touch indices >= k. Each unordered
    pair appears once. This reference enumeration costs 2^(n-k) plus output;
    the poly-size, poly-time construction of Jin-Williams-Zhang is pending.
    """
    values = _validate(values)
    if type(k) is not int or not 0 <= k <= len(values):
        raise ValueError("k must be an integer in [0, n]")
    bound = sum(values[:k])
    suffix = [(total, mask << k) for total, mask in _subset_entries(values[k:])]
    suffix.sort()
    sums = [total for total, _ in suffix]
    pairs = set()
    for total, x_mask in suffix:
        for index in range(bisect_right(sums, total - bound - 1), len(sums)):
            other_total, y_mask = suffix[index]
            if other_total > total + bound:
                break
            x_only, y_only = x_mask & ~y_mask, y_mask & ~x_mask
            if x_only != y_only:
                pairs.add((min(x_only, y_only), max(x_only, y_only)))
    return tuple(sorted(pairs))


def lift_reduced_witness(
    k: int,
    x_mask: int,
    y_mask: int,
    plus: Sequence[int],
    minus: Sequence[int],
) -> tuple[int, int]:
    """Map a witness of (w_1..w_k, w(X) - w(Y)) to original plus/minus masks.

    Index k is the extra element: on the plus side it expands to X and adds Y
    to the minus side, and symmetrically on the minus side.
    """
    plus_mask = sum(1 << i for i in plus if i != k)
    minus_mask = sum(1 << i for i in minus if i != k)
    if k in plus:
        plus_mask |= x_mask
        minus_mask |= y_mask
    elif k in minus:
        plus_mask |= y_mask
        minus_mask |= x_mask
    return plus_mask, minus_mask


def close_pair_equal_subset_sum(
    values: Sequence[int],
    k: int,
    solver=equal_subset_sum,
) -> EqualSumResult:
    """Solve ESS on nonnegative weights via the prefix plus close-pair reduction.

    Complete: if a disjoint witness (A, B) is not inside [k], then
    X = A - [k] and Y = B - [k] are distinct, disjoint and close, so the reduced
    instance W_{X,Y} = (w_1..w_k, w(X) - w(Y)) is solvable, and since the prefix
    alone is not, every reduced witness uses index k and lifts to a valid one.
    """
    values = _validate(values)
    if any(value < 0 for value in values):
        raise ValueError("close-pair reduction needs nonnegative weights")
    prefix = solver(values[:k])
    states = prefix.states
    if prefix.feasible:
        return EqualSumResult(prefix.plus, prefix.minus, states)
    for x_mask, y_mask in close_pairs(values, k):
        difference = sum(v for i, v in enumerate(values) if x_mask >> i & 1) - sum(
            v for i, v in enumerate(values) if y_mask >> i & 1
        )
        reduced = solver(values[:k] + (difference,))
        states += reduced.states + 1
        if reduced.feasible:
            plus_mask, minus_mask = lift_reduced_witness(
                k, x_mask, y_mask, reduced.plus, reduced.minus
            )
            plus, minus = _witness(plus_mask, minus_mask, len(values))
            return EqualSumResult(plus, minus, states)
    return EqualSumResult(None, None, states)


def _next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def geometric_slack(sorted_values: Sequence[int]) -> int:
    """Least Delta with w_i - 2^(i-1) in [-i*Delta, Delta] for all i (1-based).

    For sorted distinct PESS weights obeying the prefix assumption, Jin-Wu
    Lemma 6 gives d <= Delta => this bound, so d >= geometric_slack, where d
    counts non-subset-sums in [0, 2^n).
    """
    slack = 0
    for i, value in enumerate(sorted_values, start=1):
        deviation = value - (1 << (i - 1))
        slack = max(slack, deviation, -(deviation // i))
    return slack


class StructuredCounter:
    """Exact #{S : w(S) <= T} for sorted positive weights (Jin-Wu Lemma 7).

    Weights beyond the split i* are treated as 2^j plus a measured deviation,
    so only O(1) suffix subsets need meet-in-the-middle counting over the
    prefix. Exact for every sorted instance; fast when the slack is small.
    """

    def __init__(self, sorted_values: Sequence[int]):
        values = _validate(sorted_values)
        n = len(values)
        deviations = [value - (1 << j) for j, value in enumerate(values)]
        split = n
        for i in range(n + 1):
            window = sum(values[:i]) + sum(abs(e) for e in deviations[i:])
            if window <= 1 << (i + 1):
                split = i
                break
        self.values = values
        self.split = split
        self.unit = 1 << split
        self.suffix_count = 1 << (n - split)
        self.prefix_total = sum(values[:split])
        self.high = sum(e for e in deviations[split:] if e > 0)
        self.low = sum(e for e in deviations[split:] if e < 0)
        half = split // 2
        self.half = half
        self.left = _subset_entries(values[:half])
        right = _subset_entries(values[half:split])
        self.right_sums = sorted(total for total, _ in right)
        self.right_masks: dict[int, list[int]] = {}
        for total, mask in right:
            self.right_masks.setdefault(total, []).append(mask)
        self.states = len(self.left) + len(right)

    def _suffix_sum(self, k: int) -> int:
        return sum(
            self.values[self.split + b] for b in range(k.bit_length()) if k >> b & 1
        )

    def _prefix_at_most(self, bound: int) -> int:
        self.states += len(self.left)
        return sum(bisect_right(self.right_sums, bound - s) for s, _ in self.left)

    def count_at_most(self, bound: int) -> int:
        full = (bound - self.prefix_total - self.high) // self.unit + 1
        full = min(max(full, 0), self.suffix_count)
        last = min((bound - self.low) // self.unit, self.suffix_count - 1)
        total = full << self.split
        for k in range(full, last + 1):
            total += self._prefix_at_most(bound - self._suffix_sum(k))
        return total

    def masks_with_sum(self, target: int, limit: int = 2) -> list[int]:
        first = max(0, -(-(target - self.prefix_total - self.high) // self.unit))
        last = min((target - self.low) // self.unit, self.suffix_count - 1)
        masks: list[int] = []
        for k in range(first, last + 1):
            remainder = target - self._suffix_sum(k)
            for left_sum, left_mask in self.left:
                self.states += 1
                for right_mask in self.right_masks.get(remainder - left_sum, ()):
                    masks.append(left_mask | right_mask << self.half | k << self.split)
                    if len(masks) == limit:
                        return masks
        return masks


def _structured_pess(sorted_values: tuple[int, ...]) -> tuple[int, int, int]:
    counter = StructuredCounter(sorted_values)
    low, high = 0, sum(sorted_values)
    while low < high:
        middle = (low + high) // 2
        inside = counter.count_at_most(middle) - counter.count_at_most(low - 1)
        if inside > middle - low + 1:
            high = middle
        else:
            low = middle + 1
    masks = counter.masks_with_sum(low)
    if len(masks) < 2:
        raise RuntimeError("pigeonhole interval contained no duplicate sum")
    return masks[0], masks[1], counter.states


def _random_prime(rng: random.Random, lower: int) -> int:
    while True:
        candidate = rng.randrange(lower, 2 * lower + 1)
        if candidate >= 2 and all(
            candidate % d for d in range(2, int(candidate**0.5) + 1)
        ):
            return candidate


def subsample_collision(
    sorted_values: Sequence[int], delta: int, j: int, rng: random.Random
) -> tuple[int | None, int | None, int]:
    """One Jin-Wu Lemma 5 round for level j, assuming d >= delta.

    Picks a random prime p in [P, 2P] and residue r, subsamples bucket B_r at
    rate alpha = 1/(2hk), and returns (mask, mask', cost); masks are None if
    no sampled pair collides.
    """
    values = _validate(sorted_values)
    n = len(values)
    h = 1 << (j + 1)
    m = max(1, -(-delta // (h * n)))
    scale = min(1.0, ((1 << n) / (h * m * m)) ** (2 / 3))
    lower = max(2, int(2 * m * scale))
    k = -(-m // (4 * lower))
    alpha = 1 / (2 * h * k)
    modulus = _random_prime(rng, lower)
    residue = rng.randrange(modulus)
    counts = _residue_counts(values, modulus)
    bucket_size = counts[-1][residue]
    take = rng.binomialvariate(bucket_size, alpha)
    cost = n * modulus + take
    seen: dict[int, int] = {}
    for rank in _distinct_ranks(rng, bucket_size, take):
        mask = _backtrack_rank(values, counts, modulus, residue, rank)
        total = sum(v for i, v in enumerate(values) if mask >> i & 1)
        other = seen.setdefault(total, mask)
        if other != mask:
            return other, mask, cost
    return None, None, cost


def jin_wu_pigeonhole_equal_subset_sum(
    values: Sequence[int], rounds: int | None = None, seed: int = 0
) -> EqualSumResult:
    """Jin-Wu O*(2^(0.4n)) PESS (arXiv:2403.19117), Las Vegas.

    After removing duplicate weights and applying the prefix reduction, the
    measured slack Delta* = geometric_slack satisfies d >= Delta*. The solver
    runs the cheaper of the exact structured binary search (~2^(i*/2), with
    2^(i*) = O(n^2 Delta*)) and Lemma 5 subsampling (~(2^(2n)/Delta*)^(1/3)),
    so min of the two is <= 2^(0.4n) up to poly(n). Failed sampling falls back
    to the exact branch, so the answer is always correct.
    """
    values = _validate(values)
    if any(value <= 0 for value in values):
        raise ValueError("PESS weights must be positive integers")
    if sum(values) >= (1 << len(values)) - 1:
        raise ValueError("not a PESS instance: sum(weights) must be < 2^n - 1")

    order = sorted(range(len(values)), key=values.__getitem__)
    for a, b in zip(order, order[1:]):
        if values[a] == values[b]:
            return EqualSumResult((a,), (b,), len(values))

    size = len(order)
    for i in range(1, len(order)):
        if sum(values[t] for t in order[:i]) < (1 << i) - 1:
            size = i
            break
    order = order[:size]
    sorted_values = tuple(values[t] for t in order)

    slack = geometric_slack(sorted_values)
    structured_cost = 1 << (StructuredCounter(sorted_values).split // 2)
    sampling_cost = (4**size / max(slack, 1)) ** (1 / 3)
    states = 0
    pair = None
    if sampling_cost < structured_cost:
        rng = random.Random(seed)
        for _ in range(4 * size if rounds is None else rounds):
            for j in range(size):
                first, second, cost = subsample_collision(sorted_values, slack, j, rng)
                states += cost
                if first is not None:
                    pair = first, second
                    break
            if pair is not None:
                break
    if pair is None:
        first, second, cost = _structured_pess(sorted_values)
        states += cost
    else:
        first, second = pair
    plus = tuple(sorted(order[i] for i in range(size) if (first & ~second) >> i & 1))
    minus = tuple(sorted(order[i] for i in range(size) if (second & ~first) >> i & 1))
    return EqualSumResult(plus, minus, states)


def randomized_pigeonhole_equal_subset_sum(
    values: Sequence[int], trials: int = 8, seed: int = 0
) -> EqualSumResult:
    """Las Vegas PESS: modular-bucket collision rounds, then exact fallback.

    Each round picks a random prime p in [P, 2P] with P ~ 2^(n/3), a random
    residue, and samples ~2^(n/3) masks from that bucket. This captures the
    large-slack regime only; without the close-pair reduction and small-slack
    structural case it is not a worst-case O*(2^(n/3)) algorithm, so failure
    falls back to the O*(2^(n/2)) solver and the answer is always correct.
    """
    values = _validate(values)
    if any(value <= 0 for value in values):
        raise ValueError("PESS weights must be positive integers")
    if sum(values) >= (1 << len(values)) - 1:
        raise ValueError("not a PESS instance: sum(weights) must be < 2^n - 1")
    if type(trials) is not int or trials < 0:
        raise ValueError("trials must be a nonnegative integer")

    rng = random.Random(seed)
    scale = 1 << max(1, -(-len(values) // 3))
    states = 0
    for _ in range(trials):
        modulus = _next_prime(rng.randrange(scale, 2 * scale + 1))
        result = bucket_collision(
            values,
            modulus,
            rng.randrange(modulus),
            scale,
            rng.randrange(1 << 30),
        )
        states += result.states + modulus * len(values)
        if result.feasible:
            return EqualSumResult(result.plus, result.minus, states)
    result = pigeonhole_equal_subset_sum(values)
    return EqualSumResult(result.plus, result.minus, states + result.states)


def pigeonhole_equal_subset_sum(values: Sequence[int]) -> EqualSumResult:
    """Find a PESS witness by binary search and meet-in-the-middle.

    Requires positive integer weights with sum(weights) < 2^n - 1. The
    pigeonhole invariant narrows an interval containing more subset sums than
    integers; each count query uses two half-sum lists. This deterministic
    baseline takes O*(2^(n/2)) time and space, not the randomized O*(2^(n/3))
    bound.
    """
    values = _validate(values)
    if any(value <= 0 for value in values):
        raise ValueError("PESS weights must be positive integers")
    total = sum(values)
    if total >= (1 << len(values)) - 1:
        raise ValueError("not a PESS instance: sum(weights) must be < 2^n - 1")

    midpoint = len(values) // 2
    left = _subset_entries(values[:midpoint])
    right = _subset_entries(values[midpoint:])
    right_sums = sorted(subset_sum for subset_sum, _ in right)
    states = [0]

    def count_at_most(bound: int) -> int:
        states[0] += len(left)
        return sum(bisect_right(right_sums, bound - left_sum) for left_sum, _ in left)

    low, high = 0, total
    while low < high:
        middle = (low + high) // 2
        count_in_interval = count_at_most(middle) - count_at_most(low - 1)
        if count_in_interval > middle - low + 1:
            high = middle
        else:
            low = middle + 1

    target = low
    right_masks: dict[int, list[int]] = {}
    for subset_sum, mask in right:
        masks = right_masks.setdefault(subset_sum, [])
        if len(masks) < 2:
            masks.append(mask)

    first_mask = None
    second_mask = None
    for left_sum, left_mask in left:
        states[0] += 1
        for right_mask in right_masks.get(target - left_sum, ()):
            combined_mask = left_mask | (right_mask << midpoint)
            if first_mask is None:
                first_mask = combined_mask
            elif combined_mask != first_mask:
                second_mask = combined_mask
                break
        if second_mask is not None:
            break

    if first_mask is None or second_mask is None:
        raise RuntimeError("pigeonhole interval contained no duplicate sum")

    plus_mask = first_mask & ~second_mask
    minus_mask = second_mask & ~first_mask
    plus, minus = _witness(plus_mask, minus_mask, len(values))
    return EqualSumResult(plus, minus, states[0])


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
