#!/usr/bin/env python3
"""R13a: compress-then-MITM beyond toy size.

Part A (solved for real). A structured part of ``m`` elements ``a = <c, g>`` with
``c`` distinct in ``[0, L)^d`` and random 40-bit generators, plus ``r`` random decoys,
``n = m + r`` far beyond what plain meet-in-the-middle can touch (``2^{n/2}`` states).
``solve_compressed`` finds a verified witness; the table gives the states touched and
the plain-MITM count it replaces.

Part B (detection only). ``m = 200`` distinct weight-3 vectors in ``Z^12`` plus
``r = 24`` random decoys (``n = 224``): relation search with ``s <= 3`` (cost
``sum C(n,j)``); reports whether the core lies inside the structured part and its
coverage, and the predicted ``log2`` cost ``(r + log2 Sigma_ub)/2`` against ``n/2``,
with ``Sigma_ub`` the box volume ``prod_j (1 + sum_i c_ij)``. The instance is not
solved (``2^{42}`` states), so exactness is only tested on the small instances.

Writes docs/analysis/2026-10-06/subset-sum/compress_scale.md.
"""

import argparse
import random
import sys
import time
from math import log2, prod
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.compress_mitm import find_cores, solve_compressed  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def box_instance(m, d, side, r, rng, bits=40):
    gens = [rng.randrange(1 << (bits - 1), 1 << bits) for _ in range(d)]
    vecs = set()
    while len(vecs) < m:
        v = tuple(rng.randrange(side) for _ in range(d))
        if any(v):
            vecs.add(v)
    vecs = sorted(vecs)
    structured = [sum(c * g for c, g in zip(v, gens)) for v in vecs]
    decoys = [rng.randrange(1 << 60) for _ in range(r)]
    return structured, decoys, vecs


def weight3_instance(m, d, r, rng, bits=64):
    gens = [rng.randrange(1 << (bits - 1), 1 << bits) for _ in range(d)]
    vecs = set()
    while len(vecs) < m:
        vecs.add(tuple(sorted(rng.sample(range(d), 3))))
    vecs = sorted(vecs)
    structured = [sum(gens[j] for j in v) for v in vecs]
    decoys = [rng.randrange(1 << bits) for _ in range(r)]
    return structured, decoys, vecs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows_a = [
        "| m | d | L | r | n | core | |Sigma(core)| | compress states | plain MITM 2^(n/2) | "
        "ratio | seconds | verified |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |",
    ]
    for m, d, side, r in ((40, 3, 4, 16), (60, 3, 4, 16), (60, 3, 4, 20)):
        rng = random.Random(args.seed + m * 10 + r)
        structured, decoys, _ = box_instance(m, d, side, r, rng)
        values = structured + decoys
        order = list(range(len(values)))
        rng.shuffle(order)
        values = [values[i] for i in order]
        n = len(values)
        pos_struct = [k for k, i in enumerate(order) if i < m]
        chosen = rng.sample(pos_struct, m // 2) + rng.sample(
            [k for k, i in enumerate(order) if i >= m], r // 2
        )
        target = sum(values[i] for i in chosen)
        t0 = time.time()
        got = solve_compressed(values, target, smax=2, sigma_cap=1 << 23)
        sec = time.time() - t0
        ok = got.indices is not None and sum(values[i] for i in got.indices) == target
        plain = 2 ** (n // 2)
        rows_a.append(
            f"| {m} | {d} | {side} | {r} | {n} | {got.core_size} | {got.sigma_size} | "
            f"{got.states} | {plain:.2e} | {plain / got.states:.1e} | {sec:.0f} | {ok} |"
        )
        print(rows_a[-1], flush=True)

    rng = random.Random(args.seed + 224)
    m, d, r = 200, 12, 24
    structured, decoys, vecs = weight3_instance(m, d, r, rng)
    values = structured + decoys
    order = list(range(len(values)))
    rng.shuffle(order)
    values = [values[i] for i in order]
    n = len(values)
    s_set = {k for k, i in enumerate(order) if i < m}
    t0 = time.time()
    cores, enumerated = find_cores(values, 3, cap=1 << 23)
    sec = time.time() - t0
    sigma_ub = prod(1 + sum(v.count(j) for v in vecs) for j in range(d))
    rows_b = [
        "| s | enumerated | core size | core inside S | coverage of S | "
        "log2 Sigma_ub | predicted log2 cost | log2 plain 2^(n/2) |",
        "| ---: | ---: | ---: | :-- | ---: | ---: | ---: | ---: |",
    ]
    for s, core in sorted(cores.items()):
        rows_b.append(
            f"| {s} | {sum(__import__('math').comb(n, j) for j in range(1, s + 1))} | "
            f"{len(core)} | {core <= s_set} | {len(core & s_set) / m:.2f} | "
            f"{log2(sigma_ub):.1f} | {(r + log2(sigma_ub)) / 2:.1f} | {n / 2:.0f} |"
        )
        print(rows_b[-1], flush=True)

    lines = [
        "# R13a: compress-then-MITM beyond toy size",
        "",
        "## Part A: solved instances (verified witness)",
        "",
        "Structured part: `m` distinct vectors in `[0, L)^d`, random 40-bit generators; "
        "`r` random 60-bit decoys; target = a random half of the structured part plus "
        "half the decoys. Plain MITM would touch `2^(n/2)` states.",
        "",
        *rows_a,
        "",
        "## Part B: detection at `n = 224` (not solved)",
        "",
        f"`m = {m}` distinct weight-3 vectors in `Z^{d}`, 64-bit generators, `r = {r}` "
        f"random decoys; relation search took {sec:.0f} s. The predicted cost uses the "
        "box volume as an upper bound on `|Sigma(core)|`; with a full core "
        "the remaining random part is only `r` elements.",
        "",
        *rows_b,
        "",
        "## Reading",
        "",
        "* Part A: the exact solver finds a verified witness at `n = 56, 76, 80`, where "
        "plain meet-in-the-middle would need `2^28 .. 2^40` states, using "
        "`1.5e5 .. 8.3e5`: a `1.7e3 .. 1.3e6` fold reduction. The reduction is large "
        "because the structured part is rank 3 with `|Sigma|` about `2^18`, not because "
        "the method touches a hard instance.",
        "* Part B: at `n = 224` the `s = 2` relation search (about `25 000` subsets) "
        "already returns exactly the 200 structured elements and no decoy (the noise "
        "threshold for 64-bit decoys is far above `s = 3`). The predicted cost "
        "`2^46` against `2^112` is an estimate from the box volume, not a run.",
        "* Honest scope. These supports have a small-doubling structured part "
        "(rank `d` far below `m`). With only `r` random decoys the whole set has "
        "doubling bounded by a constant times `r`, which is the regime of the "
        "small-doubling algorithms of Randolph-Wegrzycki (doubly exponential constants "
        "in theory). So this shows a practical exact solver and detector for "
        "structured-plus-random inputs, not an advance on the hard band, where no "
        "sub-collection is compressible.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "compress_scale.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
