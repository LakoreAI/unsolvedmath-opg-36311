#!/usr/bin/env python3
"""R10: can algebraic methods beat the sub-solver floor?

The sub-solver must *find* a weight-(n/4) subset y with a.y = R (mod 2^(n/2)).
Counting is easy: a DP over (cardinality, residue mod 2^m) costs O(n^2 2^m).
Finding the planted element is a search problem. This compares the base-2
exponents (per n) of the candidate methods:

  * balanced meet-in-the-middle (R8): h(1/4)/2 = 0.4056
  * full-residue cardinality DP:  2^(n/2) states           = 0.5
  * FFT / group-algebra product:   >= 2^(n/2)                = 0.5
  * coarse DP (mod 2^m) + rejection sampling a fine-residue element:
        max(n^2 2^m, n 2^(n/2-m)), minimised at m=n/4       = 0.25
    ... but this returns a *random* element of the residue class, not the
    planted one.
  * finding the planted element by uniform sampling: needs the full residue
    distribution to sample uniformly, so >= 0.5.

The gap is counting vs finding: counting the class is cheap, but no method
samples the planted element in sub-linear-in-class-size time. This is the
concrete open problem; it mirrors the #P-vs-search gap.

Writes docs/analysis/2026-10-03/subset-sum/algebraic_sub_solver.md.
"""

import argparse
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"


def h2(p):
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    balanced_mitm = h2(1 / 4) / 2
    full_dp = 0.5
    coarse = 0.25  # m = n/4 balances the DP and the rejection sampling
    find_planted = 0.5  # uniform sampling needs the full residue distribution

    methods = [
        ("balanced meet-in-the-middle (R8)", f"{balanced_mitm:.4f}", "finds all of Y"),
        ("full-residue cardinality DP", f"{full_dp:.4f}", "counting, not finding"),
        ("FFT / group-algebra product", f"{full_dp:.4f}", "counting, not finding"),
        (
            "coarse DP + rejection sample",
            f"{coarse:.4f}",
            "random element, not the planted one",
        ),
        (
            "find planted element (uniform)",
            f"{find_planted:.4f}",
            "needs full distribution",
        ),
    ]

    lines = [
        "# R10: algebraic methods and the sub-solver floor",
        "",
        "Base-2 exponent per `n` to find a weight-`n/4` subset with",
        "`a.y = R (mod 2^(n/2))`.",
        "",
        "| method | exponent | what it returns |",
        "| --- | ---: | --- |",
    ]
    lines += [f"| {name} | {exp} | {ret} |" for name, exp, ret in methods]
    lines += [
        "",
        "Reading: counting the residue class is cheap (DP / FFT need only the",
        "full residue space, ~`2^(0.5n)`, already above the balanced MITM",
        f"`{balanced_mitm:.4f}n`). A coarse DP plus rejection sampling returns a",
        "*random* element in `0.25n`, but the algorithm needs the planted element",
        "(the unique surviving decomposition, R9), and sampling uniformly from the",
        "residue class requires the full `2^(n/2)` distribution. So the",
        "counting-vs-finding gap blocks the algebraic route: none of these",
        f"methods beats the balanced-MITM floor `{balanced_mitm:.4f}n` while",
        "producing the needed element.",
        "",
        "Open problem (unchanged after R8-R10): a sub-solver that finds the",
        "planted weight-`n/4` modular subset faster than `2^(0.4056n)`, or a",
        "conditional lower bound showing it is hard (e.g. a reduction from",
        "modular subset sum / k-SUM / lattice problems).",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "algebraic_sub_solver.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'algebraic_sub_solver.md'}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
