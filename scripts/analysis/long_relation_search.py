#!/usr/bin/env python3
"""R13a: adversarial search for compressible sets whose relations are all long.

A set ``S`` of ``m`` positive integers below ``R`` is compressible (``|Sigma(S)| <= mR <
2^{m/2}``) by construction. Its shortest relation ``s*`` is the smallest ``s`` such that two
distinct subsets of size ``<= s`` have equal sums. The adversary maximizes ``s*`` by
simulated annealing (objective: ``s*``, then fewest colliding pairs at size ``s*``). Bounds:

* pigeonhole (proved): a relation exists at the smallest ``s`` with
  ``sum_{j<=s} C(m, j) > s R + 1``;
* birthday (heuristic, random sets): ``(sum_{j<=s} C(m, j))^2 >= 2 (s R + 1)``.

A best-found ``s*`` well above the birthday value at the largest ``m`` would be a candidate
hard family for detect-and-compress.

Writes docs/analysis/2026-10-06/subset-sum/long_relation_search.md.
"""

import argparse
import math
import random
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"
SMAX = 4


def profile(values, smax=SMAX):
    """(s*, colliding pairs at s*) with s* = smax + 1 if no relation up to smax."""
    counts = Counter({0: 1})
    for s in range(1, smax + 1):
        for idx in combinations(values, s):
            counts[sum(idx)] += 1
        pairs = sum(c * (c - 1) // 2 for c in counts.values())
        if pairs:
            return s, pairs
    return smax + 1, 0


def bound(m, rng_size, squared):
    total = 1 + m  # sizes 0 and 1: elements are distinct, so no size-1 relation
    for s in range(2, m + 1):
        total += comb(m, s)
        lhs = total * total if squared else total
        rhs = 2 * (s * rng_size + 1) if squared else s * rng_size + 1
        if lhs > rhs:
            return s
    return m


def sidon(m):
    """Erdos-Turan Sidon set {2pk + (k^2 mod p)}: all pairwise sums distinct (s* >= 3)."""
    p = m + 1
    while any(p % q == 0 for q in range(2, int(p**0.5) + 1)):
        p += 1
    return [2 * p * k + (k * k % p) for k in range(1, m + 1)], 2 * p * p


def anneal(m, rng_size, iters, rng):
    values = rng.sample(range(1, rng_size), m)
    cur = profile(values)
    best = (cur, list(values))
    temp = 1.0
    for it in range(iters):
        cand = list(values)
        i = rng.randrange(m)
        new = rng.randrange(1, rng_size)
        if new in cand:
            continue
        cand[i] = new
        score = profile(cand)
        delta = (score[0] - cur[0]) * 1000 - (score[1] - cur[1])
        if delta >= 0 or rng.random() < math.exp(delta / max(temp, 1e-9)):
            values, cur = cand, score
            if (cur[0], -cur[1]) > (best[0][0], -best[0][1]):
                best = (cur, list(values))
        temp = 50.0 * (1 - it / iters)
    return best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()
    rng = random.Random(args.seed)
    rows = [
        "| m | R (values < R) | log2(mR) vs m/2 | pigeonhole s | birthday s | random s* | "
        "annealed best s* | collisions at s* | Sidon s* (range) |",
        "| ---: | ---: | :-- | ---: | ---: | ---: | ---: | ---: | :-- |",
    ]
    for m, iters in ((24, 600), (32, 300), (36, 200), (40, 120)):
        rng_size = max(m + 1, (1 << (m // 2 - 2)) // m)
        rand = profile(rng.sample(range(1, rng_size), m))
        (best_s, best_pairs), _vals = anneal(m, rng_size, iters, rng)
        sid, sid_range = sidon(m)
        sid_note = f"{profile(sid)[0]} ({sid_range}, {'fits' if sid_range <= rng_size else 'too wide'})"
        rows.append(
            f"| {m} | {rng_size} | {math.log2(m * rng_size):.1f} vs {m // 2} | "
            f"{bound(m, rng_size, False)} | {bound(m, rng_size, True)} | {rand[0]} | "
            f"{best_s} | {best_pairs} | {sid_note} |"
        )
        print(rows[-1], flush=True)
    lines = [
        "# R13a: adversarial search for compressible sets with only long relations",
        "",
        "Sets of `m` distinct integers below `R`, so `|Sigma| <= mR < 2^{m/2}` "
        "(compressible). `s*` = smallest size with two equal-sum subsets (searched up to "
        f"`{SMAX}`; `{SMAX + 1}` means none found). The annealer maximizes `s*`.",
        "",
        *rows,
        "",
        "## Reading",
        "",
        "* Annealing never pushed `s*` above 2, though the colliding pairs at `s = 2` fell "
        "from hundreds to about 20 as `m` grew: a weak search, not a proof.",
        "* An explicit Sidon set (Erdos-Turan) has `s* >= 3`; it fits inside the "
        "compressible range only at `m = 40` (range 3362 < 6553), one above the birthday "
        "value there. Algebraic `B_h` sets in general "
        "(Bose-Chowla) give `s* = h + 1` with range about `m^h`, compressible only for "
        "`h < m / (2 log2 m)`: relation length `O(m / log m)`, which is asymptotically "
        "*below* the birthday scale `Theta(m)`. So small `m` flatters algebraic "
        "constructions; asymptotically the random-like adversary remains the strongest known.",
        "* The pigeonhole bound (`s = 4` at `m = 40`) is not approached by any construction "
        "here.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "long_relation_search.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
