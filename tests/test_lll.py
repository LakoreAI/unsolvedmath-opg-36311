"""Checks for the exact LLL and relation lattice."""

import random
import unittest

from src.lll import lll_reduce, norm2, relation_basis


class LllTests(unittest.TestCase):
    def test_reduction_shortens_and_preserves_lattice(self):
        basis = [[1, 0, 0, 12345], [0, 1, 0, 6789], [0, 0, 1, 1011]]
        reduced = lll_reduce(basis)
        self.assertEqual(len(reduced), 3)
        self.assertLess(sum(norm2(r) for r in reduced), sum(norm2(r) for r in basis))

    def test_relation_basis_is_a_relation(self):
        rng = random.Random(3)
        for n in (6, 8, 10):
            values = [rng.randrange(1, 1 << n) for _ in range(n)]
            basis = relation_basis(values)
            self.assertEqual(len(basis), n - 1)
            for row in basis:
                self.assertEqual(sum(z * a for z, a in zip(row, values)), 0)

    def test_duplicate_gives_unit_relation(self):
        values = [5, 5, 11, 20, 33]
        norms = sorted(norm2(r) for r in relation_basis(values))
        self.assertEqual(norms[0], 2)  # e_0 - e_1


if __name__ == "__main__":
    unittest.main()
