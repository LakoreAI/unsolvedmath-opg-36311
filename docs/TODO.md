# TODO — Exact Subset Sum research

Canonical plan for this repository, kept in `docs/` per the docs convention.
Living research log: `docs/research/subset-sum-n3/` (`report.md`, `PLAN.md`,
`PHASE1.md`). Measurements: `docs/analysis/2026-10-03/subset-sum/` (R1–R21)
and `docs/analysis/2026-10-05/subset-sum/` (R13/R16/R17 follow-ups).

## 0. Status snapshot

**Question.** Worst-case `O*(2^(n/3))` for exact subset sum (`{0,1}`) is
**open**. The repository builds correct baselines, a Lean correctness layer,
reproducible measurements, three papers, and a research program that has
isolated the frontier.

**Worst-case landscape (sourced).**

| Algorithm | Time | Space | Setting |
| --- | --- | --- | --- |
| Horowitz–Sahni (1974) | `O*(2^(n/2))` | `O*(2^(n/2))` | worst case |
| Schroeppel–Shamir (1979/81) | `O*(2^(n/2))` | `O*(2^(n/4))` | worst case |
| Chen–Jin–Randolph–Servedio (2023) | `O(2^(n/2) n^(-0.5023))` | `O*(2^(n/4))` | worst case |
| Nederlof–Węgrzycki (2021) | `O*(2^(0.5n))` | `O*(2^(0.249999n))` | worst case, randomized (OV) |
| Belova et al. (ESA 2024) | `O*(2^(0.5n))` | `O*(2^(0.246n))` | worst case |
| Howgrave–Graham–Joux (2010) | `2^(0.337n)` | `2^(0.256n)` | hard/random knapsack |
| Becker–Coron–Joux (2011) | `2^(0.291n)` | — | hard/random knapsack |
| Randolph–Węgrzycki (2025) | `|C|^((0.5-ε)n)` | — | worst case, most constant `C` |

**Frontier (R11–R12, R19–R21, P2.1).** The obstacle is **not** a sub-solver or
an instance class: the representation technique already reaches `0.291n`
(average case), and the open coefficient sets `{0,1}`, `{±1}`, `{±2}` are
exactly those with no nontrivial sumset factorisation ("coefficient shifting").
The barrier is the **average-case → worst-case gap**. Two further routes are
closed: cheap collisions `c` with `c.a = 0` have support `~n/2`, so they do not
multiply solutions (R19–R21); and pairwise sumsets in the three-block split stay
`>= 2^(0.66n)` in the hard band, so Phase 2 needs cancellation across all three
blocks at once, not one pairwise sumset (P2.1).

**Structural facts.** (i) `|a_i| ≤ poly(n)` ⇒ dense DP is polynomial.
(ii) Superincreasing (powers of two) are easy. (iii) Hardness sits near density
`d ≈ 1`. (iv) Powers of two give `2^n` distinct sums yet are easy, so distinctness
is not hardness.

## 1. Repository hygiene — done

- [x] A1. Papers arranged under `docs/reports/<topic>/` (`baselines/`,
      `representation/`, `survey/`); `docs/reports/validation.md` at reports root.
- [x] A2. `README.md`, `docs/RESEARCH.md`, `docs/README.md` link to the topic paths.
- [x] A3. Removed ML-template code and placeholder dirs; `src/` is research-only.
- [x] A4. `.gitignore` ignores Python, `.venv`, `.env`, and LaTeX/Lean build
      artifacts (`*.aux`, `*.log`, `*.fls`, `*.fdb_latexmk`, `lean/.lake/`).

## 2. Algorithms and tests — done

- [x] B1. `src/subset_sum.py`: meet-in-the-middle, Schroeppel–Shamir (`ss`),
      signed DP (`dp`), `solve(...)`.
- [x] B2. `src/equal_subset_sum.py`: ESS signed MITM (`O*(3^(n/2))`) and
      PESS binary-search MITM (`O*(2^(n/2))`).
- [x] B3. `src/dissection.py`: Wagner four-list modular core + verifier.
- [x] B4. `src/hgj.py`: Howgrave-Graham–Joux representation search.
- [x] B5. `src/additive.py`: `|S(A)|`, collision count `F`, additive energy,
      modular residue profiles, cardinality counts.
- [x] B6. Tests (`tests/`): `test_subset_sum`, `test_equal_subset_sum`,
      `test_dissection`, `test_hgj`, `test_additive` — stdlib tests, all pass (68 at last count).
- [x] B7. Modules are dependency-free (stdlib only).

## 3. Measurement harnesses — done

- [x] C1. `scripts/analysis/benchmark.py` → `bench.csv`, `memory.csv`,
      `correctness.csv`, `bench.md`, `provenance.md`.
- [x] C2. `scripts/analysis/plot_benchmarks.py` → `docs/reports/baselines/figures`,
      `docs/reports/baselines/tables`.
- [x] C3. `scripts/analysis/regimes.py` → exponent fits (`regimes.{csv,md}`).
- [x] C4. `scripts/analysis/mixing_harness.py` → `mixing.md`.
- [x] C5. `scripts/analysis/hgj_benchmark.py` → `hgj.{csv,md}`.
- [x] C6. `scripts/analysis/dichotomy.py`, `synthetic_repr.py`,
      `modular_structure.py`, `pseudo_solutions.py` → `*.md`.
- [x] C7. `scripts/analysis/sub_solver.py`, `birthday_sub_solver.py`,
      `algebraic_sub_solver.py`, `representation_exponents.py`,
      `coefficient_shifting.py`, `plot_representation.py`.

## 4. Papers — done

- [x] P1 `docs/reports/baselines/` — correctness (MITM, signed DP,
      Schroeppel–Shamir), Lean layer, bounded-magnitude theorem, measurements,
      figures, tables. (4 pp.)
- [x] P2 `docs/reports/representation/` — reproduced HGJ `0.337` and BCJ `0.291`
      (ideal `0.3113`) from primary sources; structural probes; the frontier.
      (3 pp.)
- [x] P3 `docs/reports/survey/` — structured survey, 14 sections, 10 tables,
      25 references, chronology. (5 pp.)
- [x] P4. Remove all mentions of the problem-source name from the `.tex` files.
- [x] P5. All three papers compile cleanly (`pdflatex` twice, no errors/undefined
      refs); figures/tables generated by scripts.
- [x] P6 `docs/reports/mixing/` — "Elementary Mixing Bounds and Experiments for
      the Representation Technique in Subset Sum": concentration/contraction
      lemmas (Lean-formalized), the
      average-collision-energy bound `O(Y log Y)`, and full-pipeline experiments
      across adversarial families; argues the `{0,1}` barrier is the balanced
      sub-solver, not mixing. (3 pp.)

- [x] P7 `docs/reports/lift/` — "Conditional Bounds for Representation-Based Subset Sum
      via Profile Completeness and a Distinct-Sums Parameter": profile completeness theorem
      (`sqrt(8/(pi n))`), single-prime lift
      with `D*` and `N_t`, forced-relation lemma, conditional exponent table, measurements.
      Conditional/partial throughout; no unconditional worst-case claim. (3 pp.)

## 5. Verification — done

- [x] E1. `python3 -m unittest discover -s tests -p "test_*.py"` — 82 pass.
- [x] E2. Ruff lint clean and repo-wide `ruff format --check` clean across
      `src/`, `tests/`, `scripts/analysis/` (including the previously flagged
      `scripts/analysis/plot_representation.py`).
- [x] E3. Lean 4.19.0 `lake build` passes; axioms `[propext, Quot.sound]` only
      (the weight/residue lemmas add to the correctness layer; see R17).
- [x] E4. `docs/reports/validation.md` records the checks actually run.

## 6. Research program (`docs/research/subset-sum-n3/`) — done through R21 + P2.1

- [x] R1. `/research` outline + 32-field schema; 20 items.
- [x] R2. `/research-deep` — 20 validated JSON results (100% coverage).
- [x] R3. `/research-report` — `report.md` + `PLAN.md`.
- [x] R4. Phase 0: Wagner k-sum, ESS/PESS baseline, regime benchmark, mixing harness.
- [x] R4b. HGJ representation search (`src/hgj.py`), measured exponent `~0.385`.
- [x] R5–R7. Probes: dissociativity and pseudo-solutions are **not** the barrier.
- [x] R8. Balanced sub-solver model (`sub_solver.py`) — later corrected by R11.
- [x] R9. Birthday/subsampling cannot beat the (wrong-model) floor.
- [x] R10. Algebraic counting hits the counting-vs-finding gap.
- [x] R11. Reproduced HGJ `0.337` / BCJ `0.291` from primary sources; identified
      the barrier as average-case → worst-case, not a sub-solver.
- [x] R12. `coefficient_shifting.py`: open cases `{0,1}`, `{±1}`, `{±2}` are
      exactly those with no nontrivial sumset factorisation.
- [x] R19. `collision_mitm.py`: collisions are *global* (they need many items);
      in the hard band `0.9 <= beta <= 1.25` meet-in-the-middle halves show no
      repeats (work ratio `~0.99` over 32 splits) and birthday sampling needs
      `2^(0.55n)`. See `collision_mitm.md`.
- [x] R20. `bucket_collisions.py`: Jin-Wu residue-class sampling finds
      equal-sum pairs in the hard band at `2^(0.42n)` vs `2^(0.5n)` MITM
      (`n = 24`, density 1) and stays below MITM at `beta = 1.25`. It finds
      collisions, not subset-sum solutions. See `bucket_collisions.md`.
- [x] R21. `collision_amplification.py` **(negative; closes the collision
      route)**: sampled collisions have support `~n/2` (0.50–0.56), so each is
      compatible with a fixed solution with probability `~2^(1-n/2)`; over
      `n = 16, 20, 24` inputs kept 1–3 solutions. Cheap collisions do not
      multiply solutions. See `collision_amplification.md`.
- [x] P2.1. `three_block.py` **(negative for the pairwise route)**: smallest
      pairwise-sumset exponents stay `~0.66` for `beta >= 0.7`, so listing one
      pairwise sumset and matching the third block cannot beat `2^(n/2)`. Phase
      2 must cancel across all three blocks at once. See `three_block.md`.

## 7. Research frontier and follow-ups (R13–R18)

- [ ] R13. **Attack `{0,1}` worst case.** Seek a worst-case mechanism that does
      not need coefficient shifting: a canonical sumset / `{0,1}`-specific
      compatibility certificate, a new mixing lemma, or a `{0,1}`-version of
      the Equal-Subset-Sum pseudosolution construction. Success = any worst-case
      exponent `< 0.5`; target = `O*(2^(n/3))`. Fallback = a clean barrier.
      Barrier statement: `docs/research/subset-sum-n3/TRANSFER.md` shows the
      PESS engine (Lemma 4) needs the pigeonhole promise and fails without it.
      Attack plan: `docs/research/subset-sum-n3/ATTACK.md` reduces the bound to
      (i) a target-problem mixing dichotomy, (ii) a disjointness (sparse OV)
      compatibility certificate, and (iii) the balanced sub-solver (R8–R11).
      `MIXING.md` proves the elementary concentration step (poor mixing ⇒
      `|A-A mod p| ≤ s²`, with the `s=1` strip-and-recurse case), **formalized in
      Lean** (`value_diff_mem_wsum_diff`, `value_diff_mod_mem_wsum_mod_diff`,
      `dvd_listSum_sub_length_mul`), derives the collision-energy criterion
      `E_p = (1/p)Σ_k |e_w(ζ^k)|²`, and isolates the remaining **higher-order
      energy / random-prime lifting** gap. Counterexample search
      (`mixing_counterexample.md`) finds no poorly-mixing hard instance.
      `NEXT.md` adds the **average-over-primes energy lemma** (`avg E_p =
      O(Y log Y)`, so a random prime mixes to within a polylog; `average_energy.md`
      shows even the pointwise min coverage stays `≥ 0.27`) and sharpens the
      target to: *find the adversarial poorly-mixing family, or identify the
      sub-solver/profile barrier*. Also flags the unsound Salas preprint
      (arXiv:2503.20162) and the rigorous tools (RW24 small doubling, AKKN
      density, BSG/Freiman/Shkredov energy→GAP). Candidate pipeline
      `src/representation.py` (gcd + superincreasing greedy + HGJ filter + MITM
      fallback), measured correct on adversarial families
      (`subset_sum_pipeline.md`). Evidence: `mixing_dichotomy.md` — only
      structured families mix poorly. Next: prove the lifting, or find a
      poorly-mixing hard instance (a clean barrier).
      **Profile barrier resolved (2026-10-06).** `docs/analysis/2026-10-06/subset-sum/profile_permutation.md`: a
      random permutation balances the support with probability
      `~sqrt(8/(pi n))`, so completeness costs `O(sqrt n)` permutations, not
      `2^(0.811n)` (`src.hgj.hgj_permuted_search`, `balanced_probability`).
      The remaining barrier is mixing / accounting. A prime filter modulus beats
      the power-of-two default on structured families. Small-`n` total work still
      exceeds MITM (the polynomial factor dominates), so this is an asymptotic
      statement, not a speedup.
- [ ] R13a. **Single-prime lift (conditional result).** `LIFT.md`: for any
      instance whose solution support has `D` distinct weight-`n/4` sub-sums,
      time is `poly(n)(2^{0.4057n} + C(n,n/4)/D)`; below `2^{n/2}` iff `D >
      2^{0.311n}`. Remaining: prove/refute a hard instance with `D <= 2^{0.311n}`.
      `docs/analysis/2026-10-06/subset-sum/lift_check.md` checks the coverage step.
      `HIGH_ENERGY.md`: rigorous forced-relation lemma (`D < C(m/2+k,k)` => relation of
      length `<= 2k`); with the relation known to lie in the support the regime is solved at
      exponent `< 0.5` for every `delta`; the open step is bounding collisions among
      `Theta(n)`-subsets of all inputs (few: branch; many: AKKN band).
      Evidence: `docs/analysis/2026-10-06/subset-sum/{high_energy,relation_length}.md`.
      Algorithm attempt (2026-10-06): `src/compress_mitm.py` (exact; compressible-core MITM
      `sqrt(2^|R| |Sigma(C)|)`, core by short relations). `docs/analysis/2026-10-06/subset-sum/
      {relation_detect,relation_core,compress_eval}.md`: LLL fails where short subset
      relations still work; speedups `7-25x` at `n = 32` rank 3-4, none at rank 8 or on random.
      Quotient-by-relations idea ruled out (random: prune fraction `2^{-0.08n}`).
- [ ] R14. **Conditional lower bound.** Attempt a reduction making a fast
      `{0,1}` sub-solver imply progress on modular subset sum / `k`-SUM /
      lattice problems (Jin–Williams–Zhang tie PESS to lattice hardness).
- [x] R15. **Reproduce the BCJ concrete algorithm.** Done at toy size:
      `src/bcj_tree.py` is the three-level tree (eight leaf lists, `M_omega`,
      `M_kappa`, `M_nu`, consistency filters) with exact solutions at `n = 16, 32`;
      `docs/analysis/2026-10-06/subset-sum/bcj_tree_lists.md` shows measured list
      sizes match BCJ's model (leaf `1.00`, kappa `0.92-0.98`, nu `1.16-1.35`) and a
      constant per-attempt success `0.13-0.20`. The `0.291n` exponent is asymptotic
      and not readable at `n <= 32`; leaves are enumerated directly, not by the
      birthday split. (Original task: port the three-level
      `{-1,0,1}` construction (Algorithm 1 + eight lists) and verify the
      `0.291n` curve empirically.)
- [x] R16. **Port `O*(2^(n/3))` PESS (Jin–Williams–Zhang, ESA 2025).**
      - R16a: `close_pairs_structured` runs the structural close-pair search as
        a *complete* branch-and-bound: same pairs as the `2^(n-k)` reference,
        but polynomially many nodes on a nearly geometric input (measured
        `visit e ~ 0.3`, decreasing in `n`) and exponential only on
        collision-heavy inputs (`pess_structure.md`).
      - R16b: `jwz_disjoint_close_pairs` computes the poly(n)-size disjoint
        close-pair set `D` of Lemma 9 from the geometric proxy `2^i` (forcing
        every suffix index `j` with `2^j >= 6n^2 2^k` to the opposite side),
        exhaustive-tested against brute force on valid PESS inputs and measured
        to stay within the `200 n^5` bound while the naive suffix enumeration
        is `3^(n-k)` (`jwz_close_pairs.md`). `pess_jwz_pigeonhole_equal_subset_sum`
        applies the Equation (1) prefix reduction and the Lemma 10 reduction to
        `W_{X,Y} = (w_1..w_k, w(X)-w(Y))`, lifting the witness. The asymptotics
        use Lemma 6 (subsampling); the poly(n) constants are large, so this is
        an asymptotic reproduction, not a practical speedup at small `n`.
      Baseline, modular-bucket counting/sampling primitive, and Jin-Wu
      `O*(2^(0.4n))` also exist.
- [x] R17. **Formalize.** `lean/SubsetSum.lean` now proves the weight-resolved
      split lemma `hasSumWeight_append` (the representation decomposition
      `x = y + z` with `ku + kv = k`) and the modular-filter completeness lemma
      `mem_residues` (every feasible sum survives a residue filter), plus
      `hasSumWeight_sound/completes/le_length`. Axioms stay `[propext,
      Quot.sound]`; clean `lake build`.
- [ ] R18. **Survey upkeep.** Re-check the open-case map against the newest
      primary sources before any external release. Pending: Equal-Subset-Sum results
      arXiv 2608.08260 (Ye, `(5/3)^n`, one-sided Monte Carlo) and 2607.09289 (Yamano-Shibuya,
      `1.6994^n`; plain ESS, not PESS) are not yet in `docs/reports/survey/`; verify them against
      the primary text first (only abstracts were read).

## 8. Standing commands (do not lose)

```bash
# tests + lint
python3 -m unittest discover -s tests -p "test_*.py"
uv run --no-project --with ruff==0.15.15 ruff check src/ tests/ scripts/analysis/
uv run --no-project --with ruff==0.15.15 ruff format --check src/ tests/ scripts/analysis/

# measurements + figures/tables
python3 scripts/analysis/benchmark.py
python3 scripts/analysis/regimes.py
python3 scripts/analysis/dichotomy.py
python3 scripts/analysis/pseudo_solutions.py
python3 scripts/analysis/modular_structure.py
python3 scripts/analysis/synthetic_repr.py
python3 scripts/analysis/representation_exponents.py
python3 scripts/analysis/coefficient_shifting.py
uv run --no-project --with matplotlib python3 scripts/analysis/plot_benchmarks.py
uv run --no-project --with matplotlib python3 scripts/analysis/plot_representation.py

# Lean
cd lean && PATH="$HOME/.elan/bin:$PATH" lake clean && PATH="$HOME/.elan/bin:$PATH" lake build

# papers (twice each, from their own dir)
(cd docs/reports/baselines && pdflatex -interaction=nonstopmode -halt-on-error paper.tex && pdflatex -interaction=nonstopmode -halt-on-error paper.tex)
(cd docs/reports/representation && pdflatex -interaction=nonstopmode -halt-on-error representation.tex && pdflatex -interaction=nonstopmode -halt-on-error representation.tex)
(cd docs/reports/survey && pdflatex -interaction=nonstopmode -halt-on-error survey.tex && pdflatex -interaction=nonstopmode -halt-on-error survey.tex)
```
