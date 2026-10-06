#!/usr/bin/env python3
"""R13: numeric check of the single-prime lift under a distinct-sums hypothesis.

``LIFT.md`` proves: if the weight-``n/4`` sub-sums of a solution's support take
``D`` distinct values, then for a random prime ``p`` in ``[M, 2M]`` with
``M ~ D`` the expected number of residues they cover is at least
``D / (1 + D*B/pi)`` (``B`` bounds the prime factors ``>= M`` of a difference,
``pi`` counts primes in the window). This script measures ``D``, the mean
coverage over the window, and the predicted lower bound, on planted supports
from the adversarial families.

Writes docs/analysis/2026-10-06/subset-sum/lift_check.md.
"""

import argparse
import random
import sys
from itertools import combinations
from math import ceil, log, log2
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hgj_adversarial import FAMILIES, make_family, next_prime  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
SIZES = (24, 28)


def primes_in(lo: int, hi: int) -> list[int]:
    out = []
    p = lo
    while True:
        p = next_prime(p)
        if p >= hi:
            return out
        out.append(p)
        p += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| n | family | Y | D | D/Y | M | mean cover/D | bound | min cover/D |",
        "| ---: | :-- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n in SIZES:
        for name in FAMILIES:
            rng = random.Random(args.seed + n)
            values = make_family(name, n, rng)
            support = rng.sample(range(n), n // 2)
            sums = {
                sum(values[support[i]] for i in c)
                for c in combinations(range(n // 2), n // 4)
            }
            y = len(list(combinations(range(n // 2), n // 4)))
            d = len(sums)
            m = 1 << (ceil(log2(max(d, 2))) + 2)
            window = primes_in(m, 2 * m)
            covers = [len({s % p for s in sums}) / d for p in window]
            diff = max(sums) - min(sums)
            b = max(1.0, log(max(diff, 2)) / log(m))
            bound = 1 / (1 + d * b / len(window))
            rows.append(
                f"| {n} | {name} | {y} | {d} | {d / y:.3f} | {m} | "
                f"{sum(covers) / len(covers):.3f} | {bound:.3f} | {min(covers):.3f} |"
            )
            print(rows[-1], flush=True)

    lines = [
        "# R13: single-prime coverage under the distinct-sums hypothesis",
        "",
        "`Y = C(n/2, n/4)` representations of a planted weight-`n/2` support; "
        "`D` the number of distinct weight-`n/4` sub-sums; window "
        "`p in [M, 2M]` with `M` the power of two `>= 4D`. `bound` is the "
        "`LIFT.md` lower bound `1/(1 + D B / pi)` on mean coverage per distinct "
        "sum. The bound is a lower bound, so `mean cover/D >= bound` must hold.",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "lift_check.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
