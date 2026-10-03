"""Dependency-free differential checks: python3 -m unittest tests.test_subset_sum."""

from itertools import product
import random
import unittest

from src.subset_sum import bounded_dp, meet_in_middle, schroeppel_shamir, solve


def oracle(values, target):
    return any(
        sum(a * bit for a, bit in zip(values, bits)) == target
        for bits in product((0, 1), repeat=len(values))
    )


class SubsetSumTests(unittest.TestCase):
    def check_instance(self, values, target):
        expected = oracle(values, target)
        for solver in (bounded_dp, meet_in_middle, schroeppel_shamir, solve):
            result = solver(values, target)
            self.assertEqual(result.feasible, expected, (solver, values, target))
            if result.feasible:
                self.assertEqual(len(set(result.indices)), len(result.indices))
                self.assertTrue(all(0 <= i < len(values) for i in result.indices))
                self.assertEqual(sum(values[i] for i in result.indices), target)

    def test_exhaustive_signed_small_instances(self):
        for n in range(5):
            for values in product((-2, 0, 3), repeat=n):
                for target in range(-9, 14):
                    self.check_instance(values, target)

    def test_seeded_random_instances(self):
        rng = random.Random(36311)
        for _ in range(150):
            values = [rng.randrange(-15, 16) for _ in range(rng.randrange(11))]
            self.check_instance(values, rng.randrange(-50, 51))

    def test_no_item_reuse(self):
        self.check_instance([3], 6)
        self.check_instance([3, 3], 6)

    def test_arbitrary_precision_mitm(self):
        a = 10**100
        result = meet_in_middle([a, -a + 7, a + 1], 7)
        self.assertTrue(result.feasible)
        self.assertEqual(result.indices, (0, 1))

    def test_schroeppel_shamir_explicit(self):
        result = solve([3, -2, 7, 0, 5, -1, 4, 9], 12, "ss")
        self.assertEqual(result.algorithm, "ss")
        self.assertTrue(result.feasible)
        self.assertEqual(sum([3, -2, 7, 0, 5, -1, 4, 9][i] for i in result.indices), 12)

    def test_schroeppel_shamir_wide_values(self):
        values = [10**40 + i for i in range(12)]
        target = values[0] + values[5] + values[11]
        result = schroeppel_shamir(values, target)
        self.assertTrue(result.feasible)
        self.assertEqual(sum(values[i] for i in result.indices), target)

    def test_validation(self):
        with self.assertRaises(TypeError):
            solve([1.5], 2)
        with self.assertRaises(TypeError):
            solve([True], 1)
        with self.assertRaises(ValueError):
            solve([1], 1, "heuristic")


if __name__ == "__main__":
    unittest.main()
