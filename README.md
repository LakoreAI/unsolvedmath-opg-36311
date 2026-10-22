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

The current demo runs the proved reference meet-in-the-middle decision and
witness pipeline, the three-block shared-mask compatibility solver, and modular
bin alias subtraction.

## Checked pipeline

`lean/SubsetSum.lean` re-exports ten modular verification files under
`lean/SubsetSum/`:
- `lean/SubsetSum/Basic.lean`: `HasSum` occurrence specification, two- and
  three-block splits, `meetInMiddle_correct`, `threeBlock_correct`, and
  bounded-magnitude radius bounds.
- `lean/SubsetSum/Witness.lean`: Boolean occurrence-mask semantics (`maskSum`)
  and witness-returning `meetInMiddleWitness` (`meetInMiddleWitness_sound`,
  `meetInMiddleWitness_isSome_iff`).
- `lean/SubsetSum/Reductions.lean`: signed-to-nonnegative and strictly positive
  weight reductions (`hasSum_signed_iff_nonneg`, `hasSum_signed_iff_pos`,
  `flipNegMask_involutive`) and the tie-breaking solution isolation family
  (`isolation_mask_iff`, `isolation_hasSum_iff`, `isolation_unique_mask`).
- `lean/SubsetSum/Representation.lean`: weight-resolved certificates
  (`HasSumWeight`, `hasSumWeight_append`), modular-filter completeness
  (`mem_residues`), mixing concentration/contraction kernels, collision-energy
  decomposition (`collision_energy_split`), and impossibility of coefficient
  shifting for `{0,1}` and `{-1,1}` (`no_coefficient_shifting_01`,
  `no_coefficient_shifting_pm1`).
- `lean/SubsetSum/SharedMask.lean`: disjoint-mask union (`maskSum_orMask_of_disjoint`),
  three-block shared-mask compatibility solver (`sharedMaskSolve_sound`,
  `sharedMaskSolve_isSome_iff`), and exact modular bin alias subtraction
  (`modBin_alias_subtraction`).
- `lean/SubsetSum/HighEnergy.lean`: common-element stripping and Lemma T for
  colliding subsets (`masksDisjoint_diffMask`, `maskSum_diffMask_eq_iff`,
  `diffMask_ne_of_ne`, `lemma_T_forced_disjoint_relation`), scaled-geometric
  transfer barrier (`maskSum_scaled_geomWeights_inj`), discrete Cauchy-Schwarz
  collision energy (`sq_sum_le_length_mul_sumSq`), weight-slice sumset profiles
  (`sliceProfile`), compressible-core MITM (`compressMitm_correct`), HGJ
  modular-filter solver (`hgjSolve_sound`, `hgjSolve_isSome_of_representation`),
  and PESS crowded-interval halving (`pess_crowded_halving`).
- `lean/SubsetSum/Audit049.lean`: high/low-digit decomposition
  (`maskSum_high_low_split`), capped distinct-sum preliminary search
  (`cappedPrelimSolve_sound`), and end-to-end isolated alias-subtraction
  decision (`isolated_alias_decision_iff`).
- `lean/SubsetSum/Audit049Lemmas.lean`: the preprint's Lemma 2.2 deficiency
  bounds in exponentiated form (`coreSums_cons_length_le`,
  `coreSums_length_le_pow`, `coreSums_append_length_le`,
  `coreSums_exchange_length_le`), the flip bijection (5.5) (`maskSum_flip`,
  `xorMask_involutive`, `flip_hits_iff`), and the alias carry (5.4)
  (`alias_carry`).
- `lean/SubsetSum/Audit049Constants.lean`: kernel-decided ledger of every
  scalar inequality in the preprint's exponent bookkeeping (Sections 2, 4, 5
  and Appendix A), including `1.429584295 < 2^0.5168` and `h(0.0567) + 0.0567 < 0.40`.
  It checks arithmetic only, not that these quantities are running times.
- `lean/SubsetSum/Audit049Filter.lean`: `Float` reproduction of the
  Proposition 3.1 filtering moments (numerical, outside the kernel). The
  averages are stable from `N = 32` to `256` at `1.428968` and `1.428847`,
  below `2^0.5168 ≈ 1.430778`.

`lean/Main.lean` is the end-to-end executable demonstration.

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
  SubsetSum.lean          #   root barrel module and axiom checks
  SubsetSum/              #   modular specification and theorem files
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
