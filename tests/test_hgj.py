"""Checks for the Howgrave-Graham-Joux representation search."""

import math
import random
import unittest

from src.hgj import enumerated_size, hgj_search, weight_residue_subsets


def _planted(n, rng):
    """A random hard-knapsack instance with a balanced weight-n/2 solution."""
    values = [rng.randrange(1, 1 << 20) for _ in range(n)]
    k = n // 2
    left = rng.sample(range(k), n // 4)
    right = rng.sample(range(k, n), n // 4)
    indices = set(left) | set(right)
    target = sum(values[i] for i in indices)
    return values, target, indices


class HgjTests(unittest.TestCase):
    def test_weight_residue_subsets_balanced(self):
        rng = random.Random(1)
        values = [rng.randrange(0, 20) for _ in range(8)]
        modulus = 8
        k = 4
        for residue in range(modulus):
            got = sorted(weight_residue_subsets(values, 2, modulus, residue))
            expected = []
            for i in range(k):
                for j in range(k):
                    total = values[i] + values[k + j]
                    if total % modulus == residue:
                        expected.append((total, (1 << i) | (1 << (k + j))))
            self.assertEqual(got, sorted(expected), residue)

    def test_enumerated_size(self):
        self.assertEqual(enumerated_size(32, 8), 2 * math.comb(16, 4))
        self.assertEqual(enumerated_size(64, 16), 2 * math.comb(32, 8))

    def test_certificate_matches_inline(self):
        for n in (16, 24, 32):
            for t in range(6):
                rng = random.Random(2000 + n + t)
                values, target, _ = _planted(n, rng)
                inline = hgj_search(values, target, seed=t)
                certified = hgj_search(values, target, seed=t, certificate=True)
                self.assertEqual(inline.feasible, certified.feasible, (n, t))
                if certified.feasible:
                    got = set(certified.indices)
                    self.assertEqual(len(got), n // 2)
                    self.assertEqual(sum(values[i] for i in got), target)

    def test_finds_planted_solution(self):
        for n in (16, 24, 32):
            successes = 0
            trials = 10
            for t in range(trials):
                rng = random.Random(1000 + n + t)
                values, target, _ = _planted(n, rng)
                result = hgj_search(values, target, seed=t)
                if result.feasible:
                    got = set(result.indices)
                    self.assertEqual(len(got), len(result.indices))
                    self.assertEqual(len(got), n // 2)
                    self.assertEqual(sum(values[i] for i in got), target)
                    successes += 1
            self.assertGreaterEqual(successes, trials - 2, n)


if __name__ == "__main__":
    unittest.main()
