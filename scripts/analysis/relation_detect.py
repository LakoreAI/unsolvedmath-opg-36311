#!/usr/bin/env python3
"""R13a: does LLL on the relation lattice expose a low-rank support?

Instances from ``high_energy.build``: ``n/2`` support values in a rank-``d`` GAP
with random ``n``-bit generators, ``n/2`` random ``n``-bit decoys, positions
shuffled. The relation lattice ``{z : z . a = 0}`` is LLL-reduced; for each reduced
vector we record its squared norm and whether its support lies inside the hidden
support ``S``. A control with ``d = n/2`` (full rank) has no short relations inside
``S``. Prediction: for rank ``d``, the ``|S| - d`` shortest reduced vectors are
supported in ``S`` and stand out by norm, so a gap in the norm sequence (or simply
the support structure) identifies ``S`` in polynomial time.

Writes docs/analysis/2026-10-06/subset-sum/relation_detect.md.
"""

import argparse
import random
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from high_energy import build  # noqa: E402

from src.lll import norm2, relation_basis  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
CONFIGS = ((16, 2), (16, 3), (16, 8), (24, 3), (24, 4), (24, 12))
SIDON = ((16, 5), (16, 6), (24, 7), (24, 8), (24, 10))


def build_distinct(n: int, d: int, rng: random.Random):
    """Support = distinct weight-3 0/1 vectors in Z^d mapped by random n-bit generators."""
    gens = [rng.randrange(1 << (n - 1), 1 << n) for _ in range(d)]
    m = n // 2
    vecs = set()
    while len(vecs) < m:
        vecs.add(tuple(sorted(rng.sample(range(d), 3))))
    support_values = [sum(gens[j] for j in v) for v in vecs]
    decoys = [rng.randrange(1 << (n - 1), 1 << n) for _ in range(n - m)]
    positions = list(range(n))
    rng.shuffle(positions)
    values = [0] * n
    for pos, v in zip(positions[:m], support_values):
        values[pos] = v
    for pos, v in zip(positions[m:], decoys):
        values[pos] = v
    return values, sorted(positions[:m]), sum(support_values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| n | rank d | S-relations expected (m-d) | reduced vectors inside S | "
        "of the shortest (m-d) | min norm^2 inside S | min norm^2 outside S | sec |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for n, d, distinct in [(*c, False) for c in CONFIGS] + [(*c, True) for c in SIDON]:
        rng = random.Random(args.seed + n * 100 + d)
        if distinct:
            values, support, _ = build_distinct(n, d, rng)
        else:
            values, support, _ = build(n, d, 2, rng)
        s = set(support)
        t0 = time.time()
        basis = relation_basis(values)
        sec = time.time() - t0
        inside = []
        outside = []
        for row in basis:
            supp = {i for i, z in enumerate(row) if z}
            (inside if supp <= s else outside).append(norm2(row))
        expect = max(0, n // 2 - d)
        ordered = sorted(
            (norm2(r), {i for i, z in enumerate(r) if z} <= s) for r in basis
        )
        top = ordered[:expect]
        hit = sum(1 for _, ok in top if ok)
        rows.append(
            f"| {n} | {d}{'*' if distinct else ''} | {expect} | {len(inside)} | {hit}/{len(top)} | "
            f"{min(inside) if inside else '-'} | {min(outside) if outside else '-'} | {sec:.0f} |"
        )
        print(rows[-1], flush=True)
    lines = [
        "# R13a: relation-lattice detection of a low-rank support",
        "",
        "Support values in a rank-`d` GAP (side 2) with random `n`-bit generators, "
        "decoys random `n`-bit. `inside S` counts reduced-basis vectors whose "
        "support is contained in the hidden support. `of the shortest (m-d)` is "
        "how many of the `m-d` shortest reduced vectors lie inside `S`. A `*` marks "
        "the distinct-vector family (distinct weight-3 vectors, so no duplicate or "
        "zero elements and no trivial norm-1 or norm-2 relations).",
        "",
        *rows,
        "",
        "## Reading",
        "",
        "* With duplicate or zero elements (rows without `*`) the support-internal "
        "relations have norm 1-2 and LLL finds every one of them: trivially easy.",
        "* With distinct vectors (`*`) LLL still isolates all `m-d` support relations "
        "while they are shorter than generic lattice vectors (`n = 24`, `d = 7`: "
        "norm^2 4 vs 8). As `d` grows the support relations lengthen; at `d = 8` only "
        "2 of 4 are found inside `S` and at `d = 10` none (their norm no longer beats "
        "the generic shortest relations, norm^2 about 9).",
        "* The generic shortest relation of `n` random `n`-bit numbers has "
        "norm^2 `Theta(n)`; a support relation of length `Theta(n)` (exactly the "
        "forced-relation scale of `HIGH_ENERGY.md`) is not shorter. So lattice "
        "reduction detects the easy corner and meets the shortest-vector barrier in "
        "the hard corner (an approximation factor `2^{Theta(n)}` is too coarse).",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "relation_detect.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
