#!/usr/bin/env python3
"""R15: measured list sizes of the three-level BCJ tree vs BCJ's model.

For each instance, runs ``bcj_tree_attempt`` with fresh random residues and
compares mean measured list sizes with the model sizes of Sect. 3.3:
``L_w = N_w/M_w``, ``L_k = N_k/(M_w M_k)``, ``L_n = N_n/(M_w M_k M_n)`` where
``N_x`` is the number of vectors with profile ``x``. It also reports the
per-attempt success probability (an attempt succeeds when the golden solution
survives the random residues). Toy ``n`` only (``n = 16, 32``).

Writes docs/analysis/2026-10-06/subset-sum/bcj_tree_lists.md.
"""

import argparse
import random
import sys
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.bcj_tree import (  # noqa: E402
    TreeParams,
    _leaf_buckets,
    bcj_tree_attempt,
    tree_moduli,
)

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
CONFIGS = ((16, 2, 1, 0), (32, 2, 1, 0))
ATTEMPTS = 300
INSTANCES = 3


def ambient(n: int, ones: int, minus: int) -> int:
    return comb(n, ones) * comb(n - ones, minus)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| n | (a,b,g) | moduli | level | model size | measured mean | ratio |",
        "| ---: | :-- | :-- | :-- | ---: | ---: | ---: |",
    ]
    succ_rows = [
        "| n | (a,b,g) | attempts | successes | per-attempt success |",
        "| ---: | :-- | ---: | ---: | ---: |",
    ]
    for n, a, b, g in CONFIGS:
        params = TreeParams(n, a, b, g)
        moduli = tree_moduli(params)
        m_w, m_k, m_n = moduli
        model = {
            "leaf": ambient(n, params.omega.ones, params.omega.minus) / m_w,
            "kappa": ambient(n, params.kappa.ones, params.kappa.minus) / (m_w * m_k),
            "nu": ambient(n, params.nu.ones, params.nu.minus) / (m_w * m_k * m_n),
        }
        sums = {"leaf": 0.0, "kappa": 0.0, "nu": 0.0}
        count = 0
        wins = 0
        for inst in range(INSTANCES):
            rng = random.Random(args.seed + n * 10 + inst)
            values = [rng.randrange(1, 1 << n) for _ in range(n)]
            support = rng.sample(range(n), n // 2)
            target = sum(values[i] for i in support)
            buckets = _leaf_buckets(values, params.omega, m_w)
            for _ in range(ATTEMPTS):
                solution, stats = bcj_tree_attempt(
                    values, target, params, moduli, rng, buckets
                )
                wins += solution is not None
                sums["leaf"] += sum(stats.leaf) / 8
                sums["kappa"] += sum(stats.kappa) / 4
                sums["nu"] += sum(stats.nu) / 2
                count += 1
        for level in ("leaf", "kappa", "nu"):
            mean = sums[level] / count
            rows.append(
                f"| {n} | ({a},{b},{g}) | {moduli} | {level} | {model[level]:.1f} | "
                f"{mean:.1f} | {mean / model[level]:.2f} |"
            )
            print(rows[-1], flush=True)
        succ_rows.append(
            f"| {n} | ({a},{b},{g}) | {count} | {wins} | {wins / count:.3f} |"
        )
        print(succ_rows[-1], flush=True)

    lines = [
        "# R15: three-level BCJ tree, measured vs modelled list sizes",
        "",
        "Planted weight-`n/2` solutions, random `n`-bit values, fresh random "
        "residues per attempt (`300` attempts x `3` instances). Model sizes are "
        "BCJ Sect. 3.3 (`N_x / prod M`); `N_x` counts vectors of profile `x`. "
        "The `kappa`/`nu` model ignores the consistency filter, so measured sizes "
        "are expected to sit below it (BCJ call it an upper bound).",
        "",
        *rows,
        "",
        "## Per-attempt success",
        "",
        *succ_rows,
        "",
        "Toy sizes only: the exponent curve (`0.291n`) is asymptotic and cannot be "
        "read off `n <= 32`.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "bcj_tree_lists.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
