#!/usr/bin/env python3
"""R8: the balanced sub-solver bottleneck of the representation technique.

The HGJ/BCJ representation writes a solution x (weight n/2) as y + z with
y, z in {-1,0,1}^n (entries summing to x). Pick a parameter alpha: y and z each
carry (1/4+alpha)n ones and alpha n minus-ones. The modulus M is set to the
number of representations N_D, and the algorithm:

  1. sub-enumerates the partial solutions with the given coefficient counts and
     a fixed residue mod M, using a balanced meet-in-the-middle;
  2. matches the two sides on the exact target.

In units of n (base-2 exponents):

  H(alpha)   = H3(1/4+a, a, 3/4-2a)          per-element entropy of a side
  E_sub      = H/2                            balanced sub-enumeration cost
  N_D        = 1/2 + H3(2a, 2a, 1-4a)/2       representation count (alpha=0 -> 2^(n/2))
  L          = H - N_D                        solutions per side
  total      = max(E_sub, L, 2L - N_D)        + merge pre-filter term

alpha=0 is the {0,1} HGJ case. The script finds the alpha minimising the total
for this *balanced-MITM* sub-solver, which shows whether adding {-1,0,1} helps
the naive sub-solver at all.

Writes docs/analysis/2026-10-03/subset-sum/sub_solver.md.
"""

import argparse
import math
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"


def H3(parts):
    total = 0.0
    for p in parts:
        if p > 0:
            total -= p * math.log2(p)
    return total


def exponents(alpha):
    side = H3((1 / 4 + alpha, alpha, 3 / 4 - 2 * alpha))
    e_sub = side / 2
    n_d = 1 / 2 + H3((2 * alpha, 2 * alpha, 1 - 4 * alpha)) / 2
    l_exp = side - n_d
    merge = max(l_exp, 2 * l_exp - n_d)
    total = max(e_sub, merge)
    return e_sub, n_d, l_exp, merge, total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    steps = 250
    best = None
    rows = []
    for i in range(steps + 1):
        alpha = (1 / 8) * i / steps
        e_sub, n_d, l_exp, merge, total = exponents(alpha)
        rows.append((alpha, e_sub, n_d, l_exp, merge, total))
        if best is None or total < best[-1]:
            best = (alpha, e_sub, n_d, l_exp, merge, total)

    alpha0 = exponents(0.0)
    # multi-part feasibility: for 2^t equal parts of weight n/2^(t+1), the
    # representation count is 2^(t n/2); feasible only if C(n, w) >= that.
    parts_feasible = []
    for t in range(1, 5):
        w_frac = 1 / 2 ** (t + 1)
        candidate_exp = H3((w_frac, 1 - w_frac))
        parts_feasible.append((t, candidate_exp, t / 2))

    lines = [
        "# R8: the balanced sub-solver bottleneck",
        "",
        "Base-2 exponents per `n` for the representation technique with a",
        "balanced meet-in-the-middle sub-solver. `E_sub` = sub-enumeration,",
        "`L` = solutions per side, `total = max(E_sub, merge)`.",
        "",
        "| alpha | E_sub | N_D | L | merge | total |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for alpha, e_sub, n_d, l_exp, merge, total in rows[::10]:
        lines.append(
            f"| {alpha:.4f} | {e_sub:.4f} | {n_d:.4f} | {l_exp:.4f} | "
            f"{merge:.4f} | {total:.4f} |"
        )
    lines += [
        "",
        f"`alpha = 0` (the `{{0,1}}` HGJ case): E_sub = {alpha0[0]:.4f}, "
        f"L = {alpha0[2]:.4f}, total = {alpha0[4]:.4f}.",
        f"Minimum total over alpha: {best[5]:.4f} at alpha = {best[0]:.4f} "
        f"(E_sub = {best[1]:.4f}, L = {best[3]:.4f}, merge = {best[4]:.4f}).",
        "",
        "Multi-part feasibility for `{{0,1}}` (part weight `n/2^(t+1)`, "
        "representation count `2^(t n/2)`):",
        "",
        "| parts 2^t | C(n,w) exponent | representation exponent | feasible |",
        "| ---: | ---: | ---: | --- |",
    ]
    for t, cand, rep in parts_feasible:
        lines.append(
            f"| {2**t} | {cand:.4f} | {rep:.4f} | {'yes' if cand >= rep else 'no'} |"
        )
    lines += [
        "",
        "Reading: within the balanced-MITM model the total is minimised at",
        "`alpha = 0`, i.e. adding `{-1,0,1}` does *not* help the naive sub-solver",
        "— the larger `{-1,0,1}` candidate space dominates. The published",
        "`0.291n` / `0.337n` bounds therefore require a better sub-solver than",
        "balanced meet-in-the-middle, which is exactly the open gap.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "sub_solver.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'sub_solver.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
