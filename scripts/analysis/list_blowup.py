#!/usr/bin/env python3
"""R13: does the filtered list blow up on structured inputs?

Mixing is only the lower half of the cost story: if the filtered sub-solver
output ``|Y_r|`` is much larger than its random-input expectation
``ambient / M``, the follow-up disjointness match pays for it. This script
measures ``|Y_r| / E`` for the balanced weight-``n/4`` sub-solver, with a random
prime ``M`` from ``[P, 2P]`` (``P ~ C(n/4,n/8)^2``) and random residues, over
the adversarial families of ``hgj_adversarial.py`` plus two new ones that target
the modulus: ``near-ap`` (small common difference) and ``mod-cluster``
(``a_i = q b_i + r_i`` with ``q`` a prime near ``P``, so values cluster mod a
prime in the window).

Writes docs/analysis/2026-10-05/subset-sum/list_blowup.md.
"""

import argparse
import random
import sys
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hgj_adversarial import FAMILIES, make_family, next_prime  # noqa: E402

from src.hgj import weight_residue_subsets  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-05" / "subset-sum"
SIZES = (24, 32, 40)
EXTRA = ("near-ap", "mod-cluster")


def family(name: str, n: int, rng: random.Random, window: int) -> list[int]:
    if name == "near-ap":
        base = rng.randrange(1, 1 << n)
        return [base + i * rng.randrange(1, 4) for i in range(n)]
    if name == "mod-cluster":
        q = next_prime(window + rng.randrange(window))
        return [
            q * rng.randrange(1, 1 << (n // 2)) + rng.randrange(0, 8) for _ in range(n)
        ]
    return make_family(name, n, rng)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| n | family | E = ambient/M | mean ratio | max ratio |",
        "| ---: | :-- | ---: | ---: | ---: |",
    ]
    for n in SIZES:
        window = comb(n // 4, n // 8) ** 2
        ambient = comb(n // 2, n // 8) ** 2
        for name in (*FAMILIES, *EXTRA):
            ratios = []
            expected = 0.0
            for trial in range(3):
                rng = random.Random(args.seed + n * 31 + trial)
                values = family(name, n, rng, window)
                for _ in range(4):
                    modulus = next_prime(window + rng.randrange(window))
                    expected = ambient / modulus
                    for _ in range(3):
                        r = rng.randrange(modulus)
                        size = len(weight_residue_subsets(values, n // 4, modulus, r))
                        ratios.append(size / expected)
            mean = sum(ratios) / len(ratios)
            rows.append(
                f"| {n} | {name} | {expected:.1f} | {mean:.2f} | {max(ratios):.1f} |"
            )
            print(rows[-1], flush=True)

    lines = [
        "# R13: filtered-list blow-up on structured inputs",
        "",
        "`ratio = |Y_r| / E` where `Y_r` is the balanced weight-`n/4` sub-solver "
        "output for a random prime `M in [P, 2P]` (`P = C(n/4,n/8)^2`) and a random "
        "residue, and `E = C(n/2,n/8)^2 / M` its expectation on random inputs. "
        "Ratio `~1` = no blow-up; a large mean or max ratio is a cost the "
        "disjointness step must absorb.",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "list_blowup.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
