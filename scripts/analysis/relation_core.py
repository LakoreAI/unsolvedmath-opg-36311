#!/usr/bin/env python3
"""R13a: find the structured support by short equal-sum relations (no lattice).

For each ``s`` the script enumerates all subsets of size ``<= s`` of the ``n``
inputs, groups them by sum, and turns every pair of distinct subsets with equal sum
into a relation ``(P, Q)`` (common elements removed). The *core* is the union of
elements appearing in some relation. Cost per ``s`` is ``sum_{j<=s} C(n, j)``, so
for ``s = Theta(n)`` it is exponential, but for ``s`` below the *random noise
threshold* (relations among random ``n``-bit decoys appear only when
``C(n, s)^2 >~ 2^n``, ``s >~ 0.11 n``) every relation lives in the structured part.

Families: the rank-``d`` GAP supports of ``high_energy.build`` and the distinct
weight-3 vector supports of ``relation_detect.build_distinct`` (the family on which
LLL stopped working), always with random decoys. Reports, per ``s``, whether the
core lies inside the hidden support ``S``, its coverage ``|core|/|S|``, and the
enumeration cost.

Writes docs/analysis/2026-10-06/subset-sum/relation_core.md.
"""

import argparse
import random
import sys
from collections import defaultdict
from itertools import combinations
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from high_energy import build  # noqa: E402
from relation_detect import build_distinct  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
CONFIGS = (
    ("distinct", 24, 7),
    ("distinct", 24, 8),
    ("distinct", 24, 10),
    ("distinct", 32, 10),
    ("distinct", 32, 12),
    ("gap", 32, 8),
)


def core_at(values, smax):
    """Return {s: set(core elements)} for s = 1..smax (relations of size <= s)."""
    n = len(values)
    by_sum: dict[int, list[int]] = defaultdict(list)
    by_sum[0].append(0)
    cores = {}
    for s in range(1, smax + 1):
        for comb_idx in combinations(range(n), s):
            total = sum(values[i] for i in comb_idx)
            mask = 0
            for i in comb_idx:
                mask |= 1 << i
            by_sum[total].append(mask)
        core = 0
        for masks in by_sum.values():
            if len(masks) < 2:
                continue
            for a, b in combinations(masks, 2):
                common = a & b
                core |= (a | b) & ~common if (a ^ b) else 0
        cores[s] = {i for i in range(n) if core >> i & 1}
    return cores


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| family | n | d | s | enumerated | core size | core inside S | coverage of S |",
        "| :-- | ---: | ---: | ---: | ---: | ---: | :-- | ---: |",
    ]
    for kind, n, d in CONFIGS:
        rng = random.Random(args.seed + n * 100 + d)
        if kind == "distinct":
            values, support, _ = build_distinct(n, d, rng)
        else:
            values, support, _ = build(n, d, 2, rng)
        smax = 5 if n == 24 else 4
        cores = core_at(values, smax)
        s_set = set(support)
        for s in range(1, smax + 1):
            core = cores[s]
            enumerated = sum(comb(n, j) for j in range(1, s + 1))
            rows.append(
                f"| {kind} | {n} | {d} | {s} | {enumerated} | {len(core)} | "
                f"{core <= s_set} | {len(core & s_set) / len(s_set):.2f} |"
            )
            print(rows[-1], flush=True)
    lines = [
        "# R13a: short-relation core of a low-rank support",
        "",
        "Relations = equal-sum pairs of distinct subsets of size `<= s` among all `n` "
        "inputs, common elements removed. `core` is the union of elements in some "
        "relation; `core inside S` says no decoy ever appears (the signal is pure "
        "structure); `coverage` is the fraction of the hidden support `S` reached.",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "relation_core.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
