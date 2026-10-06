# Approaches to the collision-counting and distinct-sums conjectures

Status (2026-10-06). Summary of the `/research` + `/research-deep` pass over 20 approach
items (`outline.yaml`, `fields.yaml`, `results/*.json`; all 20 validate at 100% field
coverage). Conjectures, from `docs/research/subset-sum-n3/{LIFT.md,HIGH_ENERGY.md}`:

* **C1.** For every `{0,1}` instance either the number `N_c` of equal-sum disjoint pairs of
  `Theta(n)`-subsets is `2^{o(n)}`, or the input is in a large-bin regime that combines with
  AKKN to `2^{(1/2-eps)n}`.
* **C2.** A hard instance cannot have every solution's support with `D* <= 2^{0.311n}`
  (`D*` = distinct balanced half-sums).

**Reliability.** The deep-research agents mostly read abstracts, introductions and theorem
statements, not proofs; 107 field values across the files are marked `[uncertain]`
(inverse Littlewood-Offord 18, Fourier 16, lattice 13 are largely recall-based). Nothing here
is a verified citation until checked against the primary text. Items 2, 6, 8-13 of the original
outline came from model memory and several descriptions were wrong (corrected below).

## 1. Corrections to our own premises
* arXiv 2607.09289 (Yamano-Shibuya, `1.6994^n`) and 2608.08260 (Ye, `(5/3)^n`) are plain
  Equal-Subset-Sum, not PESS. The `2^{n/3}` PESS result is Jin-Williams-Zhang (ESA 2025).
* arXiv 2609.40321 (F_3^n subset sum) is algebraic (degree of regularity, XL), not collision
  counting. 2608.07309 is worst-case quantum k-SUM (`2^{2n/7}`). 2609.14630 is subset-sum
  density realization; 2412.04967 recovers a hidden multiset from its k-subset sums, not
  relation-lattice detection; 2609.26619 is only tangentially related.
* AKKN has no `D*` or `2^{0.311n}` statement; that number is only the average-case HGJ time.
* Salas (2503.20162) again confirmed unsound (the aliasing counterexample of `NEXT.md`).

## 2. What closes, what does not
**Dead ends for C1/C2 as stated:** constructive Freiman / small doubling (bounds doubly
exponential in `C`, useless at polynomial doubling); algorithmic PFR (`F_2^n` only, `2^{O(K)}`
queries); Dias da Silva-Hamidoune `|Sigma_k| >= k(m-k)+1` (polynomial, attained by APs);
CJRS `2^{n/2}/poly` (no collision counting); conditional lower bounds (SETH/k-SUM do not touch
the `2^{n/2}` exponent; that inference is the agent's, not a published theorem).

**Live and exactly on target**
1. **Randolph-Wegrzycki mixing dichotomy (Lemma 5.1/6.1).** The authors say it fails for
   coefficient sets without 0 because `a - a'` can vanish where `c` is nonzero: this is the
   precise `{0,1}` obstruction, and it is a statement about colliding solution pairs, i.e.
   `N_c`-like. Next experiment: measure how often a collision `a.x = a'.x` gives a valid
   disjoint-pair relation versus one blocked by zeros on `supp(c)`.
2. **AKKN collision-energy identity.** `||b||_2^2 = #{(U,V): w(U)=w(V)}`, rewritten as a sum over
   disjoint pairs weighted `2^{n-|U|-|V|}`; `N_c` is a slice of it. The window
   `2^{0.5n} < beta < 2^{0.661n}` is open and `0.661` is not tight.
3. **Fourier / Bohr dual formulation (derived by the agent, unverified).** The number of
   equal-sum pairs `(U,V)` is `4^n * integral prod_i cos^2(pi a_i theta) dtheta`
   (`|1+e^{2 pi i a theta}|^2 = 4cos^2`, checked by us), and `|cos pi x| <= exp(-2||x||^2)`
   turns it into the volume of a Bohr set. A tractable, quantitative handle on `N_c`.
4. **Relation lattice (LLL/BKZ).** `N_c` counts short balanced ternary relations; a rank-`d`
   GAP support gives a gap between successive minima `lambda_{|S|-d}` and `lambda_{|S|-d+1}`.
   Detects exactly the low-rank case of C2 and is computable at `n <= 40`.
5. **Distinct-subset-sums extremal theory.** Dubroff-Fox-Xu and the inverse theorems: sets
   with all `|a_i| < C(n, n/2)` have a relation (existence only; the relation may be short, not
   `Theta(n)`); few subset sums forces rank-1 near-AP structure, which is easy. Classifies the
   extremes, not the exponential-magnitude middle where C2 lives.

## 3. A derived link between C1 and C2 (our elementary observation)
By Cauchy-Schwarz the number of equal-sum ordered pairs of `k`-subsets of the support is at
least `C(m,k)^2 / |Sigma_k(S)|` (the Plunnecke item states the same). Hence **small `D*`
forces many collisions among the support's own half-subsets**: with `D* = 2^{delta n}`
and `Y = 2^{n/2}`, at least `Y^2/D* = 2^{(1-delta)n}` pairs, i.e. bins of size `>= Y/D* =
2^{(1/2 - delta)n}`. Two consequences, to be checked:
* If instead *all* (not only `Theta(n)`) equal-sum disjoint pairs among the inputs are few,
  then `D*` is large and **`LIFT.md` already applies, with no branching**. So the "few
  relations: branch" case of C1 is not needed; what remains of C1 is the converse, large
  collision count implying an algorithm.
* The gap to AKKN is now explicit: `delta = 0.311` gives bins `2^{0.189n}` among half-subsets
  of `S`, while AKKN needs `beta >= 2^{0.661n}` among all subsets. Bridging `0.189n` to
  `0.661n` is the quantitative content of the open step.

## 4. Ranked experiments (all feasible at `n <= 40` with the repo's scripts)
1. RW blocking fraction (item 1 above) on `{0,1}` instances with planted balanced solutions.
2. `N_c` (disjoint equal-sum pairs, sizes `0.1n`-`0.4n`) versus magnitude `2^{cn}`, `c` from
   `0.3` to `1.2`, `n = 24, 28, 32`: where does `N_c` vanish relative to the `2^n/sqrt n`
   distinct-sums threshold?
3. Relation-lattice gap test (LLL then BKZ-20) on rank-`d` GAP supports plus decoys.
4. Bohr-volume Monte Carlo versus `log2 N_c` (does Bohr volume predict `N_c`?).
5. Doubling `|S+S|/|S|` and energy of the half-sum set for rank-`d` GAP versus random.
6. Quantify the slice loss between `N_c` and AKKN's `||b||_2^2` (item 2 above).

## 5. Verdict
No source resolves C1 or C2. The literature gives (a) a precise statement of the `{0,1}`
obstruction (RW), (b) the right quantity to bound (AKKN collision energy / Fourier Bohr
volume), and (c) a computable detector for the low-rank part (relation lattices). Section 3
sharpens the target: bridge bins of size `2^{(1/2-delta)n}` among a support's half-subsets to
the AKKN threshold `2^{0.661n}`, or show it cannot be bridged.
