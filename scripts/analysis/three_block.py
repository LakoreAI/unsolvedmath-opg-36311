#!/usr/bin/env python3
"""P2.1: does the three-block 3SUM have exploitable sumset structure?

Split the n numbers into three blocks of n/3 and let S1, S2, S3 be the sets of
distinct block subset sums (|Si| <= N = 2^(n/3)). Subset sum is 3SUM: find
s1 + s2 + s3 = b. The simplest structured algorithm lists the smallest pairwise
sumset Si + Sj and matches it against the third block, at cost about
|Si + Sj| + N. This beats meet-in-the-middle only if |Si + Sj| <= 2^((1/2 - eps)n).

Since a pairwise sum uses 2n/3 numbers of beta*n bits, |Si + Sj| is at most
about min(2^(2n/3), (2n/3) * 2^(beta n)). So the pairwise sumset is small only
when beta < 1/2, where the dynamic program already runs in 2^(beta n). This
script measures the exponents to check that prediction, over the index split
and the best of several random splits.

Writes docs/analysis/2026-10-03/subset-sum/three_block.md.
"""

import argparse
import math
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (18, 21, 24)
BETAS = (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)


def block_sums(values):
    sums = {0}
    for value in values:
        sums |= {s + value for s in sums}
    return sums


def smallest_pair_sumset(values, order):
    k = len(values) // 3
    blocks = [
        block_sums([values[i] for i in order[j * k : (j + 1) * k]]) for j in range(3)
    ]
    blocks[2] = block_sums([values[i] for i in order[2 * k :]])
    return min(
        len({u + v for u in blocks[i] for v in blocks[j]})
        for i, j in ((0, 1), (0, 2), (1, 2))
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--splits", type=int, default=8)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for beta in BETAS:
            rng = random.Random(args.seed + n * 1000 + int(beta * 100))
            bits = max(1, round(beta * n))
            index_e, best_e = [], []
            for _ in range(args.trials):
                values = [rng.randrange(1, 1 << bits) for _ in range(n)]
                index_e.append(
                    math.log2(smallest_pair_sumset(values, list(range(n)))) / n
                )
                best = min(
                    smallest_pair_sumset(values, rng.sample(range(n), n))
                    for _ in range(args.splits)
                )
                best_e.append(math.log2(best) / n)
            predicted = min(2 / 3, (math.log2(2 * n / 3) + bits) / n)
            row = (n, beta, predicted, sum(index_e) / len(index_e), min(best_e))
            rows.append(row)
            print(*row)

    lines = [
        "# P2.1: pairwise sumsets in the three-block split",
        "",
        "Exponent `e` of the smallest pairwise sumset `|Si + Sj|` (size about "
        "`2^(e*n)`). Listing it and matching against the third block beats "
        "meet-in-the-middle only if `e < 0.5`. `predicted` is "
        "`min(2/3, (log2(2n/3) + bits)/n)`. `index` is the mean over "
        f"{args.trials} inputs with consecutive blocks; `best` is the smallest "
        f"over {args.splits} random splits per input.",
        "",
        "| n | beta | predicted e | index e | best e |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, beta, predicted, index_e, best_e in rows:
        lines.append(
            f"| {n} | {beta} | {predicted:.3f} | {index_e:.3f} | {best_e:.3f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "three_block.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
