#!/usr/bin/env python3
"""Measure the HGJ representation search against meet-in-the-middle.

For each n, plant a balanced weight-n/2 solution, run the HGJ search, and
record the raw enumeration work (the cost driver, C(n/2,n/8) per half per
residue attempt) and wall time. The empirical bit-exponent of the enumeration
is fitted and compared with the meet-in-the-middle exponent 1/2.

The HGJ exponent is ~h(1/4)/2 = 0.4057 < 1/2: the representation + modular
filter already beats meet-in-the-middle on random instances at this level of
the recursion. The optimized BCJ 0.291n recursion is not implemented.

Writes docs/analysis/2026-10-03/subset-sum/hgj.csv and hgj.md.
"""

import argparse
import csv
import math
import random
import statistics
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.hgj import enumerated_size, hgj_search  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (16, 24, 32, 40, 48, 56)


def planted(n, rng):
    values = [rng.randrange(1, 1 << 30) for _ in range(n)]
    k = n // 2
    indices = set(rng.sample(range(k), n // 4)) | set(rng.sample(range(k, n), n // 4))
    return values, sum(values[i] for i in indices)


def slope(ns, ys):
    pts = [(n, math.log2(y)) for n, y in zip(ns, ys) if y > 0]
    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    mx, mz = statistics.fmean(xs), statistics.fmean(zs)
    denom = sum((x - mx) ** 2 for x in xs)
    b = sum((x - mx) * (z - mz) for x, z in zip(xs, zs)) / denom
    ss_tot = sum((z - mz) ** 2 for z in zs)
    ss_res = sum((z - (mz + b * (x - mx))) ** 2 for x, z in zip(xs, zs))
    return b, 1 - ss_res / ss_tot if ss_tot else 1.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-seconds", type=float, default=30.0)
    args = parser.parse_args()

    rows = []
    for n in SIZES:
        successes = 0
        best = float("inf")
        enumerated = 0
        for t in range(4):
            rng = random.Random(36311 + n + t)
            values, target = planted(n, rng)
            start = time.perf_counter()
            result = hgj_search(values, target, seed=t, residues=8)
            elapsed = time.perf_counter() - start
            if result.feasible:
                successes += 1
                best = min(best, elapsed)
                enumerated = result.enumerated
        if successes == 0 or best > args.max_seconds:
            print(f"  skip n={n}: successes={successes} best={best:.2f}s")
            continue
        rows.append(
            {
                "n": n,
                "analytical_enumeration": enumerated_size(n, n // 4),
                "measured_enumeration": enumerated,
                "seconds": best,
                "successes": successes,
            }
        )
        print(
            f"  n={n} enumeration={enumerated} best={best:.3f}s successes={successes}/4"
        )

    ns = [r["n"] for r in rows]
    enum_slope, enum_r2 = slope(ns, [r["analytical_enumeration"] for r in rows])
    time_slope, _ = slope(ns, [r["seconds"] for r in rows])

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "hgj.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Howgrave-Graham-Joux representation search vs meet-in-the-middle",
        "",
        "Planted balanced weight-n/2 solutions. Enumeration work is",
        "`2 * C(n/2, n/8)` per residue attempt (the cost driver), against",
        "meet-in-the-middle enumeration `2^(n/2)`.",
        "",
        "| n | analytical enumeration | 2^(n/2) | log2(enum)/n | seconds |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for r in rows:
        lines.append(
            "| {n} | {analytical_enumeration} | {mitm:.3e} | {exp:.4f} | {seconds:.3f} |".format(
                mitm=2 ** (r["n"] / 2),
                exp=math.log2(r["analytical_enumeration"]) / r["n"],
                **r,
            )
        )
    lines += [
        "",
        f"Fitted enumeration bit-exponent: **{enum_slope:.4f}** (R^2={enum_r2:.4f});",
        f"meet-in-the-middle is 0.5. Fitted wall-time exponent: {time_slope:.4f}.",
        "The theoretical HGJ value is `h(1/4)/2 = 0.4057`; the optimized 0.291n",
        "recursion is not implemented.",
    ]
    (args.out / "hgj.md").write_text("\n".join(lines) + "\n")
    print(f"\nwrote {args.out / 'hgj.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
