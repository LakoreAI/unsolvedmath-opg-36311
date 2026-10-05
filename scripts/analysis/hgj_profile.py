#!/usr/bin/env python3
"""R13: the profile barrier of the balanced sub-solver.

The balanced sub-solver only enumerates weight-`n/4` pieces that split
`n/8`--`n/8` across the two halves of the input. If a (unique) solution's
representations are off-balance---e.g. its support lies entirely in one half---
the sub-solver never sees a representation and the search returns infeasible,
wrongly answering ``no''. This script measures the effect: planted solutions with
a controlled first-half share, with and without a random permutation of the
input. A low success rate on concentrated supports that is repaired by a
permutation is direct evidence that completeness, not mixing, is the barrier.

Writes docs/analysis/2026-10-05/subset-sum/hgj_profile.md.
"""

import argparse
from math import comb, log2
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hgj import hgj_search  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (32, 40, 48)
RESIDUES = 16
TRIALS = 4


def planted(n: int, first_half_share: int, rng: random.Random):
    """A weight-`n/2` solution with a chosen number of elements in the first half."""
    half = n // 2
    first = rng.sample(range(half), first_half_share)
    second = rng.sample(range(half, n), half - first_half_share)
    return sorted(first + second)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        half = n // 2
        shares = sorted({0, half // 8, half // 4, half // 2})
        for share in shares:
            plain_success = perm_success = 0
            for trial in range(TRIALS):
                rng = random.Random(args.seed + n * 100 + share * 10 + trial)
                values = [rng.randrange(1, 1 << n) for _ in range(n)]
                support = planted(n, share, rng)
                target = sum(values[i] for i in support)

                # No permutation: contiguous halves as coded.
                result = hgj_search(
                    values, target, weight=half, residues=RESIDUES, seed=trial
                )
                plain_success += result.feasible

                # With a random permutation of the values (target unchanged).
                perm = list(range(n))
                random.Random(args.seed + trial).shuffle(perm)
                pvalues = [values[i] for i in perm]
                presult = hgj_search(
                    pvalues, target, weight=half, residues=RESIDUES, seed=trial
                )
                perm_success += presult.feasible

            rows.append((n, share, plain_success / TRIALS, perm_success / TRIALS))
            print(*rows[-1])

    lines = [
        "# R13: the profile barrier of the balanced sub-solver",
        "",
        "Planted weight-`n/2` solutions with `share` elements in the first half "
        "(`share = n/4` is balanced). `no perm` is the success rate with the "
        "input's natural contiguous halves; `perm` is after one random "
        "permutation of the values (the target is unchanged). A concentrated "
        "solution has no balanced representation, so the balanced sub-solver "
        "misses it and wrongly answers ``no''; a permutation only repairs it "
        "with the probability that the solution lands balanced.",
        "",
        "| n | first-half share | no perm success | perm success |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for n, share, plain, perm in rows:
        lines.append(f"| {n} | {share} | {plain:.2f} | {perm:.2f} |")

    lines += [
        "",
        "## Cost of completeness",
        "",
        "The balanced profile alone costs `C(n/2, n/8)^2 = 2^(0.4057n)` and is "
        "incomplete. Enumerating every weight profile `i + j = n/4` costs "
        "`sum_i C(n/2,i) C(n/2,n/4-i) = C(n, n/4) = 2^(0.811n)`, above "
        "meet-in-the-middle. Broadening the representations (overlaps) is what "
        "recovers completeness below `2^(n/2)`.",
        "",
        "| n | balanced profile e | all profiles e | meet-in-the-middle e |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for n in SIZES:
        balanced = log2(2 * comb(n // 2, n // 8))
        all_profiles = log2(comb(n, n // 4))
        lines.append(f"| {n} | {balanced / n:.4f} | {all_profiles / n:.4f} | 0.5000 |")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "hgj_profile.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
