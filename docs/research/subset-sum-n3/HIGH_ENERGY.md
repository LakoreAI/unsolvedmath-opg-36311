# The high-energy regime: forced relations and a conditional dichotomy

Status (2026-10-06). Pen-and-paper, not Lean-checked. One rigorous counting lemma, one
conditional algorithmic consequence, and a precise statement of what blocks it. Read after
`LIFT.md`. Numbers: `docs/analysis/2026-10-06/subset-sum/relation_length.md`,
`high_energy.md`.

## 1. Setting

`x` is a weight-`n/2` solution with support `S`, `m = |S| = n/2`, split into halves
`S1, S2` of size `m/2` (the split induced by the balanced sub-solver) and
`T(S1,S2) = sigma(y1) + sigma(y2)` over `|y_i| = m/4`, `D* = min |T(S1,S2)|`. `LIFT.md`
solves the instance in `poly(n) (2^{0.4057n} + (A + N_t)/D*)`, which beats `2^{n/2}` iff
`D* > 2^{0.311n}` (assuming the pair count `N_t <= A`). The remaining regime is
`D* <= 2^{delta n}`, `delta <= 0.311`, or `N_t` large (large bins, AKKN).

## 2. Lemma (forced relation, rigorous)

Call `S` *k-dissociated* if distinct subsets of `S` of the same size `j <= k` have distinct
sums.

**Lemma.** If `S` is `k`-dissociated (`k = 2j`) then `D* >= C(m/4 + j, j)^2`.

*Proof.* Fix the partition. Choose `R_i subset S_i` with `|R_i| = m/4 - j` and let
`U_i = S_i \ R_i`, `|U_i| = m/4 + j`. For `j`-subsets `K_i subset U_i` the sum
`sigma(R_1 u R_2) + sigma(K_1) + sigma(K_2)` lies in `T(S1,S2)`, and the pairs `(K_1,K_2)`
give distinct values because `K_1 u K_2` ranges over distinct `2j`-subsets of `S` with a fixed
disjoint complement. There are `C(m/4+j, j)^2` pairs. `[]`

**Corollary.** If `D* < C(m/4 + j, j)^2` then `S` contains disjoint `P, Q` with
`|P| = |Q| <= k = 2j` and `sigma(P) = sigma(Q)`. For `D* = 2^{delta n}` the threshold `k(delta)`
is in `relation_length.md`; at `delta = 0.311`, `k = 0.105 n` (`|P u Q| <= 0.21 n`).

Tightness is NOT established, and the corrected picture is this (2026-10-06, replaces two
earlier claims). A box support with random coordinates (`[0,L)^d`, random generators) has
`Theta(n)`-length relations, not `d+1`: relations here need ternary coefficients, and a
birthday count puts the shortest at `k/n ~ h2^{-1}(delta)/2` (`0.029` at `delta = 0.32`);
Gilbert-Varshamov-type avoidance gives `0.041`; the lemma's `0.11` would need near-perfect `B_k`
sets, for which no construction is known. See `adversary_model.md`.

## 3. Conditional dichotomy

Suppose a relation `(P, Q)` found among the inputs is known to satisfy `P u Q subset S`
(solution elements). Then those `|P u Q| <= 2k` elements are in the solution, and the
residual instance has `n - 2k` elements and target `t - sigma(P u Q)`.

* Finding an equal-sum pair of `k`-subsets by sorting costs `~ C(n, k)`.
* Solving the residual by MITM costs `2^{(n-2k)/2}`.

Combined exponent `max(h2(k/n), (1 - 2k/n)/2)` (columns of `relation_length.md`):
`0.492` at `delta = 0.05`, `0.448` at `0.20`, `0.466` at `0.30`, `0.485` at the crossover
`delta = 0.311`. Above the crossover the finding cost exceeds `0.5` (`0.554` at `0.35`) and
`LIFT.md` takes over (`0.461` at `0.35`, `0.4057` from `0.405`). So, **conditional on the
relation lying in `S`**, the best of the two is `<= 0.492 < 0.5` for every `delta`; the worst
cases are tiny `D` (where small-doubling/DP tools apply instead) and the crossover.

## 4. What blocks it (the real open step)

Nothing guarantees the relation found lies in `S`. Decoys can create their own relations; the
experiment only shows that *random* decoys do not (`n = 24, 32`). The algorithm needs one of:

1. **Few relations overall.** If the number `N_c` of equal-sum disjoint `k`-subset pairs among
   *all* `n` inputs is `<= 2^{epsilon n}`, branch on each (`P u Q` in `x` or not): time
   `N_c * 2^{(n-2k)/2}`. Needs `N_c` small enough that the product stays below `2^{n/2}`.
2. **Many relations overall** is itself structure: it is the Austrin-Kaski-Koivisto-Nederlof
   large-bin regime (`beta` = max bin size of subsets of `A`), solvable below `2^{n/2}` for
   `beta >= 2^{0.661n}`, but the *intermediate* `beta` is exactly the hard band left open.
   Quantifying `N_c` against `beta` for `k`-subsets with `k = Theta(n)` is the next lemma.

So the high-energy regime reduces to a **two-sided counting question about collisions among
`Theta(n)`-subsets of the whole input**: too few -> branch; too many -> AKKN-type structure.
Neither side is proved here; the rigorous content is Section 2 and the exponents in
Section 3.

## 5. Literature (checked 2026-10-06, alphaXiv)

* Randolph-Wegrzycki, arXiv 2407.18228: small doubling `C = |A+A|/|A|` constant -> `n^{O_C(1)}`;
  our support has polynomial doubling, so not directly applicable.
* Chen-Hu-Mao-Zhang, arXiv 2607.10343 (dense subset sum in constant dimension `d`): structure
  of `S(A)` in a box, lattice/Kneser tools; the tools may extend, the theorems need constant `d`.
* No newer worst-case `{0,1}` result below `2^{n/2}` was found; Salas (2503.20162) remains
  unsound (`NEXT.md`).

## 6. Toy-size caveat

A support that is Sidon-like (no 4-term relation) and has `D <= 2^{0.311n}` needs
`(2L)^d >= m^4` and `d log(mL/2) <= 0.622 m`, i.e. `m` in the low hundreds (`n` in the
hundreds). Direct experiments at `n <= 40` can only probe the small-rank corner
(`high_energy.md`); the conclusions above are asymptotic counting.

## 7. A compressible core gives an exact algorithm (2026-10-06, experiments)

Not a worst-case result. For any set `C` of inputs, a meet-in-the-middle whose one side is
`Sigma(C) + Sigma(R1)` runs in `~ sqrt(2^{|R|} |Sigma(C)|)` (`src/compress_mitm.py`), exact
whatever `C` is. `C` is found as the union of elements in equal-sum pairs of small subsets
(`relation_core.md`): at toy size every such relation lay inside the hidden structured support
for `s` below the noise threshold, including supports on which LLL failed
(`relation_detect.md`). Measured (`compress_eval.md`, exact in all 22 rows): states shrink
`7-25x` for strong structure (`n = 32`, rank 3-4) and the gain vanishes at rank 8 and on random
inputs, where `|Sigma(C)|` is almost `2^{|C|}`. Savings need `|Sigma(C)| << 2^{|C|/2}`,
which toy sizes barely reach. This is the AKKN/small-doubling few-sums regime applied to a
sub-collection, with an automatic detector; instances with no compressible sub-collection are
untouched, and a decoy-adversarial input can make the detector include non-structured elements
(slower, never wrong).

### Beyond toy size (`compress_scale.md`)

Solved with verified witnesses at `n = 56, 76, 80` (rank-3 structured part of 40-60 elements plus
16-20 random decoys): `1.5e5 .. 8.3e5` states against `2^28 .. 2^40` for plain MITM
(`1.7e3 .. 1.3e6`-fold). Detection at `n = 224` (200 distinct weight-3 vectors in `Z^12` plus 24
decoys): the `s = 2` search (about 25 000 subsets) returns exactly the 200 structured elements, no
decoys; predicted cost `2^46` versus `2^112` (box-volume estimate, not run). Scope: these inputs
have a small-doubling structured part and constant-times-`r` doubling overall, the regime of the
small-doubling algorithms; they show a practical exact solver and detector, not progress on the
hard band where no sub-collection is compressible.

### Adversary model (`adversary_model.md`)

Under random decoys and `|Sigma(S)| <= 2^{delta n}` (both assumptions, not proved), the best of
LIFT and detect-then-compress has worst-case exponent `0.431` (birthday and GV relation models,
at `delta = 0.38`) and `0.4913` (the lemma's extremal relation length, at `delta = 0.32`),
always `< 1/2`. A hard family would need an adversarial decoy structure (relations among
decoys), a support with `|Sigma(S)|` much larger than `D*`, or relations near the pigeonhole
extremum.

### Assumption A2 and Conjecture U (`ksum_unimodal.md`)

The model's assumption `|Sigma(S)| <= 2^{delta n}` (all sizes) would follow, up to a factor
`n`, from **Conjecture U**: for every set `X` of `m` integers,
`max_k |Sigma_k(X)| <= poly(m) |Sigma_{m/2}(X)|`. Searches over random, structured and
hill-climbed sets (`m = 8..14`) never found a ratio above `1.032`; the counts are not always
unimodal (structured sets show a dip of 1 at the exact middle) but the middle is always within
a few percent of the maximum. Unproved. If U holds, the only remaining assumption of the model
is A1 (no short relations among non-support elements), plus LIFT's pair-count condition
`N_t <= A`; those two are where a genuine worst-case barrier would have to live.
