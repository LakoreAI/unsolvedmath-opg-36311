#!/usr/bin/env python3
"""Measure exact subset-sum solvers; write CSV tables and provenance.

Stdlib only. Default instances are even-valued with an odd target, so the
target is infeasible *inside* the magnitude range; every solver must therefore
do its full worst-case work instead of stopping at an early hit. A separate
feasible battery verifies that each solver returns a valid witness.

Usage:
    python3 scripts/analysis/benchmark.py
    python3 scripts/analysis/benchmark.py --max-seconds 3 --repeats 3
"""

import argparse
import csv
import os
import platform
import random
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from src.subset_sum import (  # noqa: E402
    Result,
    bounded_dp,
    meet_in_middle,
    schroeppel_shamir,
)

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"


def brute_force(values, target):
    """Exhaustive oracle for small n (not part of the library API)."""
    n = len(values)
    for bits in range(1 << n):
        total = 0
        for i, a in enumerate(values):
            if bits >> i & 1:
                total += a
        if total == target:
            return Result("brute", tuple(i for i in range(n) if bits >> i & 1), 1 << n)
    return Result("brute", None, 1 << n)


# (name, callable, max n). Larger n costs one heap/sort-heavy exponential step.
ALGORITHMS = (
    ("brute", brute_force, 16),
    ("dp", bounded_dp, 40),
    ("mitm", meet_in_middle, 36),
    ("ss", schroeppel_shamir, 36),
)


def instance(family, n, rng):
    if family == "signed_small":
        values = [2 * rng.randrange(-100, 101) for _ in range(n)]
    elif family == "wide_random":
        values = [2 * rng.randrange(-(1 << 40), 1 << 40) for _ in range(n)]
    else:
        raise ValueError(family)
    return values, 1  # odd target: infeasible since every value is even


def timed(fn, values, target, repeats):
    best = float("inf")
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(values, target)
        best = min(best, time.perf_counter() - start)
    return best, result


def peak_memory(fn, values, target):
    tracemalloc.start()
    fn(values, target)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def collect_csv(sizes, repeats, max_seconds):
    rows = []
    mem_rows = []
    for family in ("signed_small", "wide_random"):
        for n in sizes:
            rng = random.Random(36311 + n)
            values, target = instance(family, n, rng)
            width = sum(abs(a) for a in values)
            for name, fn, cap in ALGORITHMS:
                if n > cap:
                    continue
                if name == "dp" and 2 * width + 1 > 5_000_000:
                    print(f"  skip {family} n={n} dp: width {width} too large")
                    continue
                seconds, result = timed(fn, values, target, repeats)
                if seconds > max_seconds:
                    print(f"  skip {family} n={n} {name}: {seconds:.2f}s")
                    continue
                assert not result.feasible, (family, n, name)
                rows.append(
                    {
                        "family": family,
                        "n": n,
                        "algorithm": name,
                        "feasible": False,
                        "seconds": f"{seconds:.6f}",
                        "states": result.states,
                    }
                )
                if name in {"dp", "mitm", "ss"} and n <= 32:
                    mem_rows.append(
                        {
                            "family": family,
                            "n": n,
                            "algorithm": name,
                            "peak_kib": round(
                                peak_memory(fn, values, target) / 1024, 1
                            ),
                        }
                    )
                print(f"  {family} n={n} {name}: {seconds:.4f}s states={result.states}")
    return rows, mem_rows


def correctness_rows():
    """Feasible instances: every solver must return a valid unique witness."""
    rows = []
    for n in (4, 8, 12, 16, 20, 24):
        rng = random.Random(999 + n)
        values = [2 * rng.randrange(-100, 101) for _ in range(n)]
        chosen = [i for i in range(n) if rng.random() < 0.5] or [0]
        target = sum(values[i] for i in chosen)
        for name, fn, cap in ALGORITHMS:
            if n > cap:
                continue
            result = fn(values, target)
            ok = result.feasible and len(set(result.indices)) == len(result.indices)
            ok = ok and sum(values[i] for i in result.indices) == target
            rows.append({"n": n, "algorithm": name, "witness_ok": bool(ok)})
    return rows


def write_csv(path, rows):
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows, value):
    ns = sorted({r["n"] for r in rows})
    algs = sorted({r["algorithm"] for r in rows})
    lookup = {(r["n"], r["algorithm"]): r for r in rows}
    lines = [
        "| n | " + " | ".join(algs) + " |",
        "| ---: | " + " | ".join("---:" for _ in algs) + " |",
    ]
    for n in ns:
        cells = [
            f"{float(lookup[(n, alg)][value]):.3f}" if (n, alg) in lookup else "-"
            for alg in algs
        ]
        lines.append(f"| {n} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(path, bench_rows, mem_rows, corr_rows, sizes, repeats):
    parts = [
        "# Exact subset-sum measurements",
        "",
        "Generated by `scripts/analysis/benchmark.py` "
        f"(sizes n={sizes}, best of {repeats} runs, seconds).",
        "",
        "Instances are even-random; the target is odd, hence infeasible, so each",
        "solver runs to completion rather than stopping at an early hit.",
        "",
    ]
    for family in ("signed_small", "wide_random"):
        rows = [r for r in bench_rows if r["family"] == family]
        if not rows:
            continue
        parts += [
            f"## {family} — runtime (seconds, lower is better)",
            "",
            markdown_table(rows, "seconds"),
            "",
            f"## {family} — work units (`states`)",
            "",
            markdown_table(rows, "states"),
            "",
        ]
    if mem_rows:
        parts += [
            "## Peak traced memory (KiB, lower is better)",
            "",
            markdown_table(mem_rows, "peak_kib"),
            "",
        ]
    algs = sorted({r["algorithm"] for r in corr_rows})
    by_n = {}
    for r in corr_rows:
        by_n.setdefault(r["n"], {})[r["algorithm"]] = r["witness_ok"]
    parts += [
        "## Feasible witness check",
        "",
        "| n | " + " | ".join(algs) + " |",
        "| ---: | " + " | ".join("---:" for _ in algs) + " |",
    ]
    for n in sorted(by_n):
        cells = ["ok" if by_n[n].get(a) else "-" for a in algs]
        parts.append(f"| {n} | " + " | ".join(cells) + " |")
    path.write_text("\n".join(parts) + "\n")


def provenance(command, sizes, repeats, wall):
    sha = (
        subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        ).stdout.strip()
        or "unknown"
    )
    dirty = bool(
        subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        ).stdout.strip()
    )
    cpu = platform.processor() or platform.machine()
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    except OSError:
        pass
    return {
        "command": command,
        "commit": f"{sha}{' (dirty)' if dirty else ''}",
        "python": platform.python_version(),
        "platform": f"{platform.system()} {platform.release()} {platform.machine()}",
        "cpu": cpu,
        "cpu_count": os.cpu_count(),
        "seed": "36311+n (target); 999+n (correctness)",
        "sizes": str(sizes),
        "repeats": repeats,
        "date": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "wall_seconds": round(wall, 2),
    }


def write_provenance(path, data):
    lines = ["# Provenance", "", "| Field | Value |", "| --- | --- |"]
    lines += [f"| {k} | {v} |" for k, v in data.items()]
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--max-seconds", type=float, default=5.0)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=36)
    args = parser.parse_args()

    sizes = [n for n in (8, 12, 16, 20, 24, 28, 32, 36) if n <= args.max_n]
    start = time.time()
    bench_rows, mem_rows = collect_csv(sizes, args.repeats, args.max_seconds)
    corr_rows = correctness_rows()
    wall = time.time() - start

    args.out.mkdir(parents=True, exist_ok=True)
    write_csv(args.out / "bench.csv", bench_rows)
    write_csv(args.out / "memory.csv", mem_rows)
    write_csv(args.out / "correctness.csv", corr_rows)
    write_markdown(
        args.out / "bench.md", bench_rows, mem_rows, corr_rows, sizes, args.repeats
    )
    write_provenance(
        args.out / "provenance.md",
        provenance(" ".join(sys.argv), sizes, args.repeats, wall),
    )
    print(f"\nwrote tables to {args.out} in {wall:.1f}s")


if __name__ == "__main__":
    main()
