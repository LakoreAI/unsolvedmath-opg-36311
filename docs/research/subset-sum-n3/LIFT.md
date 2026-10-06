# Single-prime lift under a distinct-sums hypothesis

Status (2026-10-06): an elementary, pen-and-paper result that closes the
"lifting" gap of `MIXING.md`/`NEXT.md` *conditionally*, and states exactly which
instances remain. Not Lean-checked. It is a worst-case statement about
`2^{0.4057n}`, so it does not reach `2^{n/3}` and is in the spirit of the
Austrin-Kaski-Koivisto-Nederlof density dichotomy; I do not claim it is new.

## Setting

`x` is a solution of weight `n/2` (`n` a multiple of 8) with support `S`, `|S| = n/2`.
For a partition `S = S1 u S2` into halves of size `n/4`, let
`T(S1,S2) = { sigma(y1)+sigma(y2) : y_i subset S_i, |y_i| = n/8 }` and
`D* = min over partitions |T(S1,S2)|` (so `D* <= C(n/4,n/8)^2`). The algorithm
(`src.hgj.hgj_permuted_search`) draws a random permutation `pi` (this defines the two
halves `H1, H2` of the input, each of size `n/2`), a random prime `p in [M, 2M]` and a
random residue `r`; it enumerates `Y_r = {y : |y cap H_i| = n/8, sigma(y) = r mod p}` and
`Z_r` (residue `t - r`) by the balanced split, and reports a disjoint pair with
`sigma(y)+sigma(z) = t`. Write `A = C(n/2,n/8)^2` (the number of balanced `n/4`-subsets;
`log2 A = 0.811 n`) and `N_t` for the number of pairs `(y, z)` of balanced `n/4`-subsets
with `sigma(y) + sigma(z) = t` (not necessarily disjoint).

## Proposition

For `M ~ D*` (a power-of-two guess, `O(n)` guesses tried in turn) the expected running time
is `poly(n) * ( 2^{0.4057n} + (A + N_t) / D* )` (bit length `poly(n)`), hence `poly(n) *
2^{0.4057n}` whenever `D*` and the pair count satisfy `D* >= 2^{0.4057n}` and
`N_t <= A`; and below `2^{n/2}` whenever `A + N_t < 2^{n/2} D*`, e.g. `N_t <= A` and
`D* > 2^{0.311n}`.

## Proof

1. **Success event.** If `pi` places exactly `n/4` support elements in each half
   (probability `C(n/2,n/4)^2/C(n,n/2) = Theta(1/sqrt n)`,
   `docs/analysis/2026-10-06/subset-sum/profile_permutation.md`), the induced partition
   `(S1, S2)` of `S` has `|S_i| = n/4`. Every `y = y1 u y2` with `y_i subset S_i`,
   `|y_i| = n/8`, is balanced and so is `S \ y`. So if `r` is the residue of some element of
   `T(S1,S2)` mod `p`, then `y in Y_r` and `S \ y in Z_r`.
2. **Coverage.** Let `c_r = #{t in T : t = r mod p}` for `T = T(S1,S2)`, `D = |T|`. Then
   `sum c_r^2 = D + K_p`, `K_p` the number of ordered pairs `t != t'` with `p | t - t'`. By
   Cauchy-Schwarz the number of covered residues is `>= D^2/(D + K_p)`. Each nonzero
   difference has absolute value `<= nA_max` so at most `B = log(n A_max)/log M` prime factors
   `>= M`; over a uniform prime of the window (`pi_w` primes) `E_p K_p <= D^2 B / pi_w`. Jensen
   (convexity of `u -> D^2/(D+u)`) gives `E_p |T mod p| >= D/(1 + D B/pi_w)`. With
   `pi_w ~ M/ln M` and `M >= 2 D B ln M` this is `>= D/2`, so `Pr_r[r covered] >= D/(4M)`
   (`p <= 2M`).
3. **List sizes and pair count.** For every prime `sum_r |Y_r| = A`, so `E_r |Y_r| = A/p`; the
   same for `Z`. Every pair counted by `N_t` lies in exactly one `Y_r x Z_{t-r}` (its residue
   is fixed by `y`), so `E_r[#exact pairs in Y_r x Z_{t-r}] = N_t/p`. By Markov and a union
   bound over the three quantities, with `lambda = 24 M/D`:
   `Pr[covered and |Y_r|,|Z_r| <= lambda A/p and pairs <= lambda N_t/p] >= D/(4M) - 3/lambda
   = D/(8M)`.
4. **Cost.** A good attempt costs the balanced split `2 C(n/2,n/8) = 2^{0.4057n}`, plus the
   lists and the exact-sum matching (hashing on the exact sum, plus the disjointness test on
   each exact-sum pair): `<= lambda (A + N_t)/p <= 48 (A+N_t)/D`. The expected number of
   attempts is `O(sqrt n) * 8M/D = poly(n)` for `M ~ D`. Multiply. `[]`

## What is left, and the check

Instances not covered are those whose every solution has
`D* <= 2^{0.311n}` (or a large pair count `N_t`, the large-bin regime), i.e. a weight-`n/4` sumset of an `n/2`-element set that is
polynomially smaller than the `2^{n/2}` representations: very high additive
energy, the Balog-Szemeredi-Gowers/Freiman regime of `NEXT.md` Sect. 4.3. The
average-energy lemma of `NEXT.md` and this proposition agree: `E_infty = Y^2/D`
in the best case, so `Y log Y` bounds hold exactly when `D ~ Y`.

`lift_check.md` verifies step 2 numerically at `n = 24, 32` (balanced sums `D*` for a random
split of the support): measured mean coverage `0.93-0.96` of `D*` versus the proved lower bound
`0.12-0.33`, on every family; low `D*` appears only on arithmetic progressions (`D*/Y = 0.19`,
`0.02`), which are easy for other reasons, and `gap-rank2`/`q-multiple` keep `D*/Y >= 0.97`.
Open: **prove or refute that a `{0,1}` instance with no easy structure can have
every solution's support with `D <= 2^{0.311n}`.** That is the new, sharper form
of the lifting question.
