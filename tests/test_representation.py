"""Differential checks for the candidate {0,1} representation pipeline."""

from itertools import product
import random
import unittest

from src.representation import (
    mixing_coverage,
    representation_subset_sum,
    superincreasing_solve,
)


def oracle(values, target):
    return any(
        sum(v for v, bit in zip(values, mask) if bit) == target
        for mask in product((0, 1), repeat=len(values))
    )


def valid(values, target, indices):
    return (
        len(set(indices)) == len(indices)
        and all(0 <= i < len(values) for i in indices)
        and sum(values[i] for i in indices) == target
    )


class RepresentationTests(unittest.TestCase):
    def test_gcd_reduction_and_branches(self):
        result = representation_subset_sum([6, 9, 12], 15)
        self.assertTrue(result.feasible)
        self.assertTrue(valid([6, 9, 12], 15, result.indices))

    def test_infeasible_target_multiple_of_gcd(self):
        result = representation_subset_sum([4, 8, 12], 10)
        self.assertFalse(result.feasible)

    def test_superincreasing_branch(self):
        values = [3, 7, 16, 35, 74]
        result = representation_subset_sum(values, 7 + 35)
        self.assertEqual(result.strategy, "superincreasing")
        self.assertTrue(valid(values, 42, result.indices))

    def test_superincreasing_solve_raises_on_flat(self):
        with self.assertRaises(ValueError):
            superincreasing_solve([2, 2, 5], 4)

    def test_matches_oracle_small(self):
        rng = random.Random(36311)
        for n in range(1, 11):
            for _ in range(40):
                kind = rng.randrange(4)
                if kind == 0:
                    values = [rng.randrange(1, 8) for _ in range(n)]
                elif kind == 1:
                    values = [1 << i for i in range(n)]
                elif kind == 2:
                    values = [rng.randrange(1, 1 << (2 * n)) for _ in range(n)]
                else:
                    values = [7] * n
                target = rng.randrange(0, sum(values) + 1)
                expected = oracle(values, target)
                result = representation_subset_sum(values, target, seed=n)
                self.assertEqual(result.feasible, expected, (values, target))
                if result.feasible:
                    self.assertTrue(valid(values, target, result.indices))

    def test_mixing_coverage_bounds(self):
        values = [1, 2, 4, 8, 16, 32]
        coverage = mixing_coverage(values, list(range(6)), 3, 7)
        self.assertGreaterEqual(coverage, 0.0)
        self.assertLessEqual(coverage, 1.0)
        self.assertAlmostEqual(mixing_coverage([2, 2, 2, 2], [0, 1, 2, 3], 2, 7), 1 / 7)

    def test_mixing_coverage_arguments(self):
        with self.assertRaises(ValueError):
            mixing_coverage([1, 2], [0, 1], 3, 5)


if __name__ == "__main__":
    unittest.main()
