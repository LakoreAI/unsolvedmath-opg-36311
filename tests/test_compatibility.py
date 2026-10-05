"""Differential checks for the compatibility certificate."""

from math import comb
import random
import unittest

from src.compatibility import (
    compatible_pair_with_sum,
    count_disjoint,
    disjoint_pair_brute,
    disjoint_pair_certified,
)


def random_masks(rng, n, count, max_weight):
    masks = set()
    capacity = sum(comb(n, k) for k in range(min(max_weight, n) + 1))
    count = min(count, capacity)
    while len(masks) < count:
        weight = rng.randrange(0, max_weight + 1)
        mask = 0
        for position in rng.sample(range(n), weight):
            mask |= 1 << position
        masks.add(mask)
    return sorted(masks)


class CompatibilityTests(unittest.TestCase):
    def test_certified_matches_existence(self):
        rng = random.Random(36311)
        for n in range(2, 14):
            for _ in range(60):
                a = random_masks(rng, n, rng.randrange(1, 8), n // 2 + 1)
                b = random_masks(rng, n, rng.randrange(1, 8), n // 2 + 1)
                certified = disjoint_pair_certified(a, b, n, seed=n)
                brute = disjoint_pair_brute(a, b)
                self.assertEqual(certified is None, brute is None, (n, a, b))
                if certified is not None:
                    self.assertEqual(certified[0] & certified[1], 0)
                    self.assertIn(certified[0], a)
                    self.assertIn(certified[1], b)

    def test_certified_finds_planted_disjoint_pair(self):
        rng = random.Random(7)
        n = 20
        # Many overlapping pairs (pseudo-solutions) plus one disjoint pair.
        a_masks = []
        b_masks = []
        for _ in range(200):
            a = 0
            b = 0
            for position in rng.sample(range(n), 6):
                if rng.random() < 0.5:
                    a |= 1 << position
                else:
                    b |= 1 << position
            a_masks.append(a)
            b_masks.append(b)
        disjoint_a = 0b111111
        disjoint_b = 0b111111 << 6
        a_masks.append(disjoint_a)
        b_masks.append(disjoint_b)
        self.assertGreaterEqual(count_disjoint(a_masks, b_masks), 1)
        result = disjoint_pair_certified(a_masks, b_masks, n, seed=1)
        self.assertIsNotNone(result)
        self.assertEqual(result[0] & result[1], 0)

    def test_compatible_pair_with_sum(self):
        rng = random.Random(99)
        n = 16
        pieces_a = []
        pieces_b = []
        for _ in range(100):
            a = random_masks(rng, n, 1, 4)[0]
            b = random_masks(rng, n, 1, 4)[0]
            pieces_a.append((a, a.bit_count()))
            pieces_b.append((b, b.bit_count()))
        # Plant a disjoint pair with complementary weights summing to 7.
        disjoint_a = 0b1111
        disjoint_b = 0b1111 << 4
        pieces_a.append((disjoint_a, 4))
        pieces_b.append((disjoint_b, 3))
        result = compatible_pair_with_sum(pieces_a, pieces_b, 7, n, seed=3)
        self.assertIsNotNone(result)
        self.assertEqual(result[0] & result[1], 0)
        self.assertEqual(result[0].bit_count() + result[1].bit_count(), 7)

    def test_empty_and_arguments(self):
        self.assertIsNone(disjoint_pair_certified([], [1], 4))
        self.assertIsNone(disjoint_pair_certified([1], [], 4))
        with self.assertRaises(ValueError):
            disjoint_pair_certified([1], [1], 0)
        with self.assertRaises(ValueError):
            disjoint_pair_certified([1], [1], 4, sample_size=0)


if __name__ == "__main__":
    unittest.main()
