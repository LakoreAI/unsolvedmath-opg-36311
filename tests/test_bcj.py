"""Differential checks for the broadened (BCJ) representation search."""

from itertools import product
import random
import unittest

from src.bcj import (
    broadened_subset_sum,
    compatible,
    enumerate_profile,
    reduce_common_factor,
    representation_count,
)


def oracle(values, target):
    return any(
        sum(v for v, bit in zip(values, mask) if bit) == target
        for mask in product((0, 1), repeat=len(values))
    )


class BcjTests(unittest.TestCase):
    def test_enumerate_profile_counts(self):
        pieces = list(enumerate_profile(6, 2, 1))
        # C(6,2) * C(4,1) = 15 * 4 = 60
        self.assertEqual(len(pieces), 60)
        for plus, minus in pieces:
            self.assertEqual(plus.bit_count(), 2)
            self.assertEqual(minus.bit_count(), 1)
            self.assertEqual(plus & minus, 0)
        self.assertEqual(list(enumerate_profile(3, 4, 0)), [])

    def test_compatible(self):
        # y = +1 at 0, z = +1 at 1  ->  sum {0,1}: compatible
        self.assertTrue(compatible(0b01, 0, 0b10, 0))
        # y = +1 at 0, z = +1 at 0  ->  sum 2: incompatible
        self.assertFalse(compatible(0b01, 0, 0b01, 0))
        # y = +1 at 0, z = -1 at 0  ->  sum 0: compatible
        self.assertTrue(compatible(0b01, 0, 0, 0b01))
        # y = -1 at 0, z = 0        ->  sum -1: incompatible
        self.assertFalse(compatible(0, 0b01, 0, 0))

    def test_representation_count_positive(self):
        for n in (8, 12, 16):
            self.assertGreater(representation_count(n, 0.1), 0)
        self.assertEqual(representation_count(8, 0.0), 6)

    def test_reduce_common_factor(self):
        self.assertEqual(reduce_common_factor([6, 9, 12], 15), ((2, 3, 4), 5))
        self.assertIsNone(reduce_common_factor([4, 8], 10))
        self.assertEqual(reduce_common_factor([3, 5], 7), ((3, 5), 7))

    def test_matches_oracle_small(self):
        rng = random.Random(36311)
        for n in range(8, 13):
            for trial in range(12):
                if trial % 2 == 0:
                    values = [rng.randrange(1, 1 << n) for _ in range(n)]
                    target = sum(values[i] for i in rng.sample(range(n), n // 2))
                else:
                    values = [rng.randrange(1, 30) for _ in range(n)]
                    target = rng.randrange(0, sum(values) + 1)
                expected = oracle(values, target)
                result = broadened_subset_sum(values, target, alpha=0.1, seed=trial)
                self.assertEqual(result.feasible, expected, (n, values, target))
                if result.feasible:
                    self.assertEqual(sum(values[i] for i in result.indices), target)


if __name__ == "__main__":
    unittest.main()
