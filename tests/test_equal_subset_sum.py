"""Differential checks for the Equal-Subset-Sum baselines."""

from itertools import product
import random
import unittest

from src.equal_subset_sum import equal_subset_sum, pigeonhole_equal_subset_sum


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

    def test_promise_enforced(self):
        with self.assertRaises(ValueError):
            pigeonhole_equal_subset_sum([1 << 10, 1 << 10])


if __name__ == "__main__":
    unittest.main()
