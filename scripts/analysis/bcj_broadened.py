#!/usr/bin/env python3
"""R13: the broadened (BCJ) representation on planted instances.

Ports BCJ's Section 3.1 construction: the solution splits as ``y + z`` with
coefficients in ``{-1,0,1}``, each piece carrying ``(1/4+alpha)n`` ones and
``alpha n`` minus-ones. Broadening increases the representation count ``N_D``
while the modular filter keeps the searched lists small. This script measures,
for planted balanced solutions, the ambient list size, ``N_D``, the filtered
list size, and the success of the two-piece search. It is the single-level
construction, not BCJ's three-level recursion.

Writes docs/analysis/2026-10-05/subset-sum/bcj_broadened.md.
"""

import argparse
import math
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.bcj import broadened_subset_sum, representation_count  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (12, 16)
ALPHAS = (0.0, 0.05, 0.10, 0.15)
TRIALS = 6
RESIDUES = 8


def next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def profile_size(n: int, alpha: float) -> int:
    ones = round((0.25 + alpha) * n)
    minus = round(alpha * n)
    if ones < 0 or minus < 0 or ones + minus > n:
        return 0
    return math.comb(n, ones) * math.comb(n - ones, minus)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for alpha in ALPHAS:
            ambient = profile_size(n, alpha)
            reps = representation_count(n, alpha)
            modulus = next_prime(max(2, min(reps, 1 << n)))
            filtered = ambient / modulus
            successes = 0
            for trial in range(TRIALS):
                rng = random.Random(args.seed + n * 100 + int(alpha * 1000) + trial)
                values = [rng.randrange(1, 1 << n) for _ in range(n)]
                support = sorted(rng.sample(range(n), n // 2))
                target = sum(values[i] for i in support)
                result = broadened_subset_sum(
                    values, target, alpha=alpha, residues=RESIDUES, seed=trial
                )
                if result.feasible and (
                    sum(values[i] for i in result.indices) == target
                ):
                    successes += 1
            rows.append(
                (n, alpha, ambient, reps, modulus, filtered, successes / TRIALS)
            )
            print(*rows[-1])

    lines = [
        "# R13: the broadened (BCJ Section 3.1) representation",
        "",
        "Planted balanced solutions. `ambient` is the number of pieces with the "
        "profile `(1/4+alpha)n` ones and `alpha n` minus-ones; `N_D` the number "
        "of representations of a solution; `M` the filter modulus; `filtered = "
        "ambient/M`. Broadening raises `N_D` and `ambient` together. This is the "
        "single-level construction (direct enumeration), not BCJ's three-level "
        "recursion.",
        "",
        "| n | alpha | ambient | N_D | M | filtered | success |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, alpha, ambient, reps, modulus, filtered, success in rows:
        lines.append(
            f"| {n} | {alpha:.2f} | {ambient:.3e} | {reps:.3e} | {modulus} | "
            f"{filtered:.1f} | {success:.2f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "bcj_broadened.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
