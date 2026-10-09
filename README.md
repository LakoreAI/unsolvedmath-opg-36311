# OPG-36311: Exact Subset Sum Research

> **Warning.** This repository uses AI to attack an open conjecture. Almost all of
> the code, proofs, experiments and papers here were produced by AI under my
> direction. If anything in it turns out to be a real new finding, it says nothing
> about how good I am at math. It only shows how well I can use AI to work on math.
> Treat every claim as unreviewed until a human mathematician has checked it; the
> proofs outside the Lean layer are pen-and-paper and may contain errors.

A Lean-first research repository on exact subset sum: checked executable
reference algorithms, correctness proofs, reproducible legacy measurements,
and a roadmap toward the open `O*(2^(n/3))` worst-case bound.

**The general worst-case `O*(2^(n/3))` question is not solved here.** The
repository proves the meet-in-the-middle correctness reduction, gives an
`O*(2^(n/3))` result for the restricted family
`sum(abs(a_i)) <= 2^floor(n/3)`, ports the representation technique, and
documents which hypotheses about the barrier hold and which fail. The
repository includes a [baselines paper](docs/reports/baselines/paper.tex), a
[representation paper](docs/reports/representation/representation.tex), a
[mixing note](docs/reports/mixing/mixing.tex), a
[conditional-bounds note](docs/reports/lift/lift.tex), and a
[survey](docs/reports/survey/survey.tex); see the
[validation report](docs/reports/validation.md) for scope.

## Lean quickstart

Requires Lean 4.19.0 via elan; the Lean project has no mathlib dependency.

```bash
cd lean && lake build
cd lean && lake env lean Main.lean
```

The current demo runs the proved reference meet-in-the-middle decision
pipeline. Its correctness theorem is `SubsetSum.meetInMiddle_correct`.

## Checked pipeline

`lean/SubsetSum.lean` defines the subset-selection specification and proves
correctness of the executable meet-in-the-middle decision procedure. It also
proves contiguous two- and three-block decomposition lemmas, a
weight-resolved representation split, and modular-filter completeness.
`lean/Main.lean` is the sole end-to-end executable demonstration.

The former Python implementations, tests, analysis scripts, and package
metadata have been removed. Their published measurements and reports remain
under `docs/` as historical research artifacts.

## Measurements and research

- Measurements, figures, and provenance: `docs/analysis/2026-10-03/subset-sum/`,
  `docs/analysis/2026-10-05/subset-sum/`, and `docs/analysis/2026-10-06/subset-sum/`.
- Papers (source, PDF, figures, tables): `docs/reports/<topic>/`.
- Deep-research program toward the open bound: `docs/research/subset-sum-n3/`
  (`report.md` — 20 sourced approach items; `PLAN.md`; `PHASE1.md`;
  `TRANSFER.md` — why the PESS `2^(n/3)` structure does not transfer to `{0,1}`;
  `ATTACK.md` — reducing the `{0,1}` bound to a target-problem mixing dichotomy;
  `MIXING.md` — the proved concentration step and the lifting gap;
  `NEXT.md` — literature check, average-energy lemma, and the obstruction;
  `LIFT.md` — single-prime lift under a distinct-sums hypothesis;
  `HIGH_ENERGY.md` — forced relations in the remaining high-energy regime;
  `EXPERT_QUESTIONS.md` — two self-contained questions for expert review).
- Plan and progress: [`docs/TODO.md`](docs/TODO.md).

## Repository layout

```
lean/                     # Lean 4.19.0 correctness layer
  Main.lean               #   executable reference pipeline
  SubsetSum.lean          #   specification and checked theorems
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
