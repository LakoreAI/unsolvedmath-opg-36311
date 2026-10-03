#!/usr/bin/env python3
"""R21: do cheap collisions turn one subset-sum solution into many?

R20 found equal-sum pairs below 2^(n/2) in the hard band. A pair gives a
relation c in {-1,0,1}^n with c.a = 0. If c is compatible with a solution x
(+1 only where x_i = 0, -1 only where x_i = 1), then x + c is another solution.
For each planted input we collect collisions with the R20 class sampler within
a budget of about 2^(n/2) samples and report:

  * found       = distinct collisions collected,
  * support     = mean number of nonzero entries of c, as a fraction of n,
  * compatible  = collisions usable on the planted x (either sign of c),
  * solutions   = all subsets with the planted target sum (exact count).

A random relation with support s is compatible with probability about
2^(1-s), so the route needs collisions of small support.

Writes docs/analysis/2026-10-03/subset-sum/collision_amplification.md.
"""

import argparse
from collections import Counter
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
BETAS = (0.9, 1.0, 1.1)


def half_sums(values):
    sums = [0]
    for value in values:
        sums += [s + value for s in sums]
    return sums


def stats(values):
    half = len(values) // 2
    left, right = half_sums(values[:half]), half_sums(values[half:])
    freq = Counter(u + v for u in left for v in right)
    return freq, sum(f * (f - 1) for f in freq.values())


def collect_collisions(values, modulus, rng, budget):
    values = tuple(values)
    counts = _residue_counts(values, modulus)
    found, samples = set(), 0
    while samples < budget:
        residue = rng.randrange(modulus)
        size = counts[-1][residue]
        seen = {}
        for _ in range(min(size, budget - samples)):
            mask = _backtrack_rank(
                values, counts, modulus, residue, rng.randrange(size)
            )
            samples += 1
            total = sum(v for i, v in enumerate(values) if mask >> i & 1)
            other = seen.setdefault(total, mask)
            if other != mask:
                plus, minus = mask & ~other, other & ~mask
                found.add((min(plus, minus), max(plus, minus)))
    return found


def compatible(plus, minus, solution, full):
    forward = plus & solution == 0 and minus & (full & ~solution) == 0
    backward = minus & solution == 0 and plus & (full & ~solution) == 0
    return forward or backward


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    parser.add_argument("--trials", type=int, default=5)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        full = (1 << n) - 1
        for beta in BETAS:
            rng = random.Random(args.seed + n * 1000 + int(beta * 100))
            bits = round(beta * n)
            totals = Counter()
            for _ in range(args.trials):
                values = [rng.randrange(1, 1 << bits) for _ in range(n)]
                solution = sum(1 << i for i in rng.sample(range(n), n // 2))
                target = sum(v for i, v in enumerate(values) if solution >> i & 1)
                freq, pairs = stats(values)
                if pairs == 0:
                    continue
                lower = max(2, round((4**n / pairs) ** (1 / 3)))
                found = collect_collisions(
                    values, _random_prime(rng, lower), rng, 1 << (n // 2)
                )
                totals["inputs"] += 1
                totals["found"] += len(found)
                totals["support"] += sum(
                    (p | m).bit_count() / n for p, m in found
                ) / max(1, len(found))
                totals["compatible"] += sum(
                    compatible(p, m, solution, full) for p, m in found
                )
                totals["solutions"] += freq[target]
            k = totals["inputs"]
            if k:
                row = (
                    n,
                    beta,
                    k,
                    totals["found"] / k,
                    totals["support"] / k,
                    totals["compatible"] / k,
                    totals["solutions"] / k,
                )
                rows.append(row)
                print(*row)

    lines = [
        "# R21: do cheap collisions multiply solutions?",
        "",
        "Planted weight-n/2 solution; collisions collected by the R20 class "
        "sampler with a budget of `2^(n/2)` samples. Means over inputs with at "
        "least one collision. `support` is the fraction of nonzero entries of a "
        "collision vector; `compatible` counts collisions usable on the planted "
        "solution; `solutions` is the exact number of subsets with the target "
        "sum.",
        "",
        "| n | beta | inputs | found | support | compatible | solutions |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, beta, k, found, support, compat, sols in rows:
        lines.append(
            f"| {n} | {beta} | {k} | {found:.1f} | {support:.3f} | {compat:.2f} | "
            f"{sols:.1f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "collision_amplification.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
