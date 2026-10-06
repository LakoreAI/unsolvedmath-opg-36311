#!/usr/bin/env python3
"""R13a: compress-then-MITM on planted structured families vs plain MITM.

For each instance the exact answer of ``meet_in_middle`` is compared with
``solve_compressed`` (correctness), and the number of states each touches is
reported. Targets: ``support`` (solution = the hidden structured support) and
``mixed`` (solution = a uniformly random half of all inputs, mixing structured and
random elements). Families: distinct weight-3 low-rank supports and rank-``d``
GAP supports (random decoys), plus a fully random control (no structure).

Writes docs/analysis/2026-10-06/subset-sum/compress_eval.md.
"""

import argparse
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from high_energy import build  # noqa: E402
from relation_detect import build_distinct  # noqa: E402

from src.compress_mitm import solve_compressed  # noqa: E402
from src.subset_sum import meet_in_middle  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
CONFIGS = (
    ("distinct", 24, 7),
    ("distinct", 24, 8),
    ("distinct", 24, 10),
    ("distinct", 32, 10),
    ("distinct", 32, 12),
    ("gap", 32, 3),
    ("gap", 32, 4),
    ("gap", 32, 8),
    ("random", 24, 0),
    ("random", 32, 0),
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| family | n | d | target | strategy | core | distinct sums of core | "
        "compress states | MITM states | speedup | exact |",
        "| :-- | ---: | ---: | :-- | :-- | ---: | ---: | ---: | ---: | ---: | :-- |",
    ]
    for kind, n, d in CONFIGS:
        rng = random.Random(args.seed + n * 100 + d)
        if kind == "distinct":
            values, support, target_support = build_distinct(n, d, rng)
        elif kind == "gap":
            values, support, target_support = build(n, d, 2, rng)
        else:
            values = [rng.randrange(1, 1 << n) for _ in range(n)]
            support = rng.sample(range(n), n // 2)
            target_support = sum(values[i] for i in support)
        mixed = sum(values[i] for i in rng.sample(range(n), n // 2))
        for label, target in (("support", target_support), ("mixed", mixed)):
            got = solve_compressed(values, target)
            ref = meet_in_middle(values, target)
            exact = (got.indices is None) == (ref.indices is None) and (
                got.indices is None or sum(values[i] for i in got.indices) == target
            )
            rows.append(
                f"| {kind} | {n} | {d} | {label} | {got.strategy} | {got.core_size} | "
                f"{got.sigma_size} | {got.states} | {ref.states} | "
                f"{ref.states / got.states:.1f} | {exact} |"
            )
            print(rows[-1], flush=True)
    lines = [
        "# R13a: compress-then-MITM versus plain meet-in-the-middle",
        "",
        "`states` counts dictionary entries touched. The solver is exact whatever core "
        "the relation detector returns; the core only changes speed. `speedup` is "
        "`MITM states / compress states`. The `random` control has no structure and "
        "must fall back to plain MITM (speedup 1.0).",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "compress_eval.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
