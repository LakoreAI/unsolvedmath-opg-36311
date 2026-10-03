# Exact subset sum: proof scope and reproduction

## Outcome

The unrestricted worst-case `O*(2^(n/3))` question is **not proved**.
This project provides exact Python algorithms (meet-in-the-middle,
Schroeppel–Shamir, signed DP), formal correctness results in Lean, reproducible
measurements, and a restricted bounded-magnitude theorem. The restricted result
follows from classical pseudopolynomial dynamic programming and is not claimed
as a new discovery.

## Artifacts

- `src/subset_sum.py` — dependency-free solvers `meet_in_middle`, `schroeppel_shamir`,
  `bounded_dp`, dispatched by `solve(values, target, method)`.
- `tests/test_subset_sum.py` — brute-force differential suite over all three
  solvers.
- `lean/SubsetSum.lean` — Lean 4.19.0 correctness layer (`Std` only).
- `scripts/analysis/benchmark.py` — measurement harness (stdlib only).
- `scripts/analysis/plot_benchmarks.py` — figures and LaTeX tables from the CSV.
- `docs/reports/baselines/paper.tex` (+ `paper.pdf`) — the baselines note.
- `docs/reports/representation/representation.tex` (+ `.pdf`) — the
  representation-technique note.
- `docs/reports/survey/survey.tex` (+ `.pdf`) — the structured survey.
- `docs/analysis/2026-10-03/subset-sum/` — `bench.csv`, `memory.csv`,
  `correctness.csv`, `bench.md`, `provenance.md`, `research-notes.md`.
- `docs/reports/<topic>/figures/`, `docs/reports/<topic>/tables/` — generated
  figures and tables, one set per paper topic.

## Formal scope

`lean/SubsetSum.lean` uses Lean 4.19.0 and `Std` only. The `HasSum` inductive
specification chooses or skips each occurrence once.

| Theorem | What it establishes |
| --- | --- |
| `mem_sums_iff` | Soundness and completeness of exhaustive sum enumeration |
| `sums_length` | Exactly `2^n` enumerated entries, including repetitions |
| `hasSum_append` | Any split reduces to two subset sums adding to the target |
| `meetInMiddle_correct` | Executable reference matching decides the specification |
| `hasSum_magnitude` | Every feasible sum has absolute value at most the input magnitude sum |
| `target_outside_impossible` | A target beyond that radius cannot be feasible |
| `restricted_work_bound` | Algebraic work envelope under `w <= 2^(n/3)` |

The reference matcher uses linear membership; its runtime is not the sorted
Python matcher's runtime. The Lean file does not prove a refinement of the
Python code, the dense DP implementation, the Schroeppel–Shamir control flow,
or operational runtime bounds. The paper supplies mathematical proofs of DP and
Schroeppel–Shamir correctness and of the runtime bounds. Lean 4.19.0 (via
`elan`) was run with a clean rebuild (`lake clean && lake build`); it completed
successfully and all seven theorems depend only on `propext` and `Quot.sound`,
with no `sorryAx`.

## Measurements

`scripts/analysis/benchmark.py` generates deterministic infeasible instances
(even values, odd target) so each solver runs to completion. It records runtime,
work units, peak traced memory, and a feasible witness check, writing CSV plus a
provenance table (commit, interpreter, platform, seed). The measured findings:

- meet-in-the-middle and Schroeppel–Shamir both grow like `2^(n/2)` in time;
- peak memory grows like `2^(n/2)` for meet-in-the-middle and `2^(n/4)` for
  Schroeppel–Shamir;
- the signed DP is effectively linear in `n` for bounded values and dominates
  once `n` is large, but is unusable when the magnitude sum `W` is large.

Finite measurements illustrate the bounds; they prove neither an asymptotic
improvement nor a lower bound.

## Reproduction

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
python3 -m src.subset_sum --values 3 -2 7 0 --target 5 --method ss
python3 scripts/analysis/benchmark.py
uv run python scripts/analysis/plot_benchmarks.py   # figures + tables
cd lean && lake clean && lake build
```

Compile each paper twice from its own directory:

```bash
(cd docs/reports/baselines && pdflatex -interaction=nonstopmode -halt-on-error paper.tex && pdflatex -interaction=nonstopmode -halt-on-error paper.tex)
(cd docs/reports/representation && pdflatex -interaction=nonstopmode -halt-on-error representation.tex && pdflatex -interaction=nonstopmode -halt-on-error representation.tex)
```

## Checks performed

- Python 3.12.3: `tests/test_subset_sum.py` — 7 methods passed, including the
  Schroeppel–Shamir solvers in the exhaustive and seeded differential checks and
  a wide-value witness test. The suite covers 2,783 exhaustive instances, 150
  seeded random instances, single-use and repeated-value cases,
  arbitrary-precision inputs, and validation errors. Every solver is checked
  against independent Boolean-vector enumeration, and each witness is checked
  for unique, in-range indices and the correct sum.
- Benchmark (2026-10-03): `benchmark.py` completed in ~17 s over `n` up to 36
  and wrote all CSV/table/provenance artifacts listed above.
- Paper: `pdflatex` pass 1 and pass 2 both exited 0; output is 4 pages.
  No undefined references or citations remain; only minor overfull/underfull
  box warnings.
- Ruff 0.15.15: lint passes for all of `src/`, `tests/`, and
  `scripts/analysis/`; changed-file formatting checks pass. A repo-wide format
  check flags the untouched `scripts/analysis/plot_representation.py`.
- Lean 4.19.0: `lake clean && lake build` succeeds from scratch; `#eval` outputs
  `true` and `false` as expected; every theorem's axiom report is exactly
  `[propext, Quot.sound]`.
- Repository consolidation: the ML-template code was removed; `src/` now holds
  only the subset-sum research modules. The remaining test suite (30 stdlib
  tests) runs with no third-party packages.

## Phase 0 research artifacts (2026-10-03)

Built for the deep-research plan in `docs/research/subset-sum-n3/PLAN.md`:

- `src/equal_subset_sum.py` — exact ESS signed meet-in-the-middle baseline at
  `O*(3^(n/2))`, plus a deterministic PESS binary-search/MITM solver at
  `O*(2^(n/2))`, and a modular-bucket DP sampler for the randomized high-
  collision approach. Tests compare ESS against a `{-1,0,1}^n` brute-force
  oracle and exhaustively check the sampler on small buckets. The structural
  reductions and full randomized `O*(2^(n/3))` PESS algorithm are not
  implemented.
- `src/dissection.py` — Wagner four-list modular k-sum core plus a verifier.
  Tests check soundness and that solutions are found when many exist.
- `src/hgj.py` — Howgrave-Graham-Joux representation + modular-filter search
  (ported from ePrint 2011/474 Sect. 2.2). Tests recover planted balanced
  weight-`n/2` solutions and validate the balanced sub-enumeration. The
  benchmark `scripts/analysis/hgj_benchmark.py` measures enumeration exponent
  ~`0.385` (theoretical `0.4057`) versus meet-in-the-middle `0.5`, with `4/4`
  success for `n` up to `56`. The optimized BCJ `0.291n` recursion is not
  implemented.
- `scripts/analysis/regimes.py` — regime-aware exponent fit; measured
  `log2(states)` slopes `1.000` (brute), `0.500` (MITM and Schroeppel-Shamir),
  `~0.145` (signed DP on bounded instances). Output `regimes.{csv,md}`.
- `scripts/analysis/mixing_harness.py` — representation counts and random
  subsampling survival; output `mixing.md`. Random weights show `263`
  vanilla representations vs `1` for geometric weights at `n=16`, and a
  random-subsample survival of `54/60` vs `1/60` at `m=10`.
- `tests/test_equal_subset_sum.py`, `tests/test_dissection.py` — all pass;
  together with the subset-sum suite, 15 tests run under the standard library.

### Phase 1 probes (2026-10-03)

- `src/additive.py` (+ `tests/test_additive.py`) — exact `|S(A)|`, collision
  count `F`, additive energy, near-geometric distance, longest AP.
- `scripts/analysis/dichotomy.py` → `dichotomy.{csv,md}`. Falsifies the naive
  dichotomy: dissociated instances (`|S|=2^n`, `F=0`) are far from geometric
  and form the hard "danger zone".
- `scripts/analysis/synthetic_repr.py` → `synthetic_repr.md`. Supports H1:
  random partitions always yield a balanced representation (`200/200`, `n` up
  to 96) retaining `2^(n/2)/poly(n)` representations.
- `scripts/analysis/modular_structure.py` → `modular_structure.md` (R6):
  representations' modular residues are spread (~0.6) for dissociated and
  density-1 families, so dissociativity is not the obstacle; the corrected
  Phase 1 target is pseudo-solution accounting.
- `scripts/analysis/pseudo_solutions.py` → `pseudo_solutions.md` (R7):
  cardinality-resolved target representations show `T=1, P=0` for dissociated,
  geometric, and near-geometric instances, and large pseudo-solution load only
  for easy collision-heavy families. The barrier is the balanced sub-solver
  cost, not an adversarial instance class.
- `scripts/analysis/sub_solver.py` → `sub_solver.md` (R8): analytical exponents
  show the balanced-MITM sub-solver floor is `0.4056n`, `{-1,0,1}` does not
  lower it (minimum at `alpha=0`), and `{0,1}` admits only two parts. The gap
  to the ideal `0.3113n` is precisely the sub-solver.
- `scripts/analysis/birthday_sub_solver.py` → `birthday_sub_solver.md` (R9):
  the surviving decomposition count is ~`Poisson(1)` and hides in a residue
  class of size `L`; birthday/subsampling succeeds with probability `s/L`, so
  it cannot beat the `0.4056n` floor. Reaching `0.3113n` needs a sub-solver
  outside the balanced/birthday family, or a conditional lower bound.
- `scripts/analysis/algebraic_sub_solver.py` → `algebraic_sub_solver.md` (R10):
  full-residue DP/FFT cost `2^(0.5n)` (above the floor) and coarse-DP +
  rejection sampling returns a random element, not the planted one.
- `scripts/analysis/representation_exponents.py` → `representation_exponents.md`
  (R11): reproduced the primary-source complexity models. HGJ 2-part ideal
  `0.3113`, HGJ simple `0.337`, BCJ minimised `0.292` (paper `0.291`). This
  **corrects R8**: the real HGJ algorithm is a 4-way decomposition with the
  unbalanced Schroeppel-Shamir sub-solver, so the "`0.4056n` floor" was a model
  artifact. The obstacle is the average-case → worst-case gap.
- `scripts/analysis/coefficient_shifting.py` → `coefficient_shifting.md`
  (R12): searches sumset factorisations `C = C1 + C2`. The open cases `{0,1}`,
  `{±1}`, `{±2}` have none with multiple representations, while `{-1,0,1}` and
  `{±3}` do — independently reproducing Randolph-Węgrzycki's stated frontier
  and identifying the obstruction as the absence of coefficient shifting.
- Findings and the corrected Phase 1 direction are in
  `docs/research/subset-sum-n3/PHASE1.md`.

These are infrastructure and measurement results. The full HGJ/BCJ
representation port and the `O*(2^(n/3))` PESS algorithm are listed as pending
in `PLAN.md` and are not claimed.

The tests and measurements are finite implementation checks. They do not
establish an asymptotic improvement or resolve the open question.
