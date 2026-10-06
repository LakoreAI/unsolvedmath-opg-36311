#!/usr/bin/env python3
"""R13a: are fixed-size subset-sum counts maximized at the middle size?

``adversary_model.py`` assumes ``|Sigma(S)| <= 2^(delta n)`` for the sums of *all* sizes,
while the theory only bounds the middle-size count ``D``. If

    Conjecture U: max_k |Sigma_k(X)| <= poly(m) * |Sigma_{floor(m/2)}(X)|

held for every set ``X`` of ``m`` integers, then ``|Sigma(X)| <= (m+1) max_k |Sigma_k|`` would
remove that assumption up to a polynomial factor. This script searches for violations:
random and structured sets at ``m = 8, 10, 12`` and adversarial hill-climbing (maximize
``max_k |Sigma_k| / |Sigma_mid|``) at ``m = 8..14``.

Writes docs/analysis/2026-10-06/subset-sum/ksum_unimodal.md.
"""

import argparse
import random
from math import comb
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def ksums(xs):
    m = len(xs)
    dp = [set() for _ in range(m + 1)]
    dp[0].add(0)
    for x in xs:
        for k in range(m - 1, -1, -1):
            if dp[k]:
                dp[k + 1] |= {s + x for s in dp[k]}
    return [len(s) for s in dp]


def ratio(xs):
    counts = ksums(xs)
    return max(counts) / counts[len(xs) // 2]


def random_set(m, rng, kind):
    if kind == 0:
        return rng.sample(range(1, 3 * m), m)
    if kind == 1:
        return [rng.randrange(1, 6) * 7 + rng.randrange(2) * 1000 for _ in range(m)]
    if kind == 2:
        return list(range(1, m // 2 + 1)) + [
            10**6 * (i + 1) + i * i for i in range(m - m // 2)
        ]
    return [
        rng.choice([1, 2, 3, 50, 51, 52, 10**5]) + rng.randrange(3) * 10**7
        for _ in range(m)
    ]


def climb(m, rng, iters):
    xs = [rng.choice([1, 2, 3, 5, 8]) * 10 ** rng.randrange(0, 4) for _ in range(m)]
    cur = ratio(xs)
    for _ in range(iters):
        ys = list(xs)
        i = rng.randrange(m)
        ys[i] = rng.choice(
            [
                rng.randrange(1, 40),
                rng.randrange(1, 10**7),
                xs[rng.randrange(m)] + rng.choice([-1, 0, 1]),
                xs[rng.randrange(m)] + xs[rng.randrange(m)],
            ]
        )
        r = ratio(ys)
        if r >= cur:
            xs, cur = ys, r
    return cur, xs


def two_ap_count(h, g, k):
    """|Sigma_k| for X = {1..h} u {g+1..g+h} via a union of intervals."""
    ivs = []
    for j in range(max(0, k - h), min(k, h) + 1):
        a = k - j
        lo = a * (a + 1) // 2 + j * (j + 1) // 2 + j * g
        hi = a * (2 * h - a + 1) // 2 + j * (2 * h - j + 1) // 2 + j * g
        ivs.append((lo, hi))
    ivs.sort()
    total = 0
    cur = None
    for lo, hi in ivs:
        if cur is None or lo > cur[1] + 1:
            if cur:
                total += cur[1] - cur[0] + 1
            cur = [lo, hi]
        else:
            cur[1] = max(cur[1], hi)
    return total + cur[1] - cur[0] + 1


def ap_plus_dissociated(h, k):
    """|Sigma_k| for X = {1..h} u {N 2^i : i < h}, N huge (exact formula)."""
    return sum(
        comb(h, j) * ((k - j) * (h - k + j) + 1) for j in range(0, k + 1) if k - j <= h
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    rows = [
        "| m | search | sets tried | worst ratio | counts at worst |",
        "| ---: | :-- | ---: | ---: | :-- |",
    ]
    for m in (8, 10, 12):
        worst = (0.0, None)
        for trial in range(3000):
            xs = random_set(m, rng, trial % 4)
            r = ratio(xs)
            if r > worst[0]:
                worst = (r, xs)
        rows.append(
            f"| {m} | random/structured | 3000 | {worst[0]:.3f} | {ksums(worst[1])} |"
        )
        print(rows[-1], flush=True)
    for m in (8, 10, 12, 14):
        worst = (0.0, None)
        for _ in range(4):
            r, xs = climb(m, rng, 1500)
            if r > worst[0]:
                worst = (r, xs)
        rows.append(
            f"| {m} | hill-climb x4 | 6000 | {worst[0]:.3f} | {ksums(worst[1])} |"
        )
        print(rows[-1], flush=True)
    fam = [
        "| family | m | min over parameters of |Sigma_mid| / max_k |Sigma_k| |",
        "| :-- | ---: | ---: |",
    ]
    for h in (6, 10, 20, 50, 100, 200):
        worst = min(
            two_ap_count(h, g, h) / max(two_ap_count(h, g, k) for k in range(2 * h + 1))
            for g in range(h, h * h + 2 * h, max(1, h // 10))
        )
        fam.append(
            f"| two APs with a gap (dips at the middle) | {2 * h} | {worst:.4f} |"
        )
    for h in (10, 30, 60, 200):
        counts = [ap_plus_dissociated(h, k) for k in range(2 * h + 1)]
        fam.append(
            f"| AP plus dissociated block | {2 * h} | {counts[h] / max(counts):.4f} |"
        )
    print("\n".join(fam))
    lines = [
        "# R13a: is |Sigma_k| maximized at the middle size? (Conjecture U)",
        "",
        "`ratio = max_k |Sigma_k(X)| / |Sigma_{m/2}(X)|`. Conjecture U asks for "
        "`ratio <= poly(m)`; the counts need not be unimodal (a ratio slightly above 1 "
        "appears at `m = 8`), but no search found the middle count far from the "
        "maximum.",
        "",
        *rows,
        "",
        "## Analytic families at larger m",
        "",
        "The two-AP family is the one on which the hill-climb found dips; its worst "
        "middle-to-maximum ratio tends to 1 as `m` grows (`0.946` at `m = 12`, `0.998` "
        "at `m = 400`).",
        "",
        *fam,
        "",
        "Literature check (2026-10-06): no theorem on unimodality or middle-dominance of "
        "restricted sumset sizes `|k^ X|` in `k` was found; the nearest work studies "
        "the range of sumset sizes `R(h,k)` (arXiv 2505.07679, 2510.23022) and inverse "
        "theorems for restricted sumsets (arXiv 2505.07415), which answer different "
        "questions. Conjecture U remains open here.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "ksum_unimodal.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
