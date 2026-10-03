# Plan: toward O*(2^(n/3)) for worst-case exact subset sum

Derived from the 20-item deep-research pass in `results/` (see `report.md`).
This is a research roadmap, not a solution. The target for the vanilla
`{0,1}` decision problem is open; it is already *attained* for nearby variants.

## Executive verdict

| Fact | Consequence for the plan |
| --- | --- |
| Vanilla `{0,1}` worst case: `2^(n/2)`, only `2^(n/2)/n^0.5023` known (Chen-Jin-Randolph-Servedio 2023) | Everything must beat a 50-year-old barrier |
| Pigeonhole Equal Subset Sum: `O*(2^(n/3))` (Zhang 2024; Jin-Williams-Zhang ESA 2025) | The exponent `1/3` is reachable when a promise creates many solutions |
| Worst-case quantum subset sum: `O*(2^(2n/7))` (Chukhin et al. 2026) | `1/3` is not information-theoretically special |
| Representation technique now worst-case for most coefficient sets `C`, but **not** `C={0,1}` or `C={±1}` (Randolph-Węgrzycki 2025) | The frontier is two stubborn coefficient sets |
| No hypothesis (ETH/SETH/3SUM/MinConv) implies a `2^(Ω(n))` barrier; only the unproven MITM conjecture (Randolph thesis; EOSS undercuts its naive form) | A `2^(1/2−ε)n` breakthrough is not ruled out |
| Dense / small-target regime is essentially solved near-linearly | Hardness lives in the sparse, large-value regime |

**Highest-probability route:** move the representation/mixing technique to the
two remaining coefficient sets (`C={0,1}` for vanilla, `C={±1}` for Partition)
by *synthesizing* many representations and proving a worst-case structure-vs-
randomness dichotomy. **Second route:** exploit sumset structure so the
three-block `2^(n/3)`-size 3SUM becomes subquadratic.

## Phase 0 — infrastructure (status)

- [x] 0.1. Wagner four-list modular k-sum core (`src/dissection.py` + tests): the
      engine of dissection; finds a 4-sum mod `2^n` in ~`2^(n/3)` time with
      `2^(n/3)`-sized lists.
- [x] 0.2a. HGJ representation + modular-filter search (`src/hgj.py` + tests),
      ported from ePrint 2011/474 Sect. 2.2. Planted balanced weight-`n/2`
      solutions recovered `4/4`; measured enumeration exponent **0.385** vs
      meet-in-the-middle `0.5` (theoretical HGJ `h(1/4)/2 = 0.4057`).
- [ ] 0.2b. Optimized BCJ `0.291n` recursion (nested modular sub-knapsack
      solvers and weight balancing) — not implemented. The balanced
      `C(n/2,n/8)` sub-enumeration here is the weak HGJ, not the full attack.
- [x] 0.3. ESS/PESS baseline (`src/equal_subset_sum.py` + tests): exact signed
      meet-in-the-middle at `O*(3^(n/2))`; documents that the known
      `O*(2^(n/3))` PESS algorithm (Jin-Williams-Zhang) is not reimplemented.
- [ ] 0.4. Port the `O*(2^(n/3))` PESS algorithm and the `F = sum_t max(0,
      count(t)-1)` structural machinery.
- [x] 0.5. Regime-aware exponent benchmark (`scripts/analysis/regimes.py`).
- [x] 0.6. Mixing harness (`scripts/analysis/mixing_harness.py`).

### Observed (Phase 0, 2026-10-03)

- `regimes.py`: measured bit-exponent (slope of `log2(states)` vs `n`) is
  `1.000` for brute force, `0.500` for MITM and Schroeppel-Shamir, and `~0.145`
  for the signed DP on bounded instances — the asymptotics show up in the data.
- `mixing_harness.py` (n=16): random weights have `263` representations for
  vanilla `{0,1}` vs `1` for geometric weights; random 10-of-16 subsamples keep
  a representation in `54/60` random cases but only `1/60` geometric cases.
  This is the structure-vs-randomness dichotomy H2 depends on.

## Phase 1 — the core: break `C={0,1}` and `C={±1}`

Testable hypotheses:
- **H1 (synthetic representations).** Coefficient shifting and random
  restrictions can manufacture many representations of a `{0,1}` solution
  without changing satisfiability — the trick that makes Either-Or Subset Sum
  work (`2^(0.461n)`, item 17).
- **H2 (worst-case dichotomy).** For every input, *either* the subset-sum set has
  low additive energy / AP-like structure (then FFT/Kneser gives fast search),
  *or* it has many representations (then dissection/mixing applies). Prove one
  of the two always holds, as Randolph-Węgrzycki do for larger `C`.
- **H3 (pseudosolution recovery).** Adapt their compatibility-certificate
  machinery to `C={±1}`/`{0,1}` (item 3).

Milestone: any **worst-case exponent `< 0.5`** for vanilla subset sum is a
publishable breakthrough; matching `1/3` is the target.

### Phase 1 status (2026-10-03) — see `PHASE1.md`

- **H1 supported.** Random partitions always supply a balanced representation
  (`200/200` for `n` up to 96) and retain `2^(n/2)/poly(n)` representations.
- **H2 falsified as stated.** `F=0` does *not* imply near-geometric: generic
  *dissociated* instances (`|S(A)|=2^n`, values up to `2^(2n)`) have `F=0` yet
  are far from geometric.
- **R6 correction.** Dissociativity is *not* the obstacle. HGJ representations
  always number `2^(n/2)`, and their modular residues are spread (~0.6) even for
  dissociated instances, so the filter applies. See `PHASE1.md`.
- **Corrected target.** Drop the `(A)/(B)/(C)` split; focus on **pseudo-solution
  accounting** (`L²/M`) and on making the balanced `C={0,1}` sub-solver run in
  `O(L)` — the gap to `0.29n`.
- **R7 result.** Pseudo-solution load is `T=1, P=0` for dissociated, geometric,
  and near-geometric instances, and large only for easy collision-heavy
  families. The barrier is the sub-solver cost, confirmed not the instance
  class. Next: attempt the `O(L)` sub-solver.
- **R8 result (analytical).** Balanced-MITM sub-solver floor is `0.4056n`;
  `{-1,0,1}` does not lower it (minimised at `alpha = 0`), and `{0,1}` admits
  only 2 parts. Merge/search term is `0.3113n`. The gap is precisely the
  sub-solver; see `PHASE1.md` and `sub_solver.md`.
- **R9 result.** Birthday/subsampling cannot beat the floor: exactly ~1
  decomposition survives the residue filter and hides among `L` candidates, so
  sampling succeeds with probability `s/L`. Reaching `0.3113n` needs a
  sub-solver outside the balanced/birthday family, or a conditional lower
  bound.
- **R10 result.** Algebraic counting (DP/FFT) costs `2^(0.5n)`, above the
  floor; coarse DP + rejection sampling returns a random element, not the
  planted one.
- **R11 result (correction).** Reproduced the primary-source complexity models:
  HGJ 2-part ideal `0.3113`, HGJ simple `0.337`, BCJ minimised `0.291`. This
  shows the R8 balanced-sub-solver model was **wrong** — the real algorithm is a
  4-way decomposition with the unbalanced Schroeppel-Shamir sub-solver, and it
  already reaches `0.291n` (average case). The obstacle is the
  **average-case → worst-case gap**, not a sub-solver. See `PHASE1.md` and
  `representation_exponents.md`.
- **R12 result.** The worst-case open cases `{0,1}`, `{±1}`, `{±2}` are exactly
  the coefficient sets with no nontrivial sumset factorisation, so
  Randolph-Węgrzycki's coefficient shifting has nothing to exploit. A `{0,1}`
  solution needs a different worst-case mechanism. See `coefficient_shifting.md`.

## Phase 2 — the structured 3SUM route

1. Formalize the three-block reduction: subset sum becomes 3SUM over three
   subset-sum sets of size `N = 2^(n/3)` (item 6).
2. Prove or refute a subquadratic algorithm for 3SUM on these structured sets:
   use sumset-size bounds, bounded-integer convolution, or Kneser's theorem.
   Generic 3SUM is conjectured quadratic, so any success must exploit structure.
3. Combine with Phase 1: a dichotomy gives either AP structure (convolve) or
   many representations (dissect).

## Phase 3 — one worst-case algorithm across regimes

Branch on input parameters and aim for `2^(n/3)` in all branches:
- dense / `t ≤ 2^(n/3)`: already `O*(2^(n/3))` (items 7, 14);
- sparse large-value / density `~1`: today `2^(n/2)`; this is where Phases 1–2
  must land;
- structured (superincreasing, powers of two): already polynomial.

## Phase 4 — barriers, validation, formalization

- Stress candidate algorithms on adversarial families (superincreasing,
  density-1 random, low additive energy, arithmetic progressions).
- Try to prove or refute the formal Meet-in-the-Middle conjecture; Either-Or
  Subset Sum (item 17) is the best positive evidence.
- Formalize the reductions (three-block split, representation compatibility) in
  Lean where feasible, extending `lean/SubsetSum.lean`.

## Ordered next tasks

1. HGJ/BCJ dissection implementation + reproducible `2^(0.29n)` curve.
2. PESS `2^(n/3)` implementation and a written account of its promise.
3. Mixing harness for small `C`; search for synthetic representations.
4. Formal 3-block → 3SUM reduction with complexity bookkeeping.
5. Literature watch and re-verification: Randolph-Węgrzycki (STOC 2026),
   Jin-Williams-Zhang (ESA 2025), Chukhin et al. (2026).

## Risks

- The MITM conjecture may be true: then no `2^(1/2−ε)n` worst-case algorithm
  exists. It is unproven, and Either-Or Subset Sum weakens the naive version.
- The hard core may need genuinely new additive combinatorics, not a transfer
  of existing techniques.

## Success criteria

- **Weak (publishable):** any worst-case exponent strictly below `1/2` for
  vanilla subset sum, or a proof/refutation of the MITM conjecture.
- **Strong (the target):** a deterministic worst-case `O*(2^(n/3))` algorithm
  for `{0,1}` subset sum with a valid witness and accounted arithmetic model.
