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
- [x] 0.3. ESS/PESS baselines (`src/equal_subset_sum.py` + tests): signed
  meet-in-the-middle for ESS at `O*(3^(n/2))`, and binary-search/MITM for
  PESS at `O*(2^(n/2))`.
- [x] 0.4. Port the `O*(2^(n/3))` PESS algorithm and its structural
  `F = sum_t max(0, count(t)-1)` and subsampling/mod-p machinery. A
  modular-bucket counting/sampling primitive and a large-slack collision
  round (`bucket_collision`, Las Vegas `randomized_pigeonhole_equal_subset_sum`
  with exact fallback) are implemented. The close-pair reduction `W_{X,Y}`
  with witness lifting (`close_pair_equal_subset_sum`) is implemented and
  proven complete for nonnegative weights, using a 2^(n-k) reference
  enumeration of close pairs. The Jin-Wu `O*(2^(0.4n))` algorithm
  (arXiv:2403.19117) is implemented as `jin_wu_pigeonhole_equal_subset_sum`:
  exact structured counting (Lemma 7) plus Lemma 5 subsampling, dispatched by
  the measured slack `Delta*` with `d >= Delta*` (Lemma 6, tested by brute
  force). Near-geometric instances: cost `~2^9.6` vs MITM `~2^17.6` at
  `n=24`; on random instances poly(n) overhead dominates at `n <= 24`.
   Close-pair search (R16a): `close_pairs_structured` in `src/equal_subset_sum.py`
   is a complete branch-and-bound that returns the same pairs as the `2^(n-k)`
   reference but visits polynomially many nodes on nearly geometric inputs
   (`pess_structure.md`: `visit e ~ 0.3` and falling in `n`, vs `~1.0` dense).
   Full `O*(2^(n/3))` reduction (R16b, Jin-Williams-Zhang ESA 2025):
   `jwz_disjoint_close_pairs` builds the poly(n)-size disjoint close-pair set
   `D` of Lemma 9 from the geometric proxy (exhaustive-tested vs brute force;
   `jwz_close_pairs.md`: `|D| <= 200 n^5` while the naive suffix enumeration is
   `3^(n-k)`), and `pess_jwz_pigeonhole_equal_subset_sum` applies the prefix and
   Lemma 10 reductions to `W_{X,Y} = (w_1..w_k, w(X)-w(Y))` with witness
   lifting. The poly(n) constants are large, so this reproduces the asymptotics
   rather than a practical speedup at small `n`.
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
- **R12 result.** The worst-case open cases `{0,1}`, `{±1}`, `[±2]` have no
  sumset factorisation with a repeated representation (proved via
  `|A+B| >= |A|+|B|-1`; see the representation note), so Randolph-Węgrzycki's
  coefficient shifting has nothing to exploit. A `{0,1}` solution needs a
  different worst-case mechanism. See `coefficient_shifting.md`.
- **R19 result.** Either-or subset sum rules out all-distinct inputs as hard, so
  hard inputs have *some* collisions. Do collisions help? Sweep of number size
  `2^(beta*n)`, n = 16, 20: at `beta = 1` about 11% of subsets repeat a sum,
  yet meet-in-the-middle halves have no repeats (work ratio 0.99 even for the
  best of 32 splits) and birthday sampling needs `2^(0.55n)`. Collisions are
  *global* (they need many items), so neither half-deduplication nor sampling
  exploits them. Sampling beats `2^(n/2)` only for `beta < ~0.85`. The hard band
  is roughly `0.9 <= beta <= 1.25`: collisions exist but are too sparse and too
  spread out. Next: a collision-finding method whose cost depends on global,
  not per-half, structure. See `collision_mitm.md`.
- **R20 result.** Jin-Wu residue-class sampling (random prime `p`, one class
  `w(S) = r mod p`) is exactly such a method. Predicted cost
  `(2^n/sqrt(C2))^(2/3)`, two thirds of the birthday exponent; measured cost
  matches within ~0.02 for `beta <= 1.1` (n = 16, 20, 24). At density 1, n = 24:
  `2^(0.42n)` vs birthday `2^(0.55n)` and meet-in-the-middle `2^(0.5n)`; still
  below `2^(n/2)` at `beta = 1.25` for n = 24. So in the hard band, *equal-sum
  pairs* are cheap to find. This finds collisions, not subset-sum solutions.
  Open step: turn a supply of cheap collisions `c` (with `c.a = 0`) into
  progress on subset sum, e.g. by using them to generate many solutions from
  one, or to reduce the instance. See `bucket_collisions.md`.
- **R21 result (negative, closes the collision route).** Collisions found by
  the R20 sampler have support about `n/2` (0.50-0.56 of entries nonzero), so
  each is compatible with a fixed solution with probability about `2^(1-n/2)`.
  Over n = 16, 20, 24 and `beta` in 0.9-1.1, inputs averaged at most 1
  compatible collision out of up to 128 found, and kept 1-3 solutions. Cheap
  collisions do not multiply solutions. A useful collision would need support
  `o(n)`, and sampling does not find those. See `collision_amplification.md`.

## Phase 2 — the structured 3SUM route

1. Formalize the three-block reduction: subset sum becomes 3SUM over three
   subset-sum sets of size `N = 2^(n/3)` (item 6).
2. Find a 3SUM algorithm on these structured sets that runs in
   `N^(3/2 - eps)` time (this beats `2^(n/2)`), and ideally `N^(1 + o(1))`
   (this reaches `2^(n/3)`). A merely subquadratic `N^(2 - eps)` algorithm is
   *not* enough: it costs `2^((2/3)(1 - eps/2) n)`, worse than meet-in-the-middle
   unless `eps > 1/2`. Generic 3SUM is conjectured to need `N^2`, so the
   structure of subset-sum sets must do almost all of the work.
3. Combine with Phase 1: a dichotomy gives either AP structure (convolve) or
   many representations (dissect).

### Phase 2 status

- **P2.1 result (negative for the pairwise route).** Listing the smallest
  pairwise sumset `|Si + Sj|` and matching the third block beats `2^(n/2)` only
  if `|Si + Sj| <= 2^((1/2 - eps) n)`. Measured exponents (n = 18, 21, 24, best
  of 8 random splits): about `0.66` for `beta >= 0.7`, `0.56-0.58` at
  `beta = 0.5`, and below `0.5` only at `beta = 0.4`, where the dynamic program
  already runs in `2^(0.4n)`. This matches the bound
  `|Si + Sj| <= min(2^(2n/3), (2n/3) 2^(beta n))`. So in the hard band the
  pairwise sumsets have no usable structure, as R19 found for halves. A Phase 2
  algorithm must use cancellation that involves all three blocks at once (for
  example a modular filter applied across the three lists), not the size of any
  pairwise sumset. See `three_block.md`.

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
