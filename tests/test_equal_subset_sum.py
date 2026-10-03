"""Differential checks for the Equal-Subset-Sum baselines."""

from itertools import product
import random
import unittest

from src.equal_subset_sum import (
    StructuredCounter,
    bucket_collision,
    close_pair_equal_subset_sum,
    close_pairs,
    equal_subset_sum,
    geometric_slack,
    jin_wu_pigeonhole_equal_subset_sum,
    lift_reduced_witness,
    pigeonhole_equal_subset_sum,
    randomized_pigeonhole_equal_subset_sum,
    sample_modular_bucket,
    subsample_collision,
)


def subset_sums(values):
    return [
        sum(v for i, v in enumerate(values) if mask >> i & 1)
        for mask in range(1 << len(values))
    ]


def pess_instances(rng, n, count):
    out = []
    while len(out) < count:
        kind = rng.randrange(3)
        if kind == 0:
            values = [rng.randrange(1, max(2, (1 << n) // n)) for _ in range(n)]
        elif kind == 1:
            values = [max(1, (1 << j) - rng.randrange(0, 3)) for j in range(n)]
        else:
            values = [rng.randrange(1, 4) for _ in range(n)]
        if sum(values) < (1 << n) - 1:
            out.append(values)
    return out


def oracle(values):
    for c in product((-1, 0, 1), repeat=len(values)):
        if any(c) and sum(ci * wi for ci, wi in zip(c, values)) == 0:
            return True
    return False


class EqualSubsetSumTests(unittest.TestCase):
    def check(self, values):
        expected = oracle(values)
        result = equal_subset_sum(values)
        self.assertEqual(result.feasible, expected, values)
        if result.feasible:
            plus, minus = set(result.plus), set(result.minus)
            self.assertTrue(plus or minus)
            self.assertNotEqual(plus, minus)
            self.assertTrue(plus.isdisjoint(minus))
            self.assertEqual(
                sum(values[i] for i in result.plus),
                sum(values[i] for i in result.minus),
            )

    def test_exhaustive_small(self):
        for n in range(5):
            for values in product((-2, 0, 3), repeat=n):
                self.check(list(values))

    def test_seeded_random(self):
        rng = random.Random(36311)
        for _ in range(250):
            values = [rng.randrange(-10, 11) for _ in range(rng.randrange(9))]
            self.check(values)

    def test_pigeonhole_promise(self):
        rng = random.Random(7)
        for n in (4, 6, 8, 10):
            for _ in range(25):
                bound = max(2, (1 << n) // (2 * n))
                values = [rng.randrange(1, bound) for _ in range(n)]
                if sum(values) >= (1 << n) - 1:
                    continue
                result = pigeonhole_equal_subset_sum(values)
                self.assertTrue(result.feasible)
                self.assertEqual(
                    sum(values[i] for i in result.plus),
                    sum(values[i] for i in result.minus),
                )

    def test_pigeonhole_binary_search_exhaustive(self):
        for n in range(2, 5):
            for values in product(range(1, 8), repeat=n):
                if sum(values) >= (1 << n) - 1:
                    continue
                result = pigeonhole_equal_subset_sum(values)
                self.assertTrue(result.feasible)
                self.assertTrue(set(result.plus).isdisjoint(result.minus))
                self.assertTrue(result.plus or result.minus)
                self.assertEqual(
                    sum(values[i] for i in result.plus),
                    sum(values[i] for i in result.minus),
                )

    def test_promise_enforced(self):
        with self.assertRaises(ValueError):
            pigeonhole_equal_subset_sum([1 << 10, 1 << 10])
        with self.assertRaises(ValueError):
            pigeonhole_equal_subset_sum([0, 1])
        with self.assertRaises(ValueError):
            pigeonhole_equal_subset_sum([-1, 2])

    def test_modular_bucket_sampling(self):
        values = [1, 2, 3, 6]
        modulus = 4
        residue = 1
        expected = {
            mask
            for mask in range(1 << len(values))
            if sum(value for i, value in enumerate(values) if mask >> i & 1) % modulus
            == residue
        }
        sampled = sample_modular_bucket(
            values, modulus, residue, sample_size=len(expected), seed=17
        )
        self.assertEqual(set(sampled), expected)
        self.assertEqual(len(sampled), len(expected))
        self.assertEqual(
            sampled,
            sample_modular_bucket(
                values, modulus, residue, sample_size=len(expected), seed=17
            ),
        )

    def test_modular_bucket_sample_is_unique_and_valid(self):
        values = [-3, 2, 7, 8, 11]
        modulus = 5
        residue = -1
        sampled = sample_modular_bucket(values, modulus, residue, 3, seed=9)
        self.assertEqual(len(set(sampled)), len(sampled))
        for mask in sampled:
            total = sum(value for i, value in enumerate(values) if mask >> i & 1)
            self.assertEqual(total % modulus, residue % modulus)

    def assert_witness(self, values, result):
        self.assertTrue(result.feasible)
        self.assertTrue(result.plus or result.minus)
        self.assertTrue(set(result.plus).isdisjoint(result.minus))
        self.assertEqual(
            sum(values[i] for i in result.plus),
            sum(values[i] for i in result.minus),
        )

    def test_bucket_collision_finds_heavy_collisions(self):
        values = [1] * 8
        result = bucket_collision(values, 3, 1, 8, seed=5)
        self.assert_witness(values, result)

    def test_bucket_collision_reports_no_collision(self):
        values = [1, 2, 4, 8]
        self.assertFalse(bucket_collision(values, 3, 0, 16).feasible)

    def test_randomized_pigeonhole_always_valid(self):
        rng = random.Random(36311)
        for n in (4, 6, 8, 10, 12):
            for trial in range(20):
                bound = max(2, (1 << n) // (2 * n))
                values = [rng.randrange(1, bound) for _ in range(n)]
                if sum(values) >= (1 << n) - 1:
                    continue
                for trials in (0, 4):
                    result = randomized_pigeonhole_equal_subset_sum(
                        values, trials=trials, seed=trial
                    )
                    self.assert_witness(values, result)

    def test_randomized_pigeonhole_promise(self):
        with self.assertRaises(ValueError):
            randomized_pigeonhole_equal_subset_sum([1 << 10, 1 << 10])
        with self.assertRaises(ValueError):
            randomized_pigeonhole_equal_subset_sum([1, 1], trials=-1)

    def test_close_pairs_match_definition(self):
        values = [1, 2, 3, 5, 9, 14]
        for k in range(len(values) + 1):
            bound = sum(values[:k])
            expected = set()
            for c in product((-1, 0, 1), repeat=len(values) - k):
                x = sum(1 << (k + i) for i, ci in enumerate(c) if ci == 1)
                y = sum(1 << (k + i) for i, ci in enumerate(c) if ci == -1)
                diff = sum(ci * v for ci, v in zip(c, values[k:]))
                if any(c) and abs(diff) <= bound:
                    expected.add((min(x, y), max(x, y)))
            self.assertEqual(set(close_pairs(values, k)), expected, k)

    def test_lift_reduced_witness(self):
        self.assertEqual(lift_reduced_witness(2, 0b100, 0b1000, (2,), (0,)), (4, 9))
        self.assertEqual(lift_reduced_witness(2, 0b100, 0b1000, (1,), (2,)), (10, 4))

    def test_close_pair_reduction_matches_oracle(self):
        rng = random.Random(2025)
        cases = [list(v) for v in product((0, 1, 3, 4), repeat=3)]
        cases += [
            [rng.randrange(1, 40) for _ in range(rng.randrange(1, 8))]
            for _ in range(60)
        ]
        for values in cases:
            expected = oracle(values)
            for k in range(len(values) + 1):
                result = close_pair_equal_subset_sum(values, k)
                self.assertEqual(result.feasible, expected, (values, k))
                if expected:
                    self.assert_witness(values, result)

    def test_close_pair_arguments(self):
        with self.assertRaises(ValueError):
            close_pair_equal_subset_sum([1, -2], 1)
        with self.assertRaises(ValueError):
            close_pairs([1, 2], 3)

    def test_structured_counter_is_exact(self):
        rng = random.Random(11)
        for _ in range(80):
            n = rng.randrange(1, 9)
            if rng.random() < 0.5:
                values = sorted(rng.randrange(1, 1 << (n + 1)) for _ in range(n))
            else:
                values = [max(1, (1 << j) + rng.randrange(-3, 4)) for j in range(n)]
                values.sort()
            sums = subset_sums(values)
            counter = StructuredCounter(values)
            for bound in range(-1, sum(values) + 2):
                expected = sum(1 for s in sums if s <= bound)
                self.assertEqual(counter.count_at_most(bound), expected, values)
            target = rng.choice(sums)
            masks = counter.masks_with_sum(target, limit=3)
            self.assertEqual(len(masks), min(3, sums.count(target)))
            self.assertEqual(len(set(masks)), len(masks))
            for mask in masks:
                self.assertEqual(sums[mask], target)

    def test_lemma6_slack_lower_bounds_d(self):
        rng = random.Random(6)
        checked = 0
        for n in range(3, 11):
            for _ in range(10):
                values = [1, 2] + [(1 << j) + rng.randrange(3) for j in range(2, n)]
                values[-1] -= sum(values[:-1]) - (1 << (n - 1)) + 2 + rng.randrange(n)
                if values[-1] <= values[-2] or sum(values) >= (1 << n) - 1:
                    continue
                if any(sum(values[:i]) < (1 << i) - 1 for i in range(1, n)):
                    continue
                present = set(subset_sums(values))
                d = sum(1 for t in range(1 << n) if t not in present)
                self.assertGreaterEqual(d, geometric_slack(values), values)
                checked += 1
        self.assertGreater(checked, 20)

    def test_jin_wu_always_valid(self):
        rng = random.Random(36311)
        for n in range(2, 13):
            for trial, values in enumerate(pess_instances(rng, n, 15)):
                for rounds in (0, None):
                    result = jin_wu_pigeonhole_equal_subset_sum(
                        values, rounds=rounds, seed=trial
                    )
                    self.assert_witness(values, result)

    def test_subsample_collision_witness(self):
        rng = random.Random(3)
        values = sorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        present = set(subset_sums(values))
        d = sum(1 for t in range(1 << len(values)) if t not in present)
        found = 0
        for _ in range(40):
            for j in range(len(values)):
                first, second, _ = subsample_collision(values, d, j, rng)
                if first is not None:
                    found += 1
                    self.assertNotEqual(first, second)
                    sums = subset_sums(values)
                    self.assertEqual(sums[first], sums[second])
        self.assertGreater(found, 0)

    def test_jin_wu_promise(self):
        with self.assertRaises(ValueError):
            jin_wu_pigeonhole_equal_subset_sum([1 << 10, 1 << 10])
        with self.assertRaises(ValueError):
            jin_wu_pigeonhole_equal_subset_sum([0, 1, 1])

    def test_modular_bucket_arguments(self):
        with self.assertRaises(ValueError):
            sample_modular_bucket([1], 0, 0, 1)
        with self.assertRaises(ValueError):
            sample_modular_bucket([1], 2, 0, -1)


if __name__ == "__main__":
    unittest.main()
