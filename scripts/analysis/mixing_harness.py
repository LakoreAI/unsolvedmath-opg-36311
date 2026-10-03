#!/usr/bin/env python3
"""Mixing harness: measure representation counts for subset-sum / balancing.

The representation/dissection technique works when a target has *many*
encodings. This harness measures that quantity directly for small n and several
coefficient sets C:

  * total number of c in C^n with c . w = target (representation count);
  * how many representations survive random subsampling of the items
    (the "random restriction" used in Either-Or and worst-case representation).

Geometric weights w_i = 2^(i-1) are the near-worst case with few
representations; random weights are the near-average case with many.

Writes docs/analysis/2026-10-03/subset-sum/mixing.md.
"""

import argparse
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"

COEFF_SETS = {
    "vanilla_{0,1}": (0, 1),
    "signed_{-1,0,1}": (-1, 0, 1),
    "partition_{-1,1}": (-1, 1),
}


def half_counts(values, coeffs):
    counts = {0: 1}
    for a in values:
        nxt = {}
        for s, c in counts.items():
            for k in coeffs:
                key = s + k * a
                nxt[key] = nxt.get(key, 0) + c
        counts = nxt
    return counts


def count_coeff_vectors(values, coeffs, target):
    """Number of c in coeffs^n with c . w = target (meet-in-the-middle count)."""
    k = len(values) // 2
    left = half_counts(values[:k], coeffs)
    right = half_counts(values[k:], coeffs)
    if len(left) > len(right):
        left, right = right, left
    total = 0
    for s, c in left.items():
        total += c * right.get(target - s, 0)
    return total


def random_subset_sum(rng, values):
    chosen = [i for i in range(len(values)) if rng.random() < 0.5]
    return sum(values[i] for i in chosen)


def representation_table():
    rng = random.Random(36311)
    n = 16
    random_w = [rng.randrange(1, 51) for _ in range(n)]
    geometric_w = [1 << i for i in range(n)]
    target = random_subset_sum(rng, random_w)
    rows = []
    for label, weights, tgt in (
        ("random", random_w, target),
        ("geometric", geometric_w, random_subset_sum(rng, geometric_w)),
    ):
        for cname, coeffs in COEFF_SETS.items():
            if cname == "signed_{-1,0,1}":
                count = count_coeff_vectors(weights, coeffs, 0) - 1
                target_label = 0
            else:
                count = count_coeff_vectors(weights, coeffs, tgt)
                target_label = tgt
            rows.append((label, cname, n, target_label, count))
    return rows


def subsampling_table(trials=60):
    rng = random.Random(7)
    n = 16
    sizes = (10, 12, 14, 16)
    rows = []
    for label, weights in (
        ("random", [rng.randrange(1, 51) for _ in range(n)]),
        ("geometric", [1 << i for i in range(n)]),
    ):
        target = random_subset_sum(rng, weights)
        for m in sizes:
            hits = 0
            for _ in range(trials):
                idx = rng.sample(range(n), m)
                sub = [weights[i] for i in idx]
                if count_coeff_vectors(sub, (0, 1), target):
                    hits += 1
            rows.append((label, m, hits, trials))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    reps = representation_table()
    subs = subsampling_table()

    lines = [
        "# Mixing harness: representation counts",
        "",
        "Number of coefficient vectors `c in C^n` with `c . w = target`.",
        "Geometric weights are the near-worst case (few representations);",
        "random weights are the near-average case (many).",
        "",
        "| weights | C | n | target | representations |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    lines += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |" for r in reps]

    lines += [
        "",
        "## Random subsampling (vanilla `{0,1}`, target fixed)",
        "",
        "Fraction of random m-item subsamples that still contain a representation.",
        "The representation technique needs a solution to survive such restrictions.",
        "",
        "| weights | m / n | subsamples with a solution |",
        "| --- | ---: | ---: |",
    ]
    for label, m, hits, trials in subs:
        lines.append(f"| {label} | {m}/16 | {hits}/{trials} |")

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "mixing.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'mixing.md'}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
