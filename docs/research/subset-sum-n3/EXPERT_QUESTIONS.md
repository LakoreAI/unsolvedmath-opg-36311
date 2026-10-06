# Two questions for an additive combinatorialist

This repository attacks worst-case exact subset sum (is there a `2^{(1/2-eps)n}` algorithm for
`{0,1}` coefficients?). The work is AI-assisted and unreviewed; see the warning in the README.
Two self-contained questions now decide whether a heuristic model of ours becomes a theorem for
a whole class of instances. Short answers ("known", "false, here is a counterexample",
"provable by X") would help most.

## Background in three lines

For a set `X` of `m` integers write `Sigma_k(X)` for the set of sums of `k`-element subsets and
`Sigma(X)` for all subset sums. An exact algorithm (`src/compress_mitm.py`) solves subset sum
in about `sqrt(2^{n-|C|} |Sigma(C)|)` steps for any sub-collection `C` of the input, so
*compressible* sub-collections (`|Sigma(C)| << 2^{|C|}`) help. Our theory controls only the
middle-size sums `|Sigma_{m/2}|` of a solution's support, and finding `C` uses short equal-sum
relations.

## Question 1 (Conjecture U)

Is it true that for every set `X` of `m` integers

    max_k |Sigma_k(X)|  <=  poly(m) * |Sigma_{floor(m/2)}(X)| ?

The counts need not be unimodal: `X = {1..h} u {g+1..g+h}` dips at the middle. But in every
search we ran (random, structured, hill-climbed, `m <= 14`; analytic families up to `m = 400`)
the ratio `max_k |Sigma_k| / |Sigma_{m/2}|` stayed below `1.032`, and on the dipping family it
tends to 1 (`0.946` at `m = 12`, `0.998` at `m = 400`). We found no theorem in the literature;
the nearest work concerns the range of sumset sizes (arXiv 2505.07679, 2510.23022) and inverse
theorems for restricted sumsets (arXiv 2505.07415). Evidence:
`docs/analysis/2026-10-06/subset-sum/ksum_unimodal.md`.

## Question 2 (compressible sets with only long relations)

Call `s*(X)` the smallest `s` such that two distinct subsets of `X` of size `<= s` have equal
sums. Pigeonhole forces `s* <= s` as soon as `sum_{j<=s} C(m,j) > |Sigma_{<=s}(X)|`, so if
`|Sigma(X)| <= 2^{cm}` then `s* <~ h2^{-1}(c) m`. Random-like sets collide much earlier, at the
birthday scale `s* ~ h2^{-1}(c/2) m`. **Is there a family of sets with `|Sigma(X)| <= 2^{cm}`
(some `c < 1`) whose `s*` is asymptotically larger than the birthday scale, ideally close to
the pigeonhole scale?** Algebraic `B_h`/MDS constructions give `s*` of order `m / log m`, which
is shorter. Our searches (simulated annealing at `m <= 40`, Vandermonde, Sidon) found nothing
beyond the birthday scale except a Sidon set at `m = 40` (one step above). A positive answer is
exactly the structure that would defeat our detector; a negative answer (with a bound) would
close the long-relation regime of our model. Evidence: `long_relation.md`,
`long_relation_search.md`, and the tradeoff section 8 of `HIGH_ENERGY.md`.

## What is proved, and what is not

- Proved (pen and paper, unreviewed): Theorems 1-2 and the forced-relation lemma in
  `docs/reports/lift/lift.tex`; Lemma T (pigeonhole) in `HIGH_ENERGY.md` section 8.
- Measured only: everything about the detector, the decoy attacks, and the adversary model
  (`adversary_model.md`, worst-case best-of exponent `0.431`-`0.4913` under two assumptions).
- Not claimed: any unconditional worst-case algorithm below `2^{n/2}`.
