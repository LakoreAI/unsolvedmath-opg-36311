"""Checks for the three-level BCJ tree."""

import random
import unittest

from src.bcj_tree import (
    TreeParams,
    bcj_tree_subset_sum,
    modulus_targets,
    tree_moduli,
)
from src.subset_sum import meet_in_middle


def _planted(n, seed):
    rng = random.Random(seed)
    values = [rng.randrange(1, 1 << n) for _ in range(n)]
    support = rng.sample(range(n), n // 2)
    return values, sum(values[i] for i in support)


class BcjTreeTests(unittest.TestCase):
    def test_profiles_halve_consistently(self):
        p = TreeParams(16, 2, 1, 0)
        self.assertEqual((p.nu.ones, p.nu.minus), (6, 2))
        self.assertEqual((p.kappa.ones, p.kappa.minus), (4, 2))
        self.assertEqual((p.omega.ones, p.omega.minus), (2, 1))

    def test_rejects_odd_profiles(self):
        with self.assertRaises(ValueError):
            TreeParams(24, 2, 1, 0)  # nu = (8, 2): halves 4, 1 differ in parity
        with self.assertRaises(ValueError):
            TreeParams(12, 2, 1, 0)

    def test_moduli_are_distinct_primes(self):
        p = TreeParams(16, 2, 1, 0)
        moduli = tree_moduli(p)
        self.assertEqual(len(set(moduli)), 3)
        self.assertEqual(modulus_targets(p)[0], 12)

    def test_solutions_are_correct_and_found_by_tree(self):
        p = TreeParams(16, 2, 1, 0)
        tree_hits = 0
        for t in range(8):
            values, target = _planted(16, t)
            result = bcj_tree_subset_sum(values, target, p, attempts=60, seed=t)
            got = set(result.indices)
            self.assertEqual(len(got), 8)
            self.assertEqual(sum(values[i] for i in got), target)
            tree_hits += result.strategy == "bcj-tree"
        self.assertGreaterEqual(tree_hits, 6)

    def test_infeasible_instance_falls_back_to_none(self):
        p = TreeParams(16, 2, 1, 0)
        values = [2 * (i + 1) for i in range(16)]
        result = bcj_tree_subset_sum(values, 1, p, attempts=3)
        self.assertIsNone(result.indices)
        self.assertEqual(meet_in_middle(values, 1).indices, None)


if __name__ == "__main__":
    unittest.main()
