"""Checks for the additive-combinatorics probes."""

import unittest

from src.additive import (
    additive_energy,
    cardinality_counts,
    collision_count,
    longest_arithmetic_progression,
    near_geometric_distance,
    representation_count,
    representation_residues,
    residue_profile,
    subset_sums,
)


class AdditiveTests(unittest.TestCase):
    def test_subset_sums(self):
        self.assertEqual(subset_sums([1, 2]), [0, 1, 2, 3])
        self.assertEqual(subset_sums([1, 1]), [0, 1, 2])

    def test_collision_count(self):
        self.assertEqual(collision_count([1, 1]), 1)
        self.assertEqual(collision_count([1, 2, 4]), 0)

    def test_representation_count(self):
        self.assertEqual(representation_count([1, 1], 1), 2)
        self.assertEqual(representation_count([1, 2, 4], 3), 1)
        self.assertEqual(representation_count([1, 2, 4], 8), 0)

    def test_additive_energy(self):
        self.assertEqual(additive_energy([0]), 1)
        self.assertEqual(additive_energy([0, 1]), 6)

    def test_near_geometric_distance(self):
        self.assertEqual(near_geometric_distance([1, 2, 4, 8]), 0)
        self.assertEqual(near_geometric_distance([1, 2, 5]), 1)

    def test_longest_arithmetic_progression(self):
        self.assertEqual(longest_arithmetic_progression([1, 2, 3, 4]), 4)
        self.assertEqual(longest_arithmetic_progression([1, 2, 4, 8]), 2)

    def test_cardinality_counts(self):
        counts = cardinality_counts([1, 2, 3], 3)
        self.assertEqual(counts[1], 1)  # {3}
        self.assertEqual(counts[2], 1)  # {1, 2}
        self.assertEqual(counts[0], 0)
        self.assertEqual(counts[3], 0)

    def test_representation_residues(self):
        residues = representation_residues([1, 2, 4], 0b111, 1, 4)
        self.assertEqual(dict(residues), {1: 1, 2: 1, 0: 1})
        profile = residue_profile([1, 2, 4], 0b111, 1, 4)
        self.assertEqual(profile["decompositions"], 3)
        self.assertEqual(profile["distinct_residues"], 3)
        self.assertAlmostEqual(profile["coverage"], 0.75)


if __name__ == "__main__":
    unittest.main()
