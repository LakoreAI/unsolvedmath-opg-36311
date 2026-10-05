# OPG-36311: Exact Subset Sum Research

A dependency-free research repository on exact subset sum: correct implementa-
tions, Lean-checked correctness proofs, reproducible measurements, and a
roadmap toward the open `O*(2^(n/3))` worst-case bound.

**The general worst-case `O*(2^(n/3))` question is not solved here.** The
repository proves the meet-in-the-middle correctness reduction, gives an
`O*(2^(n/3))` result for the restricted family
`sum(abs(a_i)) <= 2^floor(n/3)`, ports the representation technique, and
documents which hypotheses about the barrier hold and which fail. The
repository includes a [baselines paper](docs/reports/baselines/paper.tex), a
[representation paper](docs/reports/representation/representation.tex), and a
[survey](docs/reports/survey/survey.tex); see the
[validation report](docs/reports/validation.md) for scope.

## Quickstart

Requires Python 3.12+. The core modules and tests need no third-party packages.

```bash
python3 -m src.subset_sum --values 3 -2 7 0 --target 5
python3 -m src.subset_sum --values 2 4 8 --target 7 --method ss
python3 -m unittest discover -s tests -p "test_*.py" -v

# Lean 4.19.0 via elan; no mathlib dependency
cd lean && lake build
```

Plotting uses matplotlib (`uv run python scripts/analysis/plot_benchmarks.py`);
the report generator uses PyYAML.

## Modules (`src/`)

| Module | Contents |
| --- | --- |
| `subset_sum.py` | Exact subset sum: sorted meet-in-the-middle, Schroeppel-Shamir (`ss`), signed dense DP (`dp`), dispatched by `solve(values, target, method)`. |
| `equal_subset_sum.py` | ESS via signed meet-in-the-middle (`O*(3^(n/2))`); PESS via binary-search MITM (`O*(2^(n/2))`); modular-bucket sampler. |
| `dissection.py` | Wagner four-list modular k-sum core and verifier. |
| `hgj.py` | Howgrave-Graham-Joux representation + modular-filter search for hard knapsacks. |
| `representation.py` | Candidate `{0,1}` pipeline: gcd reduction, superincreasing greedy, HGJ filter, MITM fallback; mixing-coverage helper. |
| `additive.py` | Additive-combinatorics probes: `\|S(A)\|`, collision count `F`, additive energy, modular residue profiles, cardinality counts. |

All solvers are exact and return occurrence-index witnesses (or `None`). `ss`
is `O*(2^(n/2))` time with `O*(2^(n/4))` space; the DP is pseudopolynomial in
`W = sum(abs(a_i))`.

## Measurements and research

- Measurements, figures, and provenance: `docs/analysis/2026-10-03/subset-sum/`.
- Papers (source, PDF, figures, tables): `docs/reports/<topic>/`.
- Deep-research program toward the open bound: `docs/research/subset-sum-n3/`
  (`report.md` — 20 sourced approach items; `PLAN.md`; `PHASE1.md`;
  `TRANSFER.md` — why the PESS `2^(n/3)` structure does not transfer to `{0,1}`;
  `ATTACK.md` — reducing the `{0,1}` bound to a target-problem mixing dichotomy;
  `MIXING.md` — the proved concentration step and the lifting gap).
- Plan and progress: [`docs/TODO.md`](docs/TODO.md).

## Repository layout

```
src/                      # dependency-free research modules
scripts/analysis/         # benchmarks, probes, figure/table generators
tests/                    # standard-library unittest suites
lean/                     # Lean 4.19.0 correctness layer
docs/                     # all documents (see docs/README.md)
  analysis/<date>/<topic>/#   measured outputs (CSV, markdown)
  reports/<topic>/        #   papers (source, PDF, figures, tables)
  reports/validation.md   #   repo-wide validation record
  research/<topic>/       #   deep-research workspace (outline, results, plans)
```

## Documentation

All documents live under `docs/`. See [docs/README.md](docs/README.md) for the
convention.

## License

Released under the repository [LICENSE](LICENSE).
