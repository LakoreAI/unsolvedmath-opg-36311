#!/usr/bin/env python3
"""Regime-aware subset-sum benchmark with empirical exponent fitting.

Families:
  bounded — values in [-50,50]; the magnitude sum W is polynomial, so the
            signed DP is polynomial and MITM/Schroeppel-Shamir are exponential.
  sparse  — values ~2^40; the DP table is infeasible, leaving the exponential
            meet-in-the-middle / Schroeppel-Shamir methods.

All targets are odd while every value is even, so instances are infeasible and
each solver runs to completion. For each (family, algorithm) we least-squares fit
log2(seconds) and log2(states) against n; the slope is the empirical bit-exponent.

Writes docs/analysis/2026-10-03/subset-sum/regimes.{csv,md}.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.subset_sum import (  # noqa: E402
    bounded_dp,
    meet_in_middle,
    schroeppel_shamir,
)

import benchmark  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"
SIZES = (8, 12, 16, 20, 24, 28, 32)
ALGORITHMS = (
    ("brute", benchmark.brute_force, 16),
    ("dp", bounded_dp, 40),
    ("mitm", meet_in_middle, 34),
    ("ss", schroeppel_shamir, 34),
)


def family_instance(family, n, rng):
    if family == "bounded":
        return [2 * rng.randrange(-50, 51) for _ in range(n)], 1
    if family == "sparse":
        return [2 * rng.randrange(-(1 << 40), 1 << 40) for _ in range(n)], 1
    raise ValueError(family)


def slope(ns, ys):
    """Least-squares slope of log2(y) against n; None if degenerate."""
    pts = [(n, math.log2(y)) for n, y in zip(ns, ys) if y > 0]
    if len(pts) < 2:
        return None, None
    xs = [p[0] for p in pts]
    zs = [p[1] for p in pts]
    mx, mz = statistics.fmean(xs), statistics.fmean(zs)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom == 0:
        return None, None
    b = sum((x - mx) * (z - mz) for x, z in zip(xs, zs)) / denom
    ss_tot = sum((z - mz) ** 2 for z in zs)
    ss_res = sum((z - (mz + b * (x - mx))) ** 2 for x, z in zip(xs, zs))
    r2 = 1 - ss_res / ss_tot if ss_tot else 1.0
    return b, r2


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-seconds", type=float, default=5.0)
    args = parser.parse_args()

    rows = []
    for family in ("bounded", "sparse"):
        for n in SIZES:
            rng = random.Random(36311 + n)
            values, target = family_instance(family, n, rng)
            width = sum(abs(a) for a in values)
            for name, fn, cap in ALGORITHMS:
                if n > cap:
                    continue
                if name == "dp" and 2 * width + 1 > 5_000_000:
                    continue
                best, result = float("inf"), None
                for _ in range(args.repeats):
                    start = time.perf_counter()
                    result = fn(values, target)
                    best = min(best, time.perf_counter() - start)
                if best > args.max_seconds:
                    continue
                assert not result.feasible
                rows.append(
                    {
                        "family": family,
                        "n": n,
                        "algorithm": name,
                        "seconds": best,
                        "states": result.states,
                    }
                )

    fits = []
    for family in ("bounded", "sparse"):
        for name, _, _ in ALGORITHMS:
            subset = sorted(
                (r for r in rows if r["family"] == family and r["algorithm"] == name),
                key=lambda r: r["n"],
            )
            if len(subset) < 3:
                continue
            ns = [r["n"] for r in subset]
            t_slope, t_r2 = slope(ns, [r["seconds"] for r in subset])
            s_slope, s_r2 = slope(ns, [r["states"] for r in subset])
            fits.append(
                {
                    "family": family,
                    "algorithm": name,
                    "points": len(subset),
                    "time_bits_per_n": f"{t_slope:.3f}"
                    if t_slope is not None
                    else "--",
                    "states_bits_per_n": f"{s_slope:.3f}"
                    if s_slope is not None
                    else "--",
                    "time_r2": f"{t_r2:.3f}" if t_r2 is not None else "--",
                }
            )

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "regimes.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = [
        "# Regime-aware subset-sum benchmark",
        "",
        "Infeasible instances (even values, odd target). Least-squares slope of",
        "`log2(seconds)` and `log2(states)` against `n` estimates the bit-exponent.",
        "",
        "| family | algorithm | points | time bits/n | states bits/n | time R^2 |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for fit in fits:
        lines.append(
            "| {family} | {algorithm} | {points} | {time_bits_per_n} | "
            "{states_bits_per_n} | {time_r2} |".format(**fit)
        )
    (args.out / "regimes.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'regimes.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
