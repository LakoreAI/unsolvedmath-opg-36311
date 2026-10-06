"""Exact integer LLL and the relation lattice of a subset-sum instance.

``lll_reduce`` is the textbook LLL algorithm in exact rational arithmetic
(``fractions.Fraction``); it is slow but dependency-free and exact, which is what
the small experiments here need (dimension up to a few dozen). ``relation_basis``
returns a reduced basis of ``{z in Z^n : z . a = 0}`` obtained by reducing the
embedding ``(e_i | scale * a_i)`` and keeping the rows whose last coordinate is
zero.
"""

from fractions import Fraction
from typing import Sequence


def _dot(u: Sequence[int | Fraction], v: Sequence[int | Fraction]):
    return sum(x * y for x, y in zip(u, v))


def lll_reduce(
    basis: Sequence[Sequence[int]], delta: Fraction = Fraction(3, 4)
) -> list[list[int]]:
    """LLL-reduce an integer basis (rows are basis vectors)."""
    b = [list(map(int, row)) for row in basis]
    n = len(b)

    def gram_schmidt():
        ortho: list[list[Fraction]] = []
        mu = [[Fraction(0)] * n for _ in range(n)]
        norms: list[Fraction] = []
        for i in range(n):
            v = [Fraction(x) for x in b[i]]
            for j in range(i):
                mu[i][j] = _dot(b[i], ortho[j]) / norms[j]
                v = [x - mu[i][j] * y for x, y in zip(v, ortho[j])]
            ortho.append(v)
            norms.append(_dot(v, v))
        return mu, norms

    mu, norms = gram_schmidt()
    k = 1
    while k < n:
        for j in range(k - 1, -1, -1):
            q = round(mu[k][j])
            if q:
                b[k] = [x - q * y for x, y in zip(b[k], b[j])]
                mu, norms = gram_schmidt()
        if norms[k] >= (delta - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            mu, norms = gram_schmidt()
            k = max(k - 1, 1)
    return b


def relation_basis(values: Sequence[int], scale: int | None = None) -> list[list[int]]:
    """Reduced basis of the integer relations ``z . values = 0``.

    Rows of the embedding ``(e_i | scale * a_i)`` are LLL-reduced; with a large
    ``scale`` the rows with last coordinate zero form a basis of the relation
    lattice (of rank ``n - 1`` for generic inputs).
    """
    n = len(values)
    if scale is None:
        scale = 1 << (2 * n + 8)
    rows = [
        [1 if i == j else 0 for j in range(n)] + [scale * values[i]] for i in range(n)
    ]
    reduced = lll_reduce(rows)
    return [row[:n] for row in reduced if row[n] == 0 and any(row[:n])]


def norm2(vec: Sequence[int]) -> int:
    return sum(x * x for x in vec)
