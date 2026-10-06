"""Checks for compress-then-MITM."""

import random
import unittest

from src.compress_mitm import find_cores, solve_compressed
from src.subset_sum import meet_in_middle


def _structured(n, rng):
    """Half the inputs are multiples of a few generators (relations), half random."""
    gens = [rng.randrange(50, 400) for _ in range(2)]
    core = [gens[rng.randrange(2)] * rng.randrange(1, 4) for _ in range(n // 2)]
    noise = [rng.randrange(1, 1 << 28) for _ in range(n - n // 2)]
    values = core + noise
    rng.shuffle(values)
    return values


class CompressTests(unittest.TestCase):
    def test_always_exact_against_mitm(self):
        for seed in range(40):
            rng = random.Random(seed)
            n = rng.choice([10, 12, 14])
            values = (
                _structured(n, rng)
                if seed % 2
                else [rng.randrange(1, 60) for _ in range(n)]
            )
            support = rng.sample(range(n), rng.randrange(0, n + 1))
            target = sum(values[i] for i in support)
            if seed % 5 == 0:
                target += 1  # often infeasible
            got = solve_compressed(values, target)
            ref = meet_in_middle(values, target)
            self.assertEqual(got.indices is None, ref.indices is None, seed)
            if got.indices is not None:
                self.assertEqual(sum(values[i] for i in got.indices), target)
                self.assertEqual(len(set(got.indices)), len(got.indices))

    def test_core_found_for_duplicates(self):
        cores, _ = find_cores([7, 7, 100, 5000, 9999], 2)
        self.assertEqual(cores[1], {0, 1})

    def test_saves_states_on_structured_input(self):
        rng = random.Random(5)
        values = _structured(20, rng)
        target = sum(values[i] for i in rng.sample(range(20), 9))
        got = solve_compressed(values, target)
        self.assertIsNotNone(got.indices)
        self.assertEqual(got.strategy, "compress")
        self.assertLess(got.states, 2**10)


if __name__ == "__main__":
    unittest.main()
