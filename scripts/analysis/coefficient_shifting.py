#!/usr/bin/env python3
"""R12: why does the worst-case representation technique avoid C={0,1} and C={+-1}?

Randolph-Wegrzycki (arXiv:2511.10823) break the worst-case Meet-in-the-Middle
barrier for most coefficient sets C using "coefficient shifting": a sumset
factorisation C = C1 + C2 in which coefficients acquire multiple
representations (e.g. {0,1} + {-3,-2,1,2} = [+-3], where +-2 has two
representations). This script computes, for each C, the coefficient
representation profile over factorisations C1 + C2 = C, and shows that
{0,1} and {+-1} admit only *trivial* factorisations, so shifting cannot be
applied. This matches the paper's stated open cases.

Writes docs/analysis/2026-10-03/subset-sum/coefficient_shifting.md.
"""

import argparse
from itertools import combinations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "docs" / "analysis" / "2026-10-03" / "subset-sum"


def sumset(c1, c2):
    return {a + b for a in c1 for b in c2}


def representation_profile(c1, c2):
    profile = {}
    for a in c1:
        for b in c2:
            profile[a + b] = profile.get(a + b, 0) + 1
    return profile


def find_factorisations(target, radius=3, max_size=4):
    """All C1, C2 subset of [-radius, radius] with C1 + C2 == target."""
    universe = list(range(-radius, radius + 1))
    subsets = []
    for size in range(0, max_size + 1):
        subsets.extend(combinations(universe, size))
    subsets = [frozenset(s) for s in subsets]
    target = set(target)
    out = []
    for c1 in subsets:
        for c2 in subsets:
            if sumset(c1, c2) == target:
                out.append((c1, c2))
    return out


def summarise(factorisations):
    best = None
    nontrivial = 0
    for c1, c2 in factorisations:
        profile = representation_profile(c1, c2)
        if not profile:
            continue
        min_reps = min(profile.values())
        max_reps = max(profile.values())
        if max_reps > 1:
            nontrivial += 1
        if best is None or (max_reps, -min_reps) > (best[0], -best[1]):
            best = (max_reps, min_reps, tuple(sorted(c1)), tuple(sorted(c2)))
    return nontrivial, best


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--radius", type=int, default=3)
    args = parser.parse_args()

    targets = {
        "Subset Sum {0,1}": (0, 1),
        "Partition {+-1}": (-1, 1),
        "Equal Subset Sum {-1,0,1}": (-1, 0, 1),
        "Balancing [+-2]": (-2, -1, 1, 2),
        "Balancing [+-3]": (-3, -2, -1, 1, 2, 3),
        "Balancing [-2:2]": (-2, -1, 0, 1, 2),
    }

    rows = []
    for name, target in targets.items():
        facts = find_factorisations(target, radius=args.radius)
        nontrivial, best = summarise(facts)
        rows.append(
            {
                "name": name,
                "target": str(target),
                "factorisations": len(facts),
                "nontrivial": nontrivial,
                "best_max_reps": best[0] if best else 0,
                "best_min_reps": best[1] if best else 0,
                "example": f"{best[2]} + {best[3]}" if best else "-",
            }
        )

    lines = [
        "# R12: coefficient shifting and the open cases",
        "",
        "Factorisations `C1 + C2 = C` with `C1, C2` subsets of",
        f"`[-{args.radius}, {args.radius}]`, size <= 3. `max reps` is the largest",
        "number of representations any coefficient acquires; shifting needs a",
        "coefficient with >= 2 representations.",
        "",
        "| C | # factorisations | # nontrivial | best max reps | best min reps | example |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for r in rows:
        lines.append(
            "| {name} | {factorisations} | {nontrivial} | {best_max_reps} | "
            "{best_min_reps} | `{example}` |".format(**r)
        )
    lines += [
        "",
        "Reading: `{0,1}` (Subset Sum) and `{+-1}` (Partition) admit only trivial",
        "factorisations, so no coefficient acquires extra representations and",
        "coefficient shifting cannot be applied. `{-1,0,1}` already has the",
        "0 = 0+0 / 1+(-1) / (-1)+1 freedom; `[+-3]` is handled by the paper's",
        "`{0,1} + {-3,-2,1,2}` factorisation, where `+-2` gets two",
        "representations. This is exactly the paper's stated frontier: the lack",
        "of a nontrivial sumset factorisation (equivalently, of a 0 coefficient)",
        "is why the worst-case technique stalls at `C={0,1}` and `C={+-1}`.",
    ]
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "coefficient_shifting.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {args.out / 'coefficient_shifting.md'}")
    print("\n".join(lines[6:]))


if __name__ == "__main__":
    main()
