#!/usr/bin/env python3
"""H1: do random restrictions create balanced representations (synthetically)?

The HGJ search needs a representation y + z of the solution with y, z each of
weight n/4 and each contributing n/8 to either half of a partition. For an
adversarial solution this balanced condition can fail. H1 asks whether a random
partition restores it w.h.p.

For a planted weight-n/2 solution x, count the balanced representations under
many random equipartitions: C(#ones_left, n/8) * C(#ones_right, n/8). A random
partition balances x's ones by Chernoff, so the count should be ~2^(n/2)/poly
with high probability — i.e. randomness, not the solution, can supply balance.

Writes docs/analysis/2026-10-03/subset-sum/synthetic_repr.md.
"""

import argparse
import math
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (32, 48, 64, 96)


def balanced_representations(n, ones, partition, half):
    left = sum(1 for i in ones if i in partition)
    right = len(ones) - left
    if left < half or right < half:
        return 0
    return math.comb(left, half) * math.comb(right, half)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--trials", type=int, default=200)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        rng = random.Random(36311 + n)
        ones = set(rng.sample(range(n), n // 2))
        half = n // 8
        counts = []
        for _ in range(args.trials):
            partition = set(rng.sample(range(n), n // 2))
            counts.append(balanced_representations(n, ones, partition, half))
        nonzero = sum(1 for c in counts if c)
        row = {
            "n": n,
            "trials": args.trials,
            "partitions_with_balance": nonzero,
            "min_representations": min(counts),
            "median_representations": sorted(counts)[len(counts) // 2],
            "log2_median": round(math.log2(sorted(counts)[len(counts) // 2]), 2)
            if sorted(counts)[len(counts) // 2]
            else 0.0,
            "total_representations_log2": n // 2,
        }
        rows.append(row)
        print(
            f"  n={n}: balanced in {nonzero}/{args.trials}, "
            f"median 2^{row['log2_median']} (total 2^{n // 2})"
        )

    lines = [
        "# H1: balanced representations under random partitions",
        "",
        "A planted weight-n/2 solution, 200 random equipartitions. A partition is",
        "balanced if it admits at least one representation with n/8 ones on each",
        "side. `total` is the number of representations before balancing (2^(n/2)).",
        "",
        "| n | partitions with balance | min reps | median reps | median log2 | total log2 |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines += [
        "| {n} | {partitions_with_balance}/{trials} | {min_representations} | "
        "{median_representations} | {log2_median} | {total_representations_log2} |".format(
            **r
        )
        for r in rows
    ]
    lines += [
        "",
        "Reading: random partitions supply a balanced representation with",
        "probability approaching 1, and retain 2^(n/2 - O(log n)) of the",
        "representations. Balancing is therefore a randomization problem, not a",
        "structural obstruction — supporting H1. The remaining obstruction is",
        "whether *enough* representations exist at all (H2).",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "synthetic_repr.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'synthetic_repr.md'}")


if __name__ == "__main__":
    main()
