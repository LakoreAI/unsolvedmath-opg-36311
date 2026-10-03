#!/usr/bin/env python3
"""R20: can residue-class sampling find collisions in the hard band?

R19 showed that at density about 1 many subsets share a sum, yet plain
birthday sampling needs about 2^(0.55n) samples. Jin-Wu's large-d idea for
PESS samples only one class B_r = {S : w(S) = r mod p} for a random prime p.
Equal sums always share a class, so B_r keeps about C2/p colliding pairs while
being p times smaller. Predicted cost, with C2 = sum_t f_t (f_t - 1):

    p + 2^n / sqrt(p * C2),  minimised at p ~ (4^n / C2)^(1/3),

i.e. about (2^n / sqrt(C2))^(2/3): two thirds of the plain birthday exponent.
This script runs the method on random inputs and compares measured cost with
the prediction. It finds equal-sum pairs, not subset-sum solutions.

Writes docs/analysis/2026-10-03/subset-sum/bucket_collisions.md.
"""

import argparse
from collections import Counter
import math
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.equal_subset_sum import (  # noqa: E402
    _backtrack_rank,
    _random_prime,
    _residue_counts,
)

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 20, 24)
BETAS = (0.9, 1.0, 1.1, 1.25)


def pair_count(values):
    half = len(values) // 2
    left, right = [0], [0]
    for value in values[:half]:
        left += [s + value for s in left]
    for value in values[half:]:
        right += [s + value for s in right]
    freq = Counter(u + v for u in left for v in right)
    return sum(f * (f - 1) for f in freq.values())


def bucket_search(values, modulus, rng, cap):
    """Sample random classes until two subsets share a sum; return samples."""
    values = tuple(values)
    counts = _residue_counts(values, modulus)
    samples = 0
    while samples < cap:
        residue = rng.randrange(modulus)
        size = counts[-1][residue]
        seen = {}
        for _ in range(min(size, cap)):
            mask = _backtrack_rank(
                values, counts, modulus, residue, rng.randrange(size)
            )
            samples += 1
            total = sum(v for i, v in enumerate(values) if mask >> i & 1)
            other = seen.setdefault(total, mask)
            if other != mask:
                return samples
            if samples >= cap:
                break
    return cap


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--runs", type=int, default=9)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for beta in BETAS:
            rng = random.Random(args.seed + n * 1000 + int(beta * 100))
            bits = round(beta * n)
            birthday, predicted, measured, sampled = [], [], [], []
            for _ in range(args.trials):
                values = [rng.randrange(1, 1 << bits) for _ in range(n)]
                pairs = pair_count(values)
                if pairs == 0:
                    continue
                birthday.append(math.log2((1 << n) / math.sqrt(pairs)) / n)
                lower = max(2, round((4**n / pairs) ** (1 / 3)))
                predicted.append(math.log2(2 * lower) / n)
                runs = []
                for _ in range(args.runs):
                    modulus = _random_prime(rng, lower)
                    samples = bucket_search(values, modulus, rng, 1 << n)
                    runs.append((modulus + samples, samples))
                runs.sort()
                cost, samples = runs[len(runs) // 2]
                measured.append(math.log2(cost) / n)
                sampled.append(math.log2(samples) / n)
            if measured:
                rows.append(
                    (
                        n,
                        beta,
                        len(measured),
                        *(
                            sum(c) / len(c)
                            for c in (birthday, predicted, measured, sampled)
                        ),
                    )
                )
                print(*rows[-1])

    lines = [
        "# R20: residue-class sampling for collisions",
        "",
        f"Random numbers of `round(beta*n)` bits; `inputs` with at least one "
        f"collision out of {args.trials}; median over {args.runs} runs per input. "
        "Columns are exponents `e` (cost about `2^(e*n)`): plain birthday sampling, "
        "the predicted class-sampling cost `2p`, the measured cost `p + samples` "
        "(classes plus samples, without the polynomial `n` factor of the residue "
        "table), and the samples alone. Meet-in-the-middle is `0.5`.",
        "",
        "| n | beta | inputs | birthday e | predicted e | measured e | samples e |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, beta, count, birthday, predicted, measured, sampled in rows:
        lines.append(
            f"| {n} | {beta} | {count} | {birthday:.3f} | {predicted:.3f} | "
            f"{measured:.3f} | {sampled:.3f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "bucket_collisions.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
