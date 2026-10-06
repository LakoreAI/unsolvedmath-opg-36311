# Single-prime lift under a distinct-sums hypothesis

Status (2026-10-06): an elementary, pen-and-paper result that closes the
"lifting" gap of `MIXING.md`/`NEXT.md` *conditionally*, and states exactly which
instances remain. Not Lean-checked. It is a worst-case statement about
`2^{0.4057n}`, so it does not reach `2^{n/3}` and is in the spirit of the
Austrin-Kaski-Koivisto-Nederlof density dichotomy; I do not claim it is new.

## Setting

`x` is a solution of weight `n/2` with support `S` (other weights: replace
`n/2, n/4` by `w, w/2`). Let `T = { sum(y) : y subset S, |y| = n/4 }` and
`D = |T|`. Note `D <= Y = C(n/2, n/4)`, and `D = Y` when the sub-sums are
distinct. The algorithm (`src.hgj.hgj_permuted_search`) draws a random prime
`p in [M, 2M]`, a random residue `r`, a random permutation, enumerates
`Y_r = {y : |y| = n/4, sum(y) = r mod p}` and `Z_r` (target `- r`) by the
balanced split, and matches disjoint exact-sum pairs.

## Proposition

For `M ~ D` (a power-of-two guess, `O(n)` guesses tried in turn) the expected
running time is

    poly(n) * ( 2^{0.4057n} + C(n, n/4) / D ),         (bit length poly(n))

so `poly(n) * 2^{0.4057n}` whenever `D >= 2^{0.4057n}`, and below `2^{n/2}`
exactly when `D > 2^{0.311n}`.

## Proof

1. **Success event.** A pair `(y, S \ y)` is found when (i) the permutation
   balances `S` (probability `Theta(1/sqrt n)`, `docs/analysis/2026-10-06/subset-sum/profile_permutation.md`), and (ii) `r` is
   the residue of some `t in T` mod `p`, i.e. `r in T mod p`. Then `y in Y_r`
   and `S \ y in Z_r`.
2. **Coverage.** Let `c_r = #{t in T : t = r mod p}`, so `sum c_r = D`,
   `sum c_r^2 = D + K_p` where `K_p` counts ordered pairs `t != t'` with
   `p | t - t'`. By Cauchy-Schwarz the number of covered residues is
   `>= D^2 / (D + K_p)`. Each nonzero difference has absolute value `<= nA`
   (`A = max a_i`) so at most `B = log(nA)/log M` prime factors `>= M`; hence
   over a uniformly random prime in the window (`pi` primes)
   `E_p K_p <= D^2 B / pi`. Jensen on `u -> D^2/(D+u)` (convex) gives
   `E_p |T mod p| >= D / (1 + D B / pi)`. With `pi ~ M / ln M` and
   `M >= 2 D B ln M` this is `>= D/2`; so `Pr_r[ r covered ] >= D / (4M)`
   (using `p <= 2M`). **This is the coverage bound, unconditional on the
   inputs; the only hypothesis is how large `D` is.**
3. **List size.** `sum_r |Y_r| = C(n, n/4)` for every prime, so
   `E_r |Y_r| = C(n, n/4)/p`. By Markov,
   `Pr_r[ |Y_r| > lambda C(n,n/4)/p ] <= 1/lambda`. Take `lambda = 8M/D`:
   `Pr[ covered and |Y_r| <= lambda C/p ] >= D/(4M) - D/(8M) = D/(8M)`.
4. **Cost.** A good attempt costs the balanced split plus the lists:
   `2^{0.4057n} + lambda C(n,n/4)/p <= 2^{0.4057n} + 8 C(n,n/4)/D`. The
   expected number of attempts is `O(sqrt n) * 8M/D = poly(n)` for `M ~ D`.
   Multiply and take the guess `M ~ D`. `[]`

## What is left, and the check

Instances not covered are those whose every solution has
`D <= 2^{0.311n}`, i.e. a weight-`n/4` sumset of an `n/2`-element set that is
polynomially smaller than the `2^{n/2}` representations: very high additive
energy, the Balog-Szemeredi-Gowers/Freiman regime of `NEXT.md` Sect. 4.3. The
average-energy lemma of `NEXT.md` and this proposition agree: `E_infty = Y^2/D`
in the best case, so `Y log Y` bounds hold exactly when `D ~ Y`.

`lift_check.md` verifies step 2 numerically at `n = 24, 28`: measured mean
coverage `0.92-0.94` of `D` versus the proved lower bound `0.09-0.31`, on every
family; low `D` appears only on arithmetic progressions (`D/Y = 0.09`, `0.03`),
which are easy for other reasons, and `gap-rank2`/`q-multiple` keep `D/Y > 0.95`.
Open: **prove or refute that a `{0,1}` instance with no easy structure can have
every solution's support with `D <= 2^{0.311n}`.** That is the new, sharper form
of the lifting question.
