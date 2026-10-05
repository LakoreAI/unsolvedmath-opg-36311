#!/usr/bin/env python3
"""R13: average collision energy over primes (the candidate mixing lemma).

For a planted balanced solution's `weight-n/4` representation sums, this script
measures the collision energy `E_p = sum_r c_r^2` and the coverage `s_p / p`
across every prime `p` in `[Y, 2Y]` (`Y = C(n/2, n/4)`), and compares the average
`E_p` with the elementary bound `E_inf + Y^2 * 2beta / pi`. The bound is the
candidate proof that a random prime mixes; the pointwise minimum coverage is the
counterexample-hunting quantity (see NEXT.md).

Writes docs/analysis/2026-10-03/subset-sum/average_energy.md.
"""

import argparse
from collections import Counter
from itertools import combinations
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 20, 22)


def next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def primes_upto(limit: int) -> list[int]:
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(2, limit + 1) if sieve[i]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        rng = random.Random(args.seed + n)
        half, weight = n // 2, n // 4
        values = [rng.randrange(1, 1 << n) for _ in range(n)]
        support = sorted(rng.sample(range(n), half))
        reps = [
            sum(values[support[i]] for i in c)
            for c in combinations(range(half), weight)
        ]
        total = len(reps)
        exact = sum(
            1 for i in range(total) for j in range(i + 1, total) if reps[i] == reps[j]
        )
        base = next_prime(total)
        window = [p for p in primes_upto(2 * base) if p >= base]
        energies, coverages = [], []
        for prime in window:
            counts = Counter(r % prime for r in reps)
            energies.append(sum(c * c for c in counts.values()))
            coverages.append(len(counts) / prime)
        avg_energy = sum(energies) / len(energies)
        bound = exact + total * total * 2.0 / len(window)
        rows.append(
            (
                n,
                total,
                len(window),
                exact,
                avg_energy,
                bound,
                sum(coverages) / len(coverages),
                min(coverages),
            )
        )
        print(*rows[-1])

    lines = [
        "# R13: average collision energy over primes",
        "",
        "Planted balanced solution; `Y` representations of weight `n/4`. For every "
        "prime `p in [Y, 2Y]`, `E_p = sum_r c_r^2` and coverage `s_p / p`. The "
        "elementary bound is `exact + Y^2 * 2 / pi` (with `2beta = 2`); the "
        "candidate lemma says the average is `O(Y log Y)`, so a random prime "
        "mixes. `min cov` is the pointwise counterexample-hunting quantity.",
        "",
        "| n | Y | primes | exact pairs | avg E_p | bound | avg cov | min cov |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, total, count, exact, avg_e, bound, avg_c, min_c in rows:
        lines.append(
            f"| {n} | {total} | {count} | {exact} | {avg_e:.1f} | {bound:.0f} | "
            f"{avg_c:.3f} | {min_c:.3f} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "average_energy.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
