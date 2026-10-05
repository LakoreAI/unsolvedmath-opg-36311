# Phase 1 — mixing attack on vanilla `{0,1}` subset sum

Status (2026-10-03): hypotheses framed, probes built, one hypothesis falsified
and refined. No algorithm claim.

## Hypotheses under test

- **H1 (synthetic representations).** Random restrictions / partitions can
  manufacture enough representations of a `{0,1}` solution without changing
  satisfiability, so the balanced-decomposition requirement is not a real
  obstruction.
- **H2 (dichotomy).** Every instance is *either* near-geometric / structured
  (few collaborations) *or* has many representations (dissection applies).
- **H3 (pseudosolution recovery).** Adapt compatibility certificates from
  Randolph–Węgrzycki to `C={0,1}` / `C={±1}`.

## H1 — supported

`scripts/analysis/synthetic_repr.py` (see `synthetic_repr.md`). For a planted
weight-`n/2` solution over 200 random equipartitions:

| n | partitions with a balanced representation | median representations | total |
| ---: | ---: | ---: | ---: |
| 32 | 200/200 | `2^12.11` | `2^16` |
| 48 | 200/200 | `2^19.60` | `2^24` |
| 64 | 200/200 | `2^27.22` | `2^32` |
| 96 | 200/200 | `2^42.68` | `2^48` |

Random partitions always supply a balanced representation and retain
`2^(n/2)/poly(n)` of them. Balancing is a randomization problem, not a
structural one — **H1 holds empirically**.

## H2 — falsified as stated, then refined

`scripts/analysis/dichotomy.py` (see `dichotomy.md`). `F = sum_t max(0,
count(t)-1)` is the PESS collision count; `geo-dist = max_i |a_i - 2^i|`.

| family | log2|S| | log2 F | geo-dist | regime |
| --- | ---: | ---: | ---: | --- |
| geometric `2^i` | `n` | `0` | `0` | structured |
| near-geometric | `~n` | large | moderate | many reps |
| arithmetic `1..n` | `~2 log n` | `~n` | large | many reps |
| density-1 random | `~n` | `~n` | large | many reps |
| **dissociated random** `[1,2^(2n)]` | `n` | `0` | `~2n` | **danger zone** |

The naive dichotomy is **false**: `F = 0` does not imply near-geometric.
Generic *dissociated* instances (all `2^n` subset sums distinct, values up to
`2^(2n)`) have no collisions and are arbitrarily far from geometric. They evade
both branches: no spare representations for dissection, no geometric structure
to collapse. **This is exactly the hard worst-case regime** where
meet-in-the-middle's `2^(n/2)` is the best known bound.

## R6 — the danger zone is not the obstacle (correction)

The initial reading (dissociated `F=0` = hard core) is **wrong**. HGJ
representations are decompositions of *one* solution (`x = y + z`); there are
always `2^(n/2)` of them, whether or not different solutions collide. R6
(`scripts/analysis/modular_structure.py`, see `modular_structure.md`) measures
the modular residues `a·y mod M` of those representations, with the modulus set
near their count `C(n/2, n/4)` as in HGJ:

| family | coverage = distinct / `C(n/2,n/4)` |
| --- | ---: |
| dissociated (`F=0`) | ~0.62 |
| density-1 random | ~0.62-0.72 |
| near-geometric | ~0.38-0.64 |
| geometric | ~0.13-0.65 |
| arithmetic | ~0.01-0.40 |
| equal-weights (concentrated) | ~0 |

The generic *and* dissociated families are **spread** at the random-birthday
level (~0.6), so the representation filter applies to them; the concentrated
families are special and easy. **No family is both hard and poorly covered**, so
dissociativity is not the obstacle. This agrees with the literature, where the
open cases are `C={0,1}` and `C={±1}` — a sub-solver-structure problem, not a
new instance class.

## Corrected target

1. The `(A)/(B)/(C)` split is the wrong axis. Replace it with **pseudo-solution
   accounting**: for worst-case inputs, bound the modular candidate count
   `L²/M` against the true representation count.
2. The decisive question: can the balanced sub-solver for `C={0,1}` run in
   `O(L)`? That is the step HGJ calls "difficult to achieve" and BCJ only
   partially realizes.
3. Lower bounds: does `2^(n/3)` for `{0,1}` imply progress on modular `k`-sum /
   orthogonal vectors? If not, no known barrier blocks it.

## R7 — pseudo-solution load is concentrated in the easy instances

`scripts/analysis/pseudo_solutions.py` (see `pseudo_solutions.md`). `T` =
target representations of cardinality `n/2` (true solutions); `P` = target
representations of cardinality `< n/2`, which are exactly the overlapping
(mismatched) pairs an HGJ merge must filter out.

| family | T | P | F |
| --- | ---: | ---: | ---: |
| dissociated | 1 | 0 | 0 |
| geometric | 1 | 0 | 0 |
| near-geometric | 1 | 0 | large |
| density-1 random | 1 | ~0 | large |
| arithmetic | large | large | large |
| dense random | large | large | large |

`T = 1` and `P = 0` for dissociated, geometric, and near-geometric instances at
every `n` up to 20. Pseudo-solution load appears only in the collision-heavy
families, which are easy. So the HGJ merge is **cleanest on the hard-looking
instances**, and the pseudo-solution blow-up feared in the BCJ analysis is not
what blocks `2^(n/3)`. Combined with R6, this pins the barrier squarely on the
**balanced sub-solver cost** (`C(n/2,n/8)` instead of `O(L)`), not on any
adversarial instance class.

## R8 — the balanced sub-solver is the bottleneck (model superseded by R11)

> **Correction (R11).** The model below assumed HGJ uses a 2-part balanced
> meet-in-the-middle sub-solver. That is **not** the HGJ algorithm: HGJ uses a
> 4-way decomposition with weight-`n/8` parts solved by the *unbalanced*
> Schroeppel-Shamir algorithm, and BCJ adds three `{-1,0,1}` levels. R11,
> working from the primary sources, reproduces the real exponents
> (`0.337` HGJ, `0.291` BCJ), so the "`0.4056n` floor" is an artifact of the
> wrong model, not a property of the technique. The sections R8-R10 are kept
> for the record; see R11 for the corrected picture.

`scripts/analysis/sub_solver.py` (see `sub_solver.md`). Represent the base-2
exponents per `n` for the representation technique with a balanced
meet-in-the-middle sub-solver, parameterised by the minus-one fraction `alpha`
of the BCJ `{-1,0,1}` representation (`alpha = 0` is the `{0,1}` HGJ case).
`E_sub` is the sub-enumeration, `L` the solutions per side, `total =
max(E_sub, merge)`.

| alpha | E_sub | L | total |
| ---: | ---: | ---: | ---: |
| 0.000 | 0.4056 | 0.3113 | 0.4056 |
| 0.025 | 0.4996 | 0.1831 | 0.4996 |
| 0.050 | 0.5529 | 0.1450 | 0.5529 |
| 0.075 | 0.6247 | 0.1588 | 0.6247 |
| 0.125 | 0.7028 | 0.1556 | 0.7028 |

Findings:

- `alpha = 0` (`{0,1}` HGJ): `E_sub = 0.4056`, merge/search `L = 0.3113`,
  `total = 0.4056`. This matches the measured HGJ exponent `~0.385` at finite
  `n`.
- The total is **minimised at `alpha = 0`**: adding `{-1,0,1}` makes the
  candidate space (and thus `E_sub`) larger, not smaller, for this sub-solver.
  So the naive sub-solver cannot exploit BCJ's extra representations.
- Multi-part `{0,1}`: only **2 parts are feasible**. For `2^t` equal parts the
  representation count is `2^(t n/2)`, while the candidate space is
  `C(n, n/2^(t+1))`; `C(n,w) >= 2^(t n/2)` holds only for `t = 1`
  (`0.8113 >= 0.5`); `t = 2` needs `0.5436 >= 1` and fails.
- Therefore the balanced-MITM sub-solver floor is `0.4056n` and the
  merge/search term is `0.3113n`. The gap `0.4056 -> 0.3113` is *exactly* the
  sub-solver improvement needed to reach the ideal `0.3113n`; the published
  `0.337n` (HGJ, May-Meurer corrected) and `0.291n` (BCJ) require sub-solvers
  better than balanced meet-in-the-middle, which is not specified in the
  sections available.

**R8 target, restated precisely:** enumerate the `L = 2^(0.3113n)` weight-`n/4`
subsets with `a·y ≡ R (mod 2^(n/2))` in time `o(2^(0.4056n))`. A birthday /
subsampling idea that enumerates only `~2^(n/4)` candidates per side can find
residue matches, but must resolve exactness and disjointness; whether that
closes the gap is open.

## R9 — birthday/subsampling does not beat the sub-solver floor

`scripts/analysis/birthday_sub_solver.py` (see `birthday_sub_solver.md`).
For a planted balanced solution, the sub-solver wants the *specific*
decomposition `(y, z)` with `y + z = x`, not just any residue match. Measured
(with `M ~ D`, the decomposition count, so the expected number of surviving
decompositions is 1):

| n | D | P(survival >= 1) | max survivors | residue class `\|Y\|` |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 30 | 0.667 | 3 | 27 |
| 20 | 90 | 0.611 | 4 | 65 |
| 24 | 350 | 0.623 | 4 | 138 |
| 28 | 1120 | 0.653 | 5 | 325 |

The survival count is ~`Poisson(1)` (`P(>=1) ~ 0.63`), exactly as HGJ designs.
But that one surviving decomposition hides in a residue class of size `|Y| ~
C(n/2,n/8)^2 / M = L`. A birthday sampler that examines `s` candidates per side
finds the needle with probability `~ (s/|Y|)`, so constant success needs
`s ~ |Y| = L` — the full balanced enumeration. The birthday trick finds *a*
residue match cheaply but not the one whose complement closes the exact target.

**Conclusion (R8 + R9).** The `0.4056n` floor stands for the family of
balanced/birthday sub-solvers. Reaching the ideal `0.3113n` — and hence the
published `0.337n` / `0.291n` — requires a sub-solver outside this family: a
new algebraic idea, a structured/adversarial assumption, or a conditional lower
bound showing it is impossible. This is the concrete open problem the research
has isolated.

## R10 — algebraic methods hit the counting-vs-finding gap

`scripts/analysis/algebraic_sub_solver.py` (see `algebraic_sub_solver.md`).
Base-2 exponents per `n` to find a weight-`n/4` subset with
`a·y = R (mod 2^(n/2))`:

| method | exponent | what it returns |
| --- | ---: | --- |
| balanced meet-in-the-middle (R8) | 0.4056 | all of `Y` |
| full-residue cardinality DP | 0.5000 | counting, not finding |
| FFT / group-algebra product | 0.5000 | counting, not finding |
| coarse DP + rejection sample | 0.2500 | a random element, not the planted one |
| find planted element (uniform) | 0.5000 | needs the full distribution |

Counting the residue class is cheap, but even DP/FFT over the full residue
space costs `2^(0.5n)` — already above the balanced-MITM floor. A coarse DP plus
rejection sampling returns a *random* element in `0.25n`, but the algorithm
needs the planted element (the unique surviving decomposition, R9), and
sampling uniformly from the residue class requires the full `2^(n/2)`
distribution. This **counting-vs-finding gap** blocks the algebraic route: all
methods either exceed the floor or return the wrong element.

## R11 — reproduced the HGJ and BCJ exponents (corrects R8)

`scripts/analysis/representation_exponents.py` →
`representation_exponents.md`. Implemented the complexity models from the
primary sources (HGJ ePrint 2010/189 §4; BCJ ePrint 2011/474 §3.3) and
minimised them numerically:

| quantity | reproduced | published |
| --- | ---: | ---: |
| HGJ 2-part ideal `D(1/2)` | 0.3113 | 0.3113 |
| HGJ simple algorithm (best `β`) | 0.3372 | 0.337 (May-Meurer) |
| BCJ `α=β=γ=0` (recovers HGJ) | 0.3371 | 0.337 |
| BCJ minimised | 0.2917 | 0.291 (α=0.0267, β=0.0168, γ=0.0029) |

The BCJ optimum reproduced at `α=0.028, β=0.018, γ=0.004` (grid resolution).

**This corrects R8.** The real HGJ structure is a **4-way decomposition** with
weight-`n/8` parts, each sub-knapsack solved by the **unbalanced
Schroeppel-Shamir** algorithm; BCJ adds three `{-1,0,1}` levels. There is no
`0.4056n` sub-solver barrier — the technique already reaches `0.291n`.

## R12 — the open cases are exactly the sets with no coefficient shifting

`scripts/analysis/coefficient_shifting.py` (see `coefficient_shifting.md`),
based on Randolph-Węgrzycki (arXiv:2511.10823). Their worst-case tool,
*coefficient shifting*, writes `C = C1 + C2` so that coefficients acquire
multiple representations. Searching factorisations `C1, C2 ⊆ [-3,3]`:

| C | nontrivial factorisations | best max reps |
| --- | ---: | ---: |
| Subset Sum `{0,1}` | 0 | 1 |
| Partition `{±1}` | 0 | 1 |
| Balancing `{±2}` | 0 | 1 |
| Equal Subset Sum `{-1,0,1}` | 6 | 2 |
| Balancing `{±3}` | 4 | 2 |
| Balancing `{-2..2}` | 39 | 3 |

The three open cases RW names — `{0,1}`, `{±1}`, `{±2}` — are **exactly** the
coefficient sets with *no* nontrivial sumset factorisation (every coefficient
keeps a single representation). Sets with a `0` coefficient (`{-1,0,1}`) or a
factorisation (`{±3}` via `{0,1}+{-3,-2,1,2}`) get the surplus that coefficient
shifting needs. This is a clean, independently reproduced characterisation of
the frontier: **the obstacle to `{0,1}` is that it admits neither a 0
coefficient nor a nontrivial factorisation, so the worst-case representation
technique has no surplus to exploit.**

## Corrected bottom line

The published `0.291n` / `0.337n` bounds are **average-case** for random hard
knapsacks; they rely on heuristic modular-distribution corollaries that can
fail on adversarial instances. So the obstacle to `O*(2^(n/3))` is **not** a
sub-solver inside the representation technique — it is the
**average-case → worst-case gap**:

> Make the representation/dissection machinery worst-case, or prove a
> conditional lower bound. This is exactly the frontier of
> Randolph-Węgrzycki (2025), which is worst-case for most coefficient sets
> `C` but **not** for `C={0,1}` (vanilla) or `C={±1}` (Partition).

R12 sharpens *why*: those sets (and `{±2}`) are precisely the ones with no
nontrivial sumset factorisation, so the worst-case technique's coefficient
shifting has nothing to work with. A `{0,1}` algorithm must therefore find a
**different** worst-case mechanism (or a new representation not based on
coefficient shifting), or show none exists.

The R6-R10 probes still stand as observations about the *weak balanced* variant
and about the structural quantities (collisions, pseudo-solutions, modular
coverage), but they do not identify the barrier; R11 does.

## Concrete next steps

1. **[done, R6]** Dissociativity is not the barrier.
2. **[done, R7]** Pseudo-solution load is not the barrier.
3. **[done, R8, corrected by R11]** Balanced-sub-solver model was wrong.
4. **[done, R9]** Birthday/subsampling cannot beat the (wrong-model) floor.
5. **[done, R10]** Algebraic counting hits the counting-vs-finding gap.
6. **[done, R11]** Reproduced HGJ `0.337` and BCJ `0.291` from primary sources;
   identified the real obstacle as average-case vs worst-case.
7. **[done, R12]** The open cases `{0,1}`, `{±1}`, `{±2}` are exactly the
   coefficient sets with no nontrivial sumset factorisation, so coefficient
   shifting cannot be applied.
8. **Next (R13).** Look for a worst-case mechanism for `{0,1}` that is not
   coefficient shifting: e.g. a canonical sumset / compatibility certificate
   specific to `{0,1}`, or a proof that none exists. The barrier statement in
   `TRANSFER.md` shows the PESS structural lemma needs the pigeonhole promise
   and is false without it, so R13 must supply a promise-forcing reduction, a
   promise-free structure dichotomy, or an all-three-block algorithm.
9. **H3**: pseudosolution recovery / compatibility certificates for `C={0,1}`.
2. **Pseudo-solution accounting (new Phase 1 core).** Instrument the HGJ search
   to count modular candidates `L²/M` versus true representations for
   adversarial families, and find families where the candidate ratio explodes.
   This is the quantity the May–Meurer correction shows governs the exponent.
3. **Sub-solver.** Attempt to solve the balanced weight-`n/4` modular
   sub-knapsack for `C={0,1}` in `O(L)` rather than `C(n/2,n/8)` — the step to
   `0.3113n` and the gap to `0.29n`.
4. **H3**: pseudosolution recovery / compatibility certificates for `C={0,1}`.
5. Extend the probes with more adversarial families and larger `n` (current
   evidence is small-`n` and family-limited).

## Artifacts

- `src/additive.py`, `tests/test_additive.py` — probes (`|S|`, `F`, additive
  energy, geometric distance, longest AP); all unit-tested.
- `scripts/analysis/dichotomy.py` → `dichotomy.{csv,md}`.
- `scripts/analysis/synthetic_repr.py` → `synthetic_repr.md`.
- `scripts/analysis/mixing_harness.py` → `mixing.md` (Phase 0).
