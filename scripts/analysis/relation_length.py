#!/usr/bin/env python3
"""R13a: how short a relation must a high-energy support contain?

Rigorous counting lemma (see ``HIGH_ENERGY.md``). Let ``S`` be the support of a
solution, ``m = |S| = n/2``, and ``T = Sigma_{m/2}(S)`` with ``D = |T|``. If
every pair of distinct ``j``-subsets of ``S`` has distinct sums for ``j <= k``
(``S`` is ``k``-dissociated), then fixing any ``R subset S`` with ``|R| = m/2 - k``
the sums ``R + K`` over ``k``-subsets ``K`` of ``S \\ R`` are distinct elements
of ``T``, so ``D >= C(m/2 + k, k)``. Hence ``D < C(m/2 + k, k)`` forces two
distinct ``k'``-subsets (``k' <= k``) of ``S`` with equal sum, i.e. disjoint
``P, Q subset S``, ``|P| = |Q| <= k``, ``sum P = sum Q``.

For ``D = 2^(delta n)`` this tabulates the smallest such ``k`` (as a fraction of
``n``), the cost exponent of finding an equal-sum pair of ``k``-subsets among all
``n`` elements by sorting (``log2 C(n, k) / n``), the residual meet-in-the-middle
exponent if ``P u Q`` is known to lie in the solution (``(n - 2k)/(2n)``), and the
LIFT.md exponent ``max(0.4057, log2 C(n,n/4)/n - delta)`` for comparison.

Writes docs/analysis/2026-10-06/subset-sum/relation_length.md.
"""

import argparse
from math import lgamma, log, log2
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def log2_comb(n: float, k: float) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return (lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1)) / log(2)


def h2(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def smallest_k_fraction(delta: float, n: int = 20000) -> float:
    """Smallest k/n with log2 C(m/2+k, k) > delta*n, m = n/2 (asymptotic, via bisection)."""
    m = n / 2
    lo, hi = 0.0, m
    for _ in range(60):
        mid = (lo + hi) / 2
        if log2_comb(m / 2 + mid, mid) > delta * n:
            hi = mid
        else:
            lo = mid
    return hi / n


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    lift = lambda delta: max(0.4057, h2(0.25) - delta)  # noqa: E731
    rows = [
        "| delta (D=2^(delta n)) | k/n | k/m | find relation exp | residual MITM exp | LIFT exp |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for delta in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.311, 0.35, 0.40, 0.45, 0.50):
        k = smallest_k_fraction(delta)
        find = h2(k)
        residual = (1 - 2 * k) / 2
        rows.append(
            f"| {delta:.3f} | {k:.4f} | {2 * k:.4f} | {find:.4f} | {residual:.4f} | "
            f"{lift(delta):.4f} |"
        )
        print(rows[-1])
    lines = [
        "# R13a: forced relation length in the high-energy regime",
        "",
        "Asymptotic exponents (`n -> infinity`, `m = n/2`). `k/n` is the smallest "
        "`k` with `C(m/2 + k, k) > D`; below it the support must contain disjoint "
        "`P, Q` with `|P| = |Q| <= k` and equal sum (rigorous counting; "
        "`HIGH_ENERGY.md`). `find relation exp` is `log2 C(n,k)/n`, the cost of "
        "finding an equal-sum pair of `k`-subsets among all `n` inputs by sorting. "
        "`residual MITM exp` assumes `P u Q` is known to lie in the solution and "
        "solves the remaining `n - 2k` elements by meet-in-the-middle. `LIFT exp` "
        "is the `LIFT.md` exponent (`max(0.4057, 0.811 - delta)`, capped by `0.5`). "
        "The conditional columns only help if the found relation lies inside the "
        "support, which is not guaranteed on adversarial decoys.",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "relation_length.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
