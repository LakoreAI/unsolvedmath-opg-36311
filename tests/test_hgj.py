"""Checks for the Howgrave-Graham-Joux representation search."""

import math
import random
import unittest

from src.hgj import (
    balanced_probability,
    enumerated_size,
    hgj_permuted_search,
    hgj_search,
    weight_residue_subsets,
)


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

    def test_balanced_probability_is_polynomial(self):
        # C(n/2,n/4)^2 / C(n,n/2) decays like 1/sqrt(n), not exponentially.
        self.assertAlmostEqual(balanced_probability(4, 2), 4 / 6)
        previous = 1.0
        for n in (16, 64, 256, 1024):
            p = balanced_probability(n, n // 2)
            self.assertLess(p, previous)
            self.assertGreater(p * math.sqrt(n), 0.5)
            previous = p
        self.assertEqual(balanced_probability(8, 10), 0.0)

    def test_permutation_repairs_concentrated_support(self):
        n = 24
        successes = 0
        for t in range(6):
            rng = random.Random(500 + t)
            values = [rng.randrange(1, 1 << 24) for _ in range(n)]
            support = rng.sample(range(n // 2), n // 2)  # entirely in the first half
            target = sum(values[i] for i in support)
            self.assertFalse(hgj_search(values, target, seed=t).feasible)
            result = hgj_permuted_search(
                values, target, permutations=24, residues=16, seed=t
            )
            if result.feasible:
                got = set(result.indices)
                self.assertEqual(sum(values[i] for i in got), target)
                self.assertEqual(len(got), n // 2)
                successes += 1
        self.assertGreaterEqual(successes, 5)

    def test_explicit_modulus(self):
        rng = random.Random(9)
        values, target, _ = _planted(16, rng)
        result = hgj_search(values, target, modulus=10007, residues=16)
        if result.feasible:
            self.assertEqual(sum(values[i] for i in result.indices), target)


if __name__ == "__main__":
    unittest.main()
