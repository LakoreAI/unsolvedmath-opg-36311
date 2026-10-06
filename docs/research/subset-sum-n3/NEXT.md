# Research memo: proving (or refuting) the target mixing dichotomy

Status (2026-10-05): literature check + a new candidate lemma + the precise
obstruction. Read with `ATTACK.md` and `MIXING.md`. The measurements referenced
below are in `docs/analysis/2026-10-05/subset-sum/`.

## 0. Alert: an unsound preprint

**Jesus Salas, arXiv:2503.20162, "Beyond Worst-Case Subset Sum: ...",
claims a guaranteed `O*(2^(n/2−ε))` via a "Controlled Aliasing" technique.
Do not cite it: the mechanism is incorrect.** It replaces an element `x1` by
`x0` inside one half's partial sums and keeps one canonical subset per aliased
sum. That merges subsets with *different true sums* and makes the stored sum
wrong. Counterexample: in half `{1,2}`, aliasing `2→1` gives canonical `{1,2}`
the stored sum `2`, but its true sum is `3`, so the merge returns a false
positive and loses the subset `{2}` — completeness is destroyed. The claimed
theorem is deferred to a companion paper and is not established. The conjecture
remains open.

## 1. Rigorous landscape (2024–2026)

- **Worst case** is still `O*(2^(n/2))`; the best is a polynomial saving
  `2^(n/2)/n^0.5023` (Chen–Jin–Randolph–Servedio 2023).
- **Small doubling is easy** (Randolph–Węgrzycki, arXiv:2407.18228): Subset Sum
  is solvable in `n^{O_C(1)}` where `C = |A+A|/|A|`.
- **Worst-case representation** (Randolph–Węgrzycki, STOC 2026) breaks MITM for
  `[−d:d], d>1` and `[±d], d>2`, via a *mixing dichotomy* + *coefficient
  shifting* + *compatibility certificates*; open for `[±1]` (Partition) and
  `[±2]`, i.e. exactly the `{0,1}` case.
- **Density dichotomy** (Austrin–Kaski–Koivisto–Nederlof, STACS 2015/2016):
  parameterized by the maximum bin size `β` (largest number of subsets with the
  same sum), instances with `β ≤ 2^{(0.5−ε)n}` or `β ≥ 2^{0.661n}` are solvable
  below `2^(n/2)`; the hard band is intermediate `β`.
- **Either-Or Subset Sum** `2^(0.461n)` (Randolph); **PESS** `2^(n/3)`;
  **ESS** `1.6994^n`; quantum Subset Sum `2^(2n/7)`.
- **Additive combinatorics**: Balog–Szemerédi–Gowers and Freiman give
  high additive energy ⇒ a large subset in a small GAP (Shao 2013, Shkredov
  2013/2014 give rank `O(1/α)` higher-order versions). This is the engine a
  lifting proof would use to turn poor mixing into structure.

## 2. A new candidate lemma: average collision energy over primes

Let the support `A` have `m = n/2` values, weight `w = n/4`, and let
`Y = C(m,w)` be the number of representations of a balanced solution. For a
prime `p`, let `c_r = #{y : Σy ≡ r (mod p)}` and `E_p = Σ_r c_r²` (the collision
energy). Poor mixing (few hit residues `s_p`) means `E_p ≥ Y²/s_p`.

**Lemma (average energy — elementary).** With `P ≈ Y` and
`π = π(P, 2P) ≈ P/ln P` the number of primes in the window,

    (1/π) Σ_{p∈[P,2P]} E_p  ≤  E_∞  +  Y² · 2β / π   =  O(Y · log Y),

where `E_∞ = Σ_v (#reps with exact sum v)²` and `2β` bounds the number of prime
factors `≥ P` of a nonzero difference `|N| ≤ w·max a` (since
`#{p : p | N} ≤ log|N|/log P ≤ 2β`).

*Proof sketch.* Sum the defining indicator: `Σ_p E_p = Σ_{y,y'} #{p : p | Σy−Σy'}`.
Diagonal and exact-collision pairs contribute `π` each (`E_∞` total); every other
pair contributes at most `2β`. ∎

**Consequence (Markov).** For `1/polylog` of the window, coverage is at least
`Y/polylog`; for `>1/2` of the window, `E_p ≤ 2Y log Y`, coverage `≥ Y/(2 log Y)`.
So a *random* prime mixes to within a polylog factor, for **every** instance.

**Numeric check** (sparse `β=1`, dissociated support, `E_∞ = Y`):

| n | Y | #primes | avg `E_p` | `Y log₂Y` | crude bound | avg coverage | **min coverage** |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 70 | 15 | 132 | 429 | 653 | 0.46 | 0.32 |
| 20 | 252 | 43 | 440 | 2010 | 2954 | 0.48 | 0.32 |

`E_p ≈ 2Y` (the birthday baseline), and the minimum coverage over *all* primes
is `0.32`, not just the average.

## 3. The obstruction this exposes

If coverage is a constant fraction for most (or all) primes, the HGJ filter +
the `2^(0.4057n)` balanced sub-solver would give a worst-case `2^(0.4057n)`
algorithm — contradicting the field's 50-year stagnation. So at least one of the
following is the true barrier, and identifying it is now the concrete goal:

1. **Adversarial low coverage.** Some instance family has `s_p = o(Y)` for every
   `p` in the algorithm's window. Randolph–Węgrzycki prove such families exist
   for other coefficient sets; none was found for `{0,1}` (`mixing_counterexample.md`,
   `hgj_adversarial.md`, up to `n = 40`; low coverage only on arithmetic
   progressions). **Not supported so far.**
2. **Profile / completeness (confirmed).** The balanced sub-solver only
   enumerates weight-`n/4` pieces split `n/8`–`n/8` across the split. A solution
   with no balanced representation is never seen, so the search returns a wrong
   ``no''. `hgj_profile.md` confirms this: success is `1.00` exactly when the
   solution's first-half share is `n/4` and `0.00` otherwise; one random
   permutation repairs it only with the (small) probability that the support
   lands balanced. Enumerating *all* weight profiles costs
   `sum_i C(n/2,i)C(n/2,n/4-i) = C(n,n/4) = 2^{0.811n}`, above meet-in-the-middle.
   This is the genuine obstacle, and it is a *completeness* rather than a mixing
   problem.

   **Correction (2026-10-06, `profile_permutation.md`).** The `2^{0.811n}` cost
   is not the price of completeness. A uniformly random permutation of the
   inputs balances a weight-`w` support with probability
   `C(n/2,w/2)^2 / C(n,w) ~ sqrt(8/(pi n))` at `w = n/2` (exact vs sampled
   agree to sampling error, `n` up to 1024), so `O(sqrt n)` permutations
   restore completeness at a polynomial factor (`src.hgj.hgj_permuted_search`;
   concentrated solutions at `n = 24, 32` are all found within a budget of
   `4 sqrt n` permutations). Unknown weight costs a further factor `n`. The
   profile is therefore **not** an exponential barrier, and obstruction 2 should
   be read as a polynomial overhead. This sharpens the contradiction in the
   opening of Sect. 3: with profile removed, what remains is mixing
   (obstruction 1) and the accounting (obstruction 3). A second finding from the
   same run: the power-of-two filter modulus is itself a weakness on
   structured inputs (geometric family: success 0.50 vs 1.00 at `n = 32` with a
   prime modulus of the same size), so a prime modulus is the right default.
3. **Accounting subtlety.** The retry/coverage argument loses a polylog; a
   constant-exponent claim needs coverage constant for a *single* prime, which
   Markov alone does not give (it gives a `1/polylog` fraction of good primes).

## 4. Suggested next steps

1. **Refute or confirm (3.1) by a targeted adversarial search.** Construct
   two-scale weights `a_i = q·b_i + r_i` with `q` a product of many small
   primes, CRT/GAP-structured sets, near-APs, and "carry" families; at
   `n = 22–28` measure `min_p s_p / Y` over large prime windows. A family with a
   uniformly low ratio settles the lifting (negative) and gives a clean barrier.
2. **Prove the average-energy lemma and its corollary rigorously** (elementary
   number theory), then **implement the full filter + balanced sub-solver +
   disjointness certificate** and measure *actual* work on the adversarial
   families. If mixing holds but runtime still hits `2^{0.5n}`, the barrier is
   (3.2) and the target shifts to the sub-solver/profile.
3. **Specialize Randolph–Węgrzycki Lemma 5.1 to `C={0,1}` target form.** Their
   dichotomy concludes "unbalanced solution or many solutions"; locate the exact
   step where "many solutions" fails to yield the target, and try to replace it
   by additive structure (GAP) via Shao/Shkredov.
4. **AKKN route.** In the hard band `2^{(0.5−ε)n} < β < 2^{0.661n}`, prove
   weight-`w` sums mix (using the bin-size bound) and run HGJ; combine with
   AKKN's fast regimes at the extremes for a full `2^{(1/2−ε)n}` algorithm.
5. **Formalize the average-energy lemma's combinatorial core** (the
   `Σ_{T,T'} #{p : p | N}` identity and the `E_∞` split) in Lean, extending
   `lean/SubsetSum.lean`.

## 5. Honest verdict

The literature sweep found no valid resolution (the one preprint claiming one is
unsound) and three rigorous tools that fit our framework: small-doubling
solvers, density/binsize dichotomies, and energy→GAP inverse theorems. The new
average-energy lemma shows mixing is generic in a strong averaged sense, and
small-`n` evidence says it may even be pointwise — which sharpens the open
problem from "prove mixing" to **"find the adversarial poorly-mixing family or
identify the sub-solver barrier"**. That is a concrete, falsifiable target for
the next iteration.

## 6. BCJ port status

The plan is to broaden the representations (Becker-Coron-Joux, ePrint 2011/474)
so every solution is seen across all weight profiles, and to recover a compatible
pair with a certificate (Randolph-Węgrzycki Thm 8.1). Status:

- **Paper obtained.** The IACR ePrint PDF is reachable through Firecrawl (the
  plain/`pdftotext` and HAL routes are bot-blocked); the full text of the
  three-level construction (Sect. 3.3, eight lists + Algorithm 1) is now in hand.
- **Broadened representation done (Sect. 3.1).** `src/bcj.py` implements the
  two-piece `{-1,0,1}` representation: pieces with `(1/4+alpha)n` ones and
  `alpha n` minus-ones, an exact compatibility test (`y+z in {0,1}^n`), a filter
  modulus `M ~ N_D`, and a meet-in-the-middle fallback. Tests match brute force;
  `bcj_broadened.md` shows `N_D` and the ambient list grow with `alpha` while the
  filtered class stays small. This is the *single-level* construction, not the
  recursion.
- **Compatibility done (exact).** `src/compatibility.py` implements the
  disjointness predicate as a sparse-OV search; `hgj_search(..., certificate=True)`
  routes the pseudo-solution step through it. It is exact, but the submask
  enumeration is not asymptotically better than the linear scan; the efficient
  version needs RW Thm 8.1's block/inclusion-exclusion certificate.
- **Next.** Port BCJ's three-level recursion (Algorithm 1 with the eight lists
  and moduli `M_nu < M_kappa < M_omega`), swap in the efficient certificate, and
  measure the worst-case curve against the `0.4057n` balanced sub-solver.
