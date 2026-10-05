#!/usr/bin/env python3
"""R16: is the close-pair search cheap exactly in the structured PESS regime?

The PESS O*(2^(n/3)) structural branch guesses the poly(n)-size set of close
pairs (X, Y) of high-index elements, where |w(X) - w(Y)| <= w([k]). The original
reference enumeration is 2^(n-k); the branch-and-bound ``close_pairs_structured``
is complete but prunes when the remaining suffix magnitude cannot close the
band. Its cost is polynomial on a nearly geometric input (when w_i ~ 2^i the
remaining suffix is dominated by one element) and exponential on collision-heavy
inputs, which is where the algorithm switches to subsampling.

This script measures the branch-and-bound visit count and the close-pair count
for a near-geometric family and for a dense random family, reporting base-2
exponents per n. Prediction: geometric exponents near 0 (poly(n)), dense
exponents large.

Writes docs/analysis/2026-10-03/subset-sum/pess_structure.md.
"""

import argparse
import math
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.equal_subset_sum import close_pair_visit_count, close_pairs_structured

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 19, 22)
FAMILIES = ("geometric", "dense")


def geometric_instance(n: int) -> list[int]:
    """Near-geometric PESS instance: 1, 2, 4, ..., 2^(n-1) with the top dropped."""
    values = [1 << i for i in range(n)]
    values[-1] -= 1
    return values


def dense_instance(n: int, rng: random.Random) -> list[int]:
    """Collision-heavy PESS instance: many small equal weights."""
    return sorted(rng.randrange(1, 5) for _ in range(n))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for k in sorted({n // 3, n // 2}):
            for family in FAMILIES:
                rng = random.Random(args.seed + n * 100 + k)
                if family == "geometric":
                    values = geometric_instance(n)
                else:
                    values = dense_instance(n, rng)
                visits = close_pair_visit_count(values, k)
                pairs = len(close_pairs_structured(values, k))
                rows.append(
                    (
                        n,
                        k,
                        family,
                        math.log2(max(visits, 1)) / n,
                        math.log2(max(pairs, 1)) / n,
                    )
                )
                print(*rows[-1])

    lines = [
        "# R16: cost of the structured close-pair search",
        "",
        "Base-2 exponents per `n` of the branch-and-bound node count (`visit e`) "
        "and of the number of close pairs `(X, Y)` (`pairs e`), for a near-"
        "geometric PESS instance (`1, 2, 4, ..., 2^(n-1)` with the top element "
        "reduced by 1) and a collision-heavy dense instance of weights in "
        "`[1, 4]`. `k` is the prefix cutoff. A near-zero `visit e` on the "
        "geometric family is the structured regime the `O*(2^(n/3))` algorithm "
        "relies on; the dense family is where it must subsample instead.",
        "",
        "| n | k | family | visit e | pairs e |",
        "| ---: | ---: | :-- | ---: | ---: |",
    ]
    for n, k, family, visit_e, pairs_e in rows:
        lines.append(f"| {n} | {k} | {family} | {visit_e:.3f} | {pairs_e:.3f} |")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "pess_structure.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
