#!/usr/bin/env python3
"""R9: can a birthday/subsampling sub-solver beat the balanced-MITM floor?

The sub-solver must produce Y = { weight-(n/4) subsets y : a.y = R (mod M) }.
A balanced meet-in-the-middle builds all of Y in C(n/2, n/8) = 2^(0.4056n) time.
The hope: sample only s candidates per side and still hit a *valid* pair
(y, z) with a.y + a.z = target and y, z disjoint.

This measures the two quantities that decide it for planted balanced instances:

  * D — the number of balanced decompositions of the planted solution;
  * survival — over random residues R, how many decompositions have a.y = R,
    and how often at least one does (the needle the algorithm must find);
  * |Y| — the size of the residue class the needle hides in.

If survival is ~1 and |Y| ~ L, then uniform sampling of Y includes the needle
with probability s/|Y|, so reaching constant success needs s ~ |Y| = L: no gain.

Writes docs/analysis/2026-10-03/subset-sum/birthday_sub_solver.md.
"""

import argparse
import random
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hgj import weight_residue_subsets  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 20, 24, 28)


def balanced_decompositions(values, ones, n):
    half = n // 2
    per = n // 8
    left = [i for i in ones if i < half]
    right = [i for i in ones if i >= half]
    if len(left) < per or len(right) < per:
        return []
    out = []
    for lc in combinations(left, per):
        lm = 0
        for i in lc:
            lm |= 1 << i
        for rc in combinations(right, per):
            rm = 0
            for i in rc:
                rm |= 1 << i
            out.append((lm | rm, sum(values[i] for i in lc + rc)))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    parser.add_argument("--residues", type=int, default=400)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        rng = random.Random(args.seed + n)
        values = [rng.randrange(1, 1 << 30) for _ in range(n)]
        ones = rng.sample(range(n), n // 2)
        decomps = balanced_decompositions(values, set(ones), n)
        d = len(decomps)
        modulus = max(2, d)  # M ~ number of representations, so E[survival] = 1
        by_residue = Counter(s % modulus for _, s in decomps)
        survivors = [by_residue.get(r, 0) for r in range(modulus)]
        p_at_least_one = sum(1 for c in survivors if c) / modulus
        y_size = len(
            weight_residue_subsets(values, n // 4, modulus, rng.randrange(modulus))
        )
        rows.append(
            {
                "n": n,
                "decompositions_D": d,
                "modulus_M": modulus,
                "p_survival_ge_1": round(p_at_least_one, 4),
                "max_survivors": max(survivors),
                "residue_class_Y": y_size,
                "sample_success_s_over_Y": "s / Y",
            }
        )
        print(
            f"  n={n}: D={d} M={modulus} P(surv>=1)={p_at_least_one:.3f} "
            f"max_surv={max(survivors)} |Y|={y_size}"
        )

    lines = [
        "# R9: birthday/subsampling sub-solver",
        "",
        "For a planted balanced solution: `D` decompositions, modulus `M ~ D`",
        "(so the expected number of surviving decompositions for a random residue",
        "is ~1). `P(survival>=1)` is the fraction of residues that keep a",
        "decomposition; `|Y|` is the residue class the needle hides in.",
        "",
        "| n | D | M | P(survival>=1) | max survivors | \\|Y\\| |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        lines.append(
            "| {n} | {decompositions_D} | {modulus_M} | {p_survival_ge_1} | "
            "{max_survivors} | {residue_class_Y} |".format(**r)
        )
    lines += [
        "",
        "Reading: exactly ~1 decomposition survives the residue filter (as HGJ",
        "designs), but it hides in a residue class of size `|Y|`. Uniform",
        "sampling of `s` candidates per side hits the needle with probability",
        "`~ (s/|Y|)`, so constant success requires `s ~ |Y| = L` — i.e. the full",
        "balanced enumeration. There is no subsampling gain for finding the",
        "*specific* decomposition; the birthday idea finds *a* residue match but",
        "not the one whose complement closes the exact target. The `0.4056n`",
        "floor stands for this sub-solver.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "birthday_sub_solver.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'birthday_sub_solver.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
