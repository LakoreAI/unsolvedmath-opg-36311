#!/usr/bin/env python3
"""Brutal search for a poorly-mixing *hard* instance (a lifting counterexample).

The target mixing dichotomy needs: poor HGJ mixing for a random prime implies
additive structure. This script hammers it with adversarial constructions and
measures, for a planted balanced support, the *best* coverage over several
random primes `p in [C(n/2,n/4), 2 C(n/2,n/4)]` (the algorithm may retry), next
to structural flags. A "hard" instance (gcd 1, not superincreasing, many
distinct subset sums) with small best-coverage would refute the dichotomy.

Writes docs/analysis/2026-10-05/subset-sum/mixing_counterexample.md.
"""

import argparse
from math import comb, gcd
import random
import sys
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (18, 20)
PRIMES_PER_INSTANCE = 6
TRIALS = 6
FAMILIES = (
    "random-b0.75",
    "random-b1.0",
    "random-b1.25",
    "short-range",
    "short-ap",
    "near-geometric",
    "common-factor",
    "sidon",
)


def next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def make_family(name: str, n: int, rng: random.Random) -> list[int]:
    if name.startswith("random-b"):
        beta = float(name.split("b")[1])
        return [rng.randrange(1, max(2, 1 << round(beta * n))) for _ in range(n)]
    if name == "short-range":
        # Range about p = 2^(n/2): subset sums can collide mod p freely.
        return [rng.randrange(1, 1 << (n // 2)) for _ in range(n)]
    if name == "short-ap":
        start = rng.randrange(1, 1 << 20)
        step = rng.randrange(1, 1 << 12)
        return [start + i * step for i in range(n)]
    if name == "near-geometric":
        return [1 << i for i in range(n)]
    if name == "common-factor":
        factor = rng.randrange(2, 1 << 10)
        values = [factor * rng.randrange(1, 1 << (2 * n)) for _ in range(n)]
        values[0] += 1  # break the gcd and the superincreasing order
        return values
    if name == "sidon":
        base = sorted(rng.sample(range(1, 1 << (3 * n)), n))
        while len({a + b for a in base for b in base}) != n * (n + 1) // 2:
            base = sorted(rng.sample(range(1, 1 << (3 * n)), n))
        return base
    raise ValueError(name)


def coverage(values, support, weight, modulus) -> float:
    residues = {
        sum(values[support[i]] for i in comb) % modulus
        for comb in combinations(range(len(support)), weight)
    }
    return len(residues) / modulus


def gcd_all(values) -> int:
    result = 0
    for value in values:
        result = gcd(result, value)
    return result


def is_superincreasing(values) -> bool:
    running = 0
    for value in sorted(values):
        if value <= running:
            return False
        running += value
    return True


def distinct_sum_ratio(values) -> float:
    sums = {0}
    for value in values:
        sums |= {s + value for s in sums}
    return len(sums) / (1 << len(values))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        half = n // 2
        weight = n // 4
        reps = comb(half, weight)
        base_prime = next_prime(reps)
        for family in FAMILIES:
            best_coverages = []
            hard_best = []
            for trial in range(TRIALS):
                rng = random.Random(args.seed + n * 100 + trial * 7 + len(family))
                values = make_family(family, n, rng)
                support = sorted(rng.sample(range(n), half))
                coverages = []
                for k in range(PRIMES_PER_INSTANCE):
                    prime = next_prime(rng.randrange(base_prime, 2 * base_prime))
                    coverages.append(coverage(values, support, weight, prime))
                best = max(coverages)
                best_coverages.append(best)
                hard = (
                    gcd_all(values) == 1
                    and not is_superincreasing(values)
                    and distinct_sum_ratio(values) > 0.5
                )
                if hard:
                    hard_best.append(best)
            rows.append(
                (
                    n,
                    family,
                    sum(best_coverages) / len(best_coverages),
                    min(best_coverages),
                    len(hard_best),
                    min(hard_best) if hard_best else float("nan"),
                )
            )
            print(*rows[-1])

    lines = [
        "# Brutal search for a poorly-mixing hard instance",
        "",
        "For a random balanced support of size `n/2`, `best coverage` is the "
        "largest fraction of residues hit (`p ~ C(n/2,n/4)`) over several random "
        "primes (the algorithm may retry). A `hard` instance has `gcd 1`, is not "
        "superincreasing, and has `|S(A)|/2^n > 0.5`. A hard instance with small "
        "best coverage would refute the target mixing dichotomy.",
        "",
        "| n | family | mean best coverage | min best coverage | hard trials | min best coverage (hard) |",
        "| ---: | :-- | ---: | ---: | ---: | ---: |",
    ]
    for n, family, mean_best, min_best, hard, min_hard in rows:
        hard_str = f"{min_hard:.3f}" if min_hard == min_hard else "—"
        lines.append(
            f"| {n} | {family} | {mean_best:.3f} | {min_best:.3f} | "
            f"{hard}/{TRIALS} | {hard_str} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "mixing_counterexample.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
