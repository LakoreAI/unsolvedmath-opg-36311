# The high-energy regime: forced relations and a conditional dichotomy

Status (2026-10-06). Pen-and-paper, not Lean-checked. One rigorous counting lemma, one
conditional algorithmic consequence, and a precise statement of what blocks it. Read after
`LIFT.md`. Numbers: `docs/analysis/2026-10-06/subset-sum/relation_length.md`,
`high_energy.md`.

## 1. Setting

`x` is a weight-`n/2` solution with support `S`, `m = |S| = n/2`,
`T = Sigma_{m/2}(S)`, `D = |T|`. `LIFT.md` solves the instance in
`poly(n) (2^{0.4057n} + C(n,n/4)/D)`, which beats `2^{n/2}` iff `D > 2^{0.311n}`. The
remaining regime is `D <= 2^{delta n}` with `delta <= 0.311`.

## 2. Lemma (forced relation, rigorous)

Call `S` *k-dissociated* if distinct subsets of `S` of the same size `j <= k` have distinct
sums.

**Lemma.** If `S` is `k`-dissociated then `D >= C(m/2 + k, k)`.

*Proof.* Fix `R subset S`, `|R| = m/2 - k`, and let `U = S \ R`, `|U| = m/2 + k`. The
`k`-subsets `K` of `U` have pairwise distinct sums (k-dissociation), so the sums
`sigma(R) + sigma(K)` are `C(m/2+k, k)` distinct elements of `T`. `[]`

**Corollary.** If `D < C(m/2 + k, k)` then `S` contains disjoint `P, Q` with
`|P| = |Q| <= k` and `sigma(P) = sigma(Q)` (two distinct equal-size subsets with equal sum;
remove their intersection). For `D = 2^{delta n}` the threshold `k(delta)` is in
`relation_length.md`; at `delta = 0.311`, `k = 0.105 n` (`|P u Q| <= 0.21 n`).

Tightness: a "box" support (`m` vectors in `[0,L)^d`, random generators) is
`k`-dissociated for `k ~ d log(kL)/log(m/k)` yet has `D <= (mL/2)^d`, matching the lemma up to
constants, so `k = Theta(m)` relations are the right scale in this regime (not `O(1)`, not
`o(m)`). Constant-length relations (the additive quadruples of `high_energy.py`) are *not*
forced; the experiment finds them only for small rank.

## 3. Conditional dichotomy

Suppose a relation `(P, Q)` found among the inputs is known to satisfy `P u Q subset S`
(solution elements). Then those `|P u Q| <= 2k` elements are in the solution, and the
residual instance has `n - 2k` elements and target `t - sigma(P u Q)`.

* Finding an equal-sum pair of `k`-subsets by sorting costs `~ C(n, k)`.
* Solving the residual by MITM costs `2^{(n-2k)/2}`.

Combined exponent `max(h2(k/n), (1 - 2k/n)/2)` (columns of `relation_length.md`):
`0.4922` at `delta = 0.05` falling to `0.395-0.485` around `delta = 0.311`, and below
`0.40` for `delta >= 0.35`. Together with `LIFT.md` this is `< 0.5` for every `delta`
**conditional on the relation lying in `S`**. The best point is at `delta ~ 0.3-0.4`, the
worst (`0.49`) at tiny `D`; for `D = n^{O(1)}` small-doubling/DP tools apply instead.

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
