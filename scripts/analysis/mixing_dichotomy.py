#!/usr/bin/env python3
"""R13 probe: does poor representation mixing coincide with additive structure?

The Randolph-Wegrzycki worst-case framework needs a mixing dichotomy: if the
HGJ representation sums `a . w` (over weight-`n/4` vectors `a`) do not spread
across residues modulo a prime `p ~ C(n/2, n/4)`, then the input has "some other
useful property". For coefficient sets with a 0 they use unbalanced solutions;
for the target problem `x . w = t`, the candidate property is additive structure
(small doubling), which makes subset sum easy (Randolph-Wegrzycki, small
doubling).

This script measures, for adversarial families, the representation coverage
(distinct residues / min(p, C(n, n/4))) against the doubling constant
`|A+A| / n`. The dichotomy is supported when the only low-coverage families are
structured (small doubling) ones; a low-coverage *dissociated* family would be a
counterexample.

Writes docs/analysis/2026-10-05/subset-sum/mixing_dichotomy.md.
"""

import argparse
import math
import random
import sys
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (16, 20)
FAMILIES = (
    "constant",
    "geometric",
    "arithmetic",
    "random-small",
    "random-large",
    "sidon",
)


def next_prime(lower: int) -> int:
    candidate = max(2, lower)
    while any(candidate % d == 0 for d in range(2, int(candidate**0.5) + 1)):
        candidate += 1
    return candidate


def make_family(name: str, n: int, rng: random.Random) -> list[int]:
    if name == "constant":
        return [1] * n
    if name == "geometric":
        return [1 << i for i in range(n)]
    if name == "arithmetic":
        return list(range(1, n + 1))
    if name == "random-small":
        return [rng.randrange(1, 1 << max(1, n // 2)) for _ in range(n)]
    if name == "random-large":
        return [rng.randrange(1, 1 << (2 * n)) for _ in range(n)]
    if name == "sidon":
        # A Sidon-like set: all pairwise sums (and differences) are distinct.
        base = sorted(rng.sample(range(1, 1 << (3 * n)), n))
        while len(set(a + b for a in base for b in base)) != n * (n + 1) // 2:
            base = sorted(rng.sample(range(1, 1 << (3 * n)), n))
        return base
    raise ValueError(name)


def representation_coverage(values: list[int], rng: random.Random) -> float:
    """Coverage of a planted balanced solution's HGJ representations mod p.

    A weight-`n/2` solution `x` has `C(n/2, n/4)` representations `y + (x-y)`
    with `|y| = n/4`. With `p ~ C(n/2, n/4)`, a random residue class retains one
    representation iff the sums `y . w` spread; this is the mixing condition.
    """
    n = len(values)
    weight = max(1, n // 4)
    reps = math.comb(n // 2, weight) if n >= 4 else 1
    modulus = next_prime(max(2, reps))
    solution = sorted(rng.sample(range(n), n // 2))
    distinct = {
        sum(values[solution[i]] for i in comb) % modulus
        for comb in combinations(range(len(solution)), weight)
    }
    return len(distinct) / modulus


def doubling_constant(values: list[int]) -> float:
    sums = {a + b for a in values for b in values}
    return len(sums) / len({*values})


def is_dissociated(values: list[int]) -> bool:
    sums = {0}
    for value in values:
        sums |= {s + value for s in sums}
    return len(sums) == (1 << len(values))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        for family in FAMILIES:
            rng = random.Random(args.seed + n * 10 + len(family))
            values = make_family(family, n, rng)
            coverage = representation_coverage(values, rng)
            doubling = doubling_constant(values)
            dissociated = is_dissociated(values)
            rows.append((n, family, coverage, doubling, dissociated))
            print(*rows[-1])

    lines = [
        "# R13 probe: representation mixing vs additive structure",
        "",
        "`coverage` is the fraction of residues mod `p ~ C(n/2, n/4)` hit by the "
        "HGJ sums `y . w` over the `C(n/2, n/4)` weight-`n/4` representations `y` "
        "of a planted weight-`n/2` solution; `doubling` is `|A+A| / n`; "
        "`dissociated` is `|S(A)| = 2^n` (not by itself a hardness proxy: powers "
        "of two are dissociated and easy). The candidate mixing dichotomy for the "
        "target problem says low coverage should coincide with additive structure "
        "(small doubling or superincreasing), so a random residue still retains a "
        "representation; only such structured inputs may mix poorly.",
        "",
        "| n | family | coverage | doubling | dissociated |",
        "| ---: | :-- | ---: | ---: | :-- |",
    ]
    for n, family, coverage, doubling, dissociated in rows:
        lines.append(
            f"| {n} | {family} | {coverage:.3f} | {doubling:.2f} | "
            f"{'yes' if dissociated else 'no'} |"
        )
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "mixing_dichotomy.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
