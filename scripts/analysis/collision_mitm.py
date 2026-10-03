#!/usr/bin/env python3
"""R19: do colliding subset sums make subset sum easier?

Either-or subset sum (Randolph) implies that inputs whose 2^n subset sums are
all distinct are solvable below 2^(n/2). So hard inputs, if any, have some
colliding sums. This script asks whether collisions in turn help, measuring
over a sweep of number sizes 2^(beta*n):

  * excess    = 1 - |S(A)|/2^n, the fraction of subsets that repeat a sum;
  * mitm      = (|S(L)|+|S(R)|) / (|L-list|+|R-list|), the work of
                meet-in-the-middle on distinct half sums, for the index split
                and for the best of several random splits;
  * birthday  = log2(2^n / sqrt(C2)) / n with C2 = sum_t f_t (f_t - 1), the
                exponent of random sampling until two subsets share a sum.

Writes docs/analysis/2026-10-03/subset-sum/collision_mitm.md.
"""

import argparse
from collections import Counter
import math
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 20)
BETAS = (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.25, 1.5)


def subset_sums(values):
    sums = [0]
    for value in values:
        sums += [s + value for s in sums]
    return sums


def mitm_ratio(values, left_positions):
    left = [values[i] for i in left_positions]
    right = [v for i, v in enumerate(values) if i not in left_positions]
    distinct = len(set(subset_sums(left))) + len(set(subset_sums(right)))
    return distinct / ((1 << len(left)) + (1 << len(right)))


def measure(values, rng, splits):
    n = len(values)
    left_sums = subset_sums(values[: n // 2])
    right_sums = subset_sums(values[n // 2 :])
    freq = Counter(u + v for u in left_sums for v in right_sums)
    pairs = sum(f * (f - 1) for f in freq.values())
    birthday = math.log2((1 << n) / math.sqrt(pairs)) / n if pairs else float("inf")
    index_split = mitm_ratio(values, set(range(n // 2)))
    best_split = min(
        mitm_ratio(values, set(rng.sample(range(n), n // 2))) for _ in range(splits)
    )
    return 1 - len(freq) / (1 << n), index_split, best_split, birthday


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--splits", type=int, default=32)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for beta in BETAS:
            rng = random.Random(args.seed + n * 1000 + int(beta * 100))
            bits = max(1, round(beta * n))
            samples = [
                measure(
                    [rng.randrange(1, 1 << bits) for _ in range(n)], rng, args.splits
                )
                for _ in range(args.trials)
            ]
            means = [sum(column) / len(column) for column in zip(*samples)]
            rows.append((n, beta, bits, *means))
            print(n, beta, *(f"{m:.4f}" for m in means))

    lines = [
        "# R19: do colliding subset sums make subset sum easier?",
        "",
        f"Random numbers in `[1, 2^bits)` with `bits = round(beta*n)`; means over "
        f"{args.trials} inputs. `mitm` is the work of meet-in-the-middle on distinct "
        "half sums relative to the plain method (1 = no saving); `best` is the "
        f"best of {args.splits} random balanced splits. `birthday` is the exponent "
        "`e` such that about `2^(e*n)` random subsets are needed before two share "
        "a sum (`e < 0.5` beats meet-in-the-middle for finding a collision).",
        "",
        "| n | beta | bits | excess | mitm (index split) | mitm (best split) | birthday e |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, beta, bits, excess, index_split, best_split, birthday in rows:
        lines.append(
            f"| {n} | {beta} | {bits} | {excess:.4f} | {index_split:.4f} | "
            f"{best_split:.4f} | {birthday:.3f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "collision_mitm.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
