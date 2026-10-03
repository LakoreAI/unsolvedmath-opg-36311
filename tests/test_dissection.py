"""Checks for the Wagner four-list modular k-sum core."""

import random
import unittest

from src.dissection import verify_4sum, wagner_4sum_mod


class WagnerTests(unittest.TestCase):
    def test_soundness(self):
        rng = random.Random(1)
        for _ in range(50):
            modulus = 1 << 8
            lists = [[rng.randrange(modulus) for _ in range(32)] for _ in range(4)]
            indices = wagner_4sum_mod(lists, modulus)
            if indices is not None:
                self.assertTrue(verify_4sum(lists, indices, modulus))

    def test_finds_solution_when_many_exist(self):
        rng = random.Random(2)
        found = 0
        trials = 30
        for _ in range(trials):
            modulus = 1 << 8
            lists = [[rng.randrange(modulus) for _ in range(32)] for _ in range(4)]
            indices = wagner_4sum_mod(lists, modulus)
            if indices is not None:
                self.assertTrue(verify_4sum(lists, indices, modulus))
                found += 1
        self.assertGreater(found, trials - 3)

    def test_planted_solution(self):
        rng = random.Random(3)
        modulus = 1 << 9
        lists = [[rng.randrange(modulus) for _ in range(24)] for _ in range(4)]
        lists[3][0] = -(lists[0][0] + lists[1][0] + lists[2][0]) % modulus
        indices = wagner_4sum_mod(lists, modulus)
        self.assertIsNotNone(indices)
        self.assertTrue(verify_4sum(lists, indices, modulus))

    def test_validation(self):
        with self.assertRaises(ValueError):
            wagner_4sum_mod([[0]], 4)
        with self.assertRaises(ValueError):
            wagner_4sum_mod([[0]] * 4, 6)
        with self.assertRaises(ValueError):
            wagner_4sum_mod([[0]] * 4, 4, 5)


if __name__ == "__main__":
    unittest.main()
