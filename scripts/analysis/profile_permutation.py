#!/usr/bin/env python3
"""R13: the profile barrier is polynomial, not exponential.

``NEXT.md`` (Sect. 3.2) identified profile completeness as the barrier: the
balanced sub-solver only sees solutions with exactly ``w/2`` support elements in
each half, and enumerating all profiles costs ``2^(0.811n)``. That remedy is not
needed. A uniformly random permutation of the inputs puts a weight-``w`` support
balanced with probability ``C(n/2,w/2)^2 / C(n,w) = Theta(1/sqrt(n))`` (for
``w = n/2``), so ``O(sqrt(n))`` permutations -- a polynomial factor -- repair
completeness. This script (a) tabulates the exact probability and the number of
permutations for 99% coverage, (b) checks the formula against sampled
permutations, (c) runs the real search on concentrated solutions with a
permutation budget, and (d) re-runs the adversarial families with a prime
modulus in place of the power-of-two default, to separate the profile effect
from the modulus effect.

Writes docs/analysis/2026-10-06/subset-sum/profile_permutation.md.
"""

import argparse
import random
import sys
from math import ceil, comb, log, sqrt
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hgj_adversarial import FAMILIES, make_family, next_prime  # noqa: E402

from src.hgj import balanced_probability, hgj_permuted_search  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def formula_table(rng: random.Random) -> list[str]:
    rows = [
        "| n | w | exact p | p*sqrt(n) | sampled p | perms for 99% |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n in (16, 32, 64, 128, 256, 1024):
        for w in (n // 2, n // 4):
            exact = balanced_probability(n, w)
            hits = 0
            samples = 20000
            for _ in range(samples):
                support = rng.sample(range(n), w)
                first = sum(1 for i in support if i < n // 2)
                hits += first == w // 2
            perms = ceil(log(100) / -log(1 - exact)) if exact < 1 else 1
            rows.append(
                f"| {n} | {w} | {exact:.4f} | {exact * sqrt(n):.3f} | "
                f"{hits / samples:.4f} | {perms} |"
            )
    return rows


def concentrated_table(seed: int) -> list[str]:
    rows = [
        "| n | first-half share | perm budget | success | mean work | MITM work |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    trials = 8
    for n in (24, 32):
        half = n // 2
        budget = ceil(4 * sqrt(n))
        for share in (0, half // 4, half // 2):
            wins = 0
            work = 0
            for t in range(trials):
                rng = random.Random(seed + n * 1000 + share * 10 + t)
                values = [rng.randrange(1, 1 << n) for _ in range(n)]
                support = rng.sample(range(half), share) + rng.sample(
                    range(half, n), half - share
                )
                target = sum(values[i] for i in support)
                result = hgj_permuted_search(
                    values, target, permutations=budget, residues=16, seed=t
                )
                wins += result.feasible
                work += result.enumerated
            rows.append(
                f"| {n} | {share} | {budget} | {wins / trials:.2f} | "
                f"{work / trials:.0f} | {2 ** (n // 2)} |"
            )
    return rows


def modulus_table(seed: int) -> list[str]:
    rows = [
        "| n | family | pow2 success | pow2 work | prime success | prime work |",
        "| ---: | :-- | ---: | ---: | ---: | ---: |",
    ]
    trials = 6
    for n in (24, 32):
        budget = ceil(3 * sqrt(n))
        reps = comb(n // 4, n // 8) ** 2
        pow2 = 1 << max(1, reps.bit_length() - 1)
        prime = next_prime(pow2)
        for family in FAMILIES:
            stats = {}
            for label, modulus in (("pow2", pow2), ("prime", prime)):
                wins = work = 0
                for t in range(trials):
                    rng = random.Random(seed + n * 100 + t)
                    values = make_family(family, n, rng)
                    support = rng.sample(range(n), n // 2)  # uniform, not balanced
                    target = sum(values[i] for i in support)
                    result = hgj_permuted_search(
                        values,
                        target,
                        permutations=budget,
                        residues=8,
                        seed=t,
                        modulus=modulus,
                    )
                    wins += result.feasible
                    work += result.enumerated
                stats[label] = (wins / trials, work / trials)
            rows.append(
                f"| {n} | {family} | {stats['pow2'][0]:.2f} | "
                f"{stats['pow2'][1]:.3g} | {stats['prime'][0]:.2f} | "
                f"{stats['prime'][1]:.3g} |"
            )
            print(rows[-1])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    lines = [
        "# R13: the profile barrier is polynomial",
        "",
        "Correction to `NEXT.md` Sect. 3.2. A random permutation balances a "
        "weight-`w` support with probability `C(n/2,w/2)^2/C(n,w)`; at `w=n/2` "
        "this is `Theta(1/sqrt(n))`, "
        "so `O(sqrt n)` permutations restore completeness. The `2^(0.811n)` "
        "all-profiles enumeration is unnecessary.",
        "",
        "## Exact probability vs sampling",
        "",
        *formula_table(rng),
        "",
        "## Real search on concentrated solutions",
        "",
        "Planted weight-`n/2` solutions with a controlled first-half share, "
        "random `n`-bit values, `hgj_permuted_search` (first attempt keeps the "
        "natural order). Compare `hgj_profile.md`, where one permutation at 4 "
        "trials gave 0-0.5.",
        "",
        *concentrated_table(args.seed),
        "",
        "## Power-of-two vs prime modulus on adversarial families",
        "",
        "Uniformly random weight-`n/2` supports (not balanced), permutation "
        "budget `ceil(3 sqrt n)`, 8 residues per permutation. The modulus is "
        "`2^m` (default) or the next prime above it.",
        "",
        *modulus_table(args.seed),
        "",
        "Work is total enumerated subsets across permutations and residues.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "profile_permutation.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
