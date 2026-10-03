#!/usr/bin/env python3
"""Probe the Phase 1 dichotomy: structure versus many representations.

For several weight families, measure:
  * log2|S(A)|        — size of the reachable-sum set;
  * F                 — collision count sum_t max(0, count(t)-1) (PESS quantity);
  * energy(A)/n^3     — additive energy of the weights, normalised;
  * geo distance      — max_i |a_i - 2^i|, small means near-geometric.

The hypothesis: instances are either near-geometric / structured (small F) or
have many representations (large F). We flag any family with small F yet large
geometric distance, which would need a different argument.

Writes docs/analysis/2026-10-03/subset-sum/dichotomy.{csv,md}.
"""

import argparse
import csv
import math
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.additive import (  # noqa: E402
    additive_energy,
    collision_count,
    near_geometric_distance,
    subset_sums,
)

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (10, 12, 14, 16)


def families(n, rng):
    return {
        "geometric": [1 << i for i in range(n)],
        "near_geometric": [
            (1 << i) + rng.randrange(-(1 << (i // 2)), (1 << (i // 2)) + 1)
            for i in range(n)
        ],
        "powers_plus_one": [(1 << i) + 1 for i in range(n)],
        "arithmetic": list(range(1, n + 1)),
        "dense_random": [rng.randrange(1, n + 1) for _ in range(n)],
        "density1_random": [rng.randrange(1, 1 << n) for _ in range(n)],
        "dissociated_random": [rng.randrange(1, 1 << (2 * n)) for _ in range(n)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        rng = random.Random(args.seed + n)
        for name, values in families(n, rng).items():
            reachable = len(subset_sums(values))
            collisions = collision_count(values)
            energy = additive_energy(values) / (n**3)
            geo = near_geometric_distance(values)
            rows.append(
                {
                    "family": name,
                    "n": n,
                    "log2_sumset": round(math.log2(reachable), 2)
                    if reachable > 1
                    else 0.0,
                    "log2_collisions": round(math.log2(collisions), 2)
                    if collisions
                    else 0.0,
                    "normalised_energy": round(energy, 3),
                    "log2_geometric_distance": round(math.log2(1 + geo), 2),
                }
            )

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "dichotomy.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Phase 1 dichotomy probe",
        "",
        "Collision count `F` is the PESS quantity; a large `F` means many",
        "representations (subsampling/dissection applies), small `F` with small",
        "geometric distance means near-geometric structure.",
        "",
        "| family | n | log2|S| | log2 F | energy(A)/n^3 | log2 geo-dist |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines += [
        "| {family} | {n} | {log2_sumset} | {log2_collisions} | "
        "{normalised_energy} | {log2_geometric_distance} |".format(**r)
        for r in rows
    ]
    small = [
        r
        for r in rows
        if r["log2_collisions"] <= 1 and r["log2_geometric_distance"] >= 1
    ]
    lines += [
        "",
        "Danger-zone families (log2 F <= 1 and geo-dist >= 1): "
        + (", ".join(f"{r['family']}(n={r['n']})" for r in small) or "none"),
    ]
    (args.out / "dichotomy.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'dichotomy.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
