#!/usr/bin/env python3
"""R13a: how hard can a few-distinct-sums support be for the detect-and-compress route?

Heuristic exponent model (asymptotic, base 2, divided by ``n``; ``m = n/2``). A support
with ``D* = 2^(delta n)`` has its shortest relation (``|P| = |Q| = k``) at a length that
depends on how well the set avoids collisions:

* ``birthday``: random-like structure (e.g. a box with random coordinates). Pairs of
  ``k``-subsets collide when ``C(m,k)^2 ~ |Sigma_k| ~ 2^(2 delta m / 2)``, i.e.
  ``h2(k/m) = delta`` (``delta`` here is ``delta_n``).
* ``gv``: best known explicit-style avoidance (Gilbert-Varshamov): no relation of total
  length ``<= 2k`` requires ``h2(2k/m) = 2 delta``.
* ``pigeonhole``: the extremal bound of ``HIGH_ENERGY.md`` (``relation_length.md``); no known
  construction attains it (it needs near-perfect ``B_k`` sets).

Costs: detection ``h2(k/n)`` (sort all ``k``-subsets of the ``n`` inputs, valid below
the random-noise threshold ``k <= 0.11 n``); compress ``0.25 + delta/2``
(``sqrt(2^(n/2) |Sigma(S)|)``, assuming ``|Sigma(S)| <= 2^(delta n)``); LIFT
``min(0.5, max(0.4057, 0.8113 - delta))``. The algorithm runs both routes in parallel:
``best = min(LIFT, max(detect, compress))``.

Writes docs/analysis/2026-10-06/subset-sum/adversary_model.md.
"""

import argparse
from math import log2
from pathlib import Path

from relation_length import smallest_k_fraction

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def h2(p: float) -> float:
    if p <= 0 or p >= 1:
        return 0.0
    return -p * log2(p) - (1 - p) * log2(1 - p)


def h2inv(y: float) -> float:
    lo, hi = 0.0, 0.5
    for _ in range(80):
        mid = (lo + hi) / 2
        if h2(mid) < y:
            lo = mid
        else:
            hi = mid
    return lo


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    deltas = [round(0.02 * i, 2) for i in range(1, 25)]
    models = ("birthday", "gv", "pigeonhole")
    worst = {m: (0.0, 0.0) for m in models}
    rows = [
        "| delta | LIFT | compress | birthday k/n | detect | best | gv k/n | detect | best "
        "| pigeonhole k/n | detect | best |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for delta in deltas:
        lift = min(0.5, max(0.4057, 0.8113 - delta))
        compress = 0.25 + delta / 2
        cells = [f"{delta:.2f}", f"{lift:.3f}", f"{compress:.3f}"]
        for model in models:
            if model == "birthday":
                k_over_n = h2inv(delta) / 2 if delta <= 1 else 0.5
            elif model == "gv":
                k_over_n = h2inv(min(1.0, 2 * delta)) / 4
            else:
                k_over_n = smallest_k_fraction(delta)
            detect = h2(k_over_n)
            best = min(lift, max(detect, compress))
            cells += [f"{k_over_n:.4f}", f"{detect:.3f}", f"{best:.3f}"]
            if best > worst[model][0]:
                worst[model] = (best, delta)
        rows.append("| " + " | ".join(cells) + " |")
    lines = [
        "# R13a: adversary model for the detect-and-compress route",
        "",
        "Heuristic asymptotic exponents (see the script docstring for the model). "
        "`best = min(LIFT, max(detect, compress))`: the two routes run in parallel, "
        "and the relation route is only valid while `k <= 0.11 n` (random-noise "
        "threshold; otherwise decoy relations appear and `detect` is not trusted).",
        "",
        *rows,
        "",
        "## Worst case over `delta`",
        "",
        "| model | worst best-of exponent | at delta |",
        "| :-- | ---: | ---: |",
        *[f"| {m} | {worst[m][0]:.4f} | {worst[m][1]:.2f} |" for m in models],
        "",
        "Assumptions that make this a model and not a theorem: decoys are random (no "
        "relations below the noise threshold); `|Sigma(S)|` over all sizes is at most "
        "`2^(delta n)` (only the balanced half-sums are bounded by `D*`); the relations "
        "found cover the support. None of these is proved.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "adversary_model.md").write_text("\n".join(lines) + "\n")
    for m in models:
        print(m, worst[m])


if __name__ == "__main__":
    main()
