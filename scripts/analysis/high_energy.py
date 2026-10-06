#!/usr/bin/env python3
"""R13a: the high-energy regime ``D <= 2^(0.311 n)`` of LIFT.md.

Builds planted instances whose *solution support* lies in a rank-``d`` generalized
arithmetic progression with random ``n``-bit generators (``a_i = <c_i, g>``,
``c_i in [0, L)^d``) and fills the rest with random ``n``-bit decoys, so the
support is not distinguishable by size. For each instance it reports

* ``D``, ``Y`` for the support and the proposition's predicted exponent
  ``max(0.4057 n, log2 C(n, n/4) - log2 D) / n`` (capped by MITM at ``0.5``);
* the measured enumeration work of ``hgj_permuted_search`` with the modulus
  ``M`` set to ``~4D`` (the guess the proposition uses) and the default
  ``2^(n/2)``-scale modulus;
* the additive-quadruple *core* (elements in some ``a_i + a_j = a_k + a_l``):
  its size and whether it contains the support. A core of size ``~n/2``
  containing the support lets meet-in-the-middle run on the core alone.

Writes docs/analysis/2026-10-06/subset-sum/high_energy.md.
"""

import argparse
import random
import sys
from collections import defaultdict
from itertools import combinations
from math import ceil, comb, log2
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hgj_adversarial import next_prime  # noqa: E402

from src.hgj import hgj_permuted_search  # noqa: E402

DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-06" / "subset-sum"


def build(n: int, d: int, side: int, rng: random.Random):
    gens = [rng.randrange(1 << (n - 1), 1 << n) for _ in range(d)]
    m = n // 2
    support_values = [sum(rng.randrange(side) * g for g in gens) for _ in range(m)]
    decoys = [rng.randrange(1 << (n - 1), 1 << n) for _ in range(n - m)]
    positions = list(range(n))
    rng.shuffle(positions)
    values = [0] * n
    for pos, v in zip(positions[:m], support_values):
        values[pos] = v
    for pos, v in zip(positions[m:], decoys):
        values[pos] = v
    support = sorted(positions[:m])
    return values, support, sum(support_values)


def quadruple_core(values) -> set[int]:
    pairs = defaultdict(list)
    for i, j in combinations(range(len(values)), 2):
        pairs[values[i] + values[j]].append((i, j))
    core = set()
    for group in pairs.values():
        for (i, j), (k, r) in combinations(group, 2):
            if len({i, j, k, r}) == 4:
                core.update((i, j, k, r))
    return core


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=36311)
    args = parser.parse_args()

    rows = [
        "| n | d | L | D | Y | D/Y | pred exp | work (M~4D) | work (default M) | MITM | core | support in core |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |",
    ]
    configs = [
        (24, 2, 2),
        (24, 3, 2),
        (24, 4, 2),
        (24, 6, 2),
        (32, 3, 2),
        (32, 4, 2),
        (32, 6, 2),
        (32, 8, 2),
    ]
    for n, d, side in configs:
        rng = random.Random(args.seed + n * 100 + d)
        values, support, target = build(n, d, side, rng)
        m = n // 2
        sup_vals = [values[i] for i in support]
        t_set = {sum(sup_vals[i] for i in c) for c in combinations(range(m), m // 2)}
        dd = len(t_set)
        yy = comb(m, m // 2)
        amb = comb(n, n // 4)
        pred = min(0.5, max(0.4057, log2(amb / dd) / n))
        work = {}
        for label, modulus in (
            ("small", next_prime(4 * dd)),
            ("default", next_prime(1 << (n // 2))),
        ):
            result = hgj_permuted_search(
                values,
                target,
                permutations=ceil(4 * n**0.5) * 2,
                residues=8,
                seed=1,
                modulus=modulus,
            )
            work[label] = (
                f"{result.enumerated:.2e}"
                if result.feasible
                else f">{result.enumerated:.1e}"
            )
        core = quadruple_core(values)
        rows.append(
            f"| {n} | {d} | {side} | {dd} | {yy} | {dd / yy:.2f} | {pred:.3f} | "
            f"{work['small']} | {work['default']} | {2 ** (n // 2):.1e} | {len(core)} | "
            f"{set(support) <= core} |"
        )
        print(rows[-1], flush=True)

    lines = [
        "# R13a: the high-energy regime",
        "",
        "Planted weight-`n/2` solutions whose support is a rank-`d` GAP (random "
        "`n`-bit generators, coordinates in `[0, L)`), with random `n`-bit decoys "
        "elsewhere. `pred exp` is the LIFT.md exponent `max(0.4057, "
        "log2(C(n,n/4)/D)/n)` capped at `0.5`. `work` is total enumerated subsets "
        "of `hgj_permuted_search` (budget `8 sqrt n` permutations x 8 residues) "
        "with modulus `~4D` and with the default `~2^(n/2)` modulus; a `>` marks "
        "a run that did not find the solution. `core` is the number of elements "
        "in some additive quadruple `a_i + a_j = a_k + a_l`.",
        "",
        *rows,
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "high_energy.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
