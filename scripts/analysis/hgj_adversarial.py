#!/usr/bin/env python3
"""R13: does the full HGJ filter survive adversarial families, and at what cost?

Step 2 of the attack: run the complete pipeline (balanced weight-`n/8` sub-solver
per half, modular filter, disjointness + exact-sum match) on planted balanced
solutions across adversarial families, and measure (a) the fraction of instances
solved within a small number of residues, (b) the enumeration work exponent
(against the sub-solver baseline `2*C(n/2, n/8) = 2^{0.4057n}` and MITM `0.5`),
and (c) the representation coverage for a random prime. A family that is both
hard (large distinct-sum count, no gcd, not superincreasing) and low-coverage
would be the adversarial poorly-mixing instance; otherwise the barrier is the
sub-solver.

Writes docs/analysis/2026-10-05/subset-sum/hgj_adversarial.md.
"""

import argparse
import math
import random
import sys
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hgj import enumerated_size, hgj_search  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (24, 32, 40)
FAMILIES = (
    "random-b1.0",
    "random-b1.5",
    "geometric",
    "arithmetic-large",
    "two-scale",
    "gap-rank2",
    "q-multiple",
)
TRIALS = 6
RESIDUE_BUDGET = 16


def next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def make_family(name: str, n: int, rng: random.Random) -> list[int]:
    if name == "random-b1.0":
        return [rng.randrange(1, 1 << n) for _ in range(n)]
    if name == "random-b1.5":
        return [rng.randrange(1, 1 << (3 * n // 2)) for _ in range(n)]
    if name == "geometric":
        return [1 << i for i in range(n)]
    if name == "arithmetic-large":
        start = rng.randrange(1, 1 << n)
        step = rng.randrange(1, 1 << (n // 2))
        return [start + i * step for i in range(n)]
    if name == "two-scale":
        # a_i = q * b_i + r_i with q a product of a few primes near 2^{n/2}.
        q = 1
        for _ in range(3):
            q *= next_prime(rng.randrange(1 << (n // 2), 1 << (n // 2 + 3)))
        return [
            q * rng.randrange(1, 1 << (n // 2)) + rng.randrange(0, 1 << (n // 3))
            for _ in range(n)
        ]
    if name == "gap-rank2":
        d1 = rng.randrange(1, 1 << (n // 2))
        d2 = rng.randrange(1, 1 << (n // 2))
        base = rng.randrange(1, 1 << n)
        return [
            base + (i % 5) * d1 + (i // 5) * d2 + rng.randrange(0, 1 << (n // 4))
            for i in range(n)
        ]
    if name == "q-multiple":
        q = next_prime(1 << (n // 2))
        return [q * i + rng.randrange(0, q // (2 * n) + 1) for i in range(1, n + 1)]
    raise ValueError(name)


def planted(n: int, rng: random.Random):
    half = n // 2
    indices = set(rng.sample(range(half), n // 4)) | set(
        rng.sample(range(half, n), n // 4)
    )
    return sorted(indices)


def coverage(values, support, weight, modulus) -> float:
    residues = {
        sum(values[support[i]] for i in comb) % modulus
        for comb in combinations(range(len(support)), weight)
    }
    return len(residues) / modulus


def distinct_ratio(values) -> float:
    sums = {0}
    for value in values:
        sums |= {s + value for s in sums}
    return len(sums) / (1 << len(values))


def gcd_all(values) -> int:
    result = 0
    for value in values:
        result = math.gcd(result, value)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        weight = n // 4
        reps = math.comb(n // 4, n // 8) ** 2 if n % 8 == 0 else 1 << (n // 2)
        modulus = next_prime(max(2, reps))
        baseline = enumerated_size(n, weight)  # 2*C(n/2, n/8)
        for family in FAMILIES:
            successes = 0
            cov = []
            work = []
            for trial in range(TRIALS):
                rng = random.Random(args.seed + n * 100 + trial + len(family))
                values = make_family(family, n, rng)
                support = planted(n, rng)
                target = sum(values[i] for i in support)
                result = hgj_search(
                    values, target, weight=n // 2, residues=RESIDUE_BUDGET, seed=trial
                )
                if result.feasible:
                    successes += 1
                    work.append(result.enumerated)
                cov.append(coverage(values, support, weight, modulus))
            rows.append(
                (
                    n,
                    family,
                    successes / TRIALS,
                    sum(cov) / len(cov),
                    min(cov),
                    sum(work) / len(work) if work else float("nan"),
                    baseline,
                )
            )
            print(*rows[-1])

    lines = [
        "# R13: HGJ filter + sub-solver on adversarial families",
        "",
        f"Planted balanced solutions; up to {RESIDUE_BUDGET} residue attempts. "
        "`success` is the fraction solved, `cov avg`/`cov min` the representation "
        "coverage over several primes, `work` the mean enumeration (the sub-solver "
        "baseline is `2*C(n/2,n/8) = 2^0.4057n`; MITM is `0.5`). Prediction: hard "
        "families mix (coverage `~0.5`) and succeed; low-coverage families are "
        "structured, not hard.",
        "",
        "| n | family | success | cov avg | cov min | work | baseline |",
        "| ---: | :-- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, family, success, cov_avg, cov_min, work, baseline in rows:
        work_str = f"{work:.3e}" if work == work else "—"
        lines.append(
            f"| {n} | {family} | {success:.2f} | {cov_avg:.3f} | {cov_min:.3f} | "
            f"{work_str} | {baseline} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "hgj_adversarial.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
