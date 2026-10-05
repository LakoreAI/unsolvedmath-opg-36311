# Why the PESS `O*(2^(n/3))` structure does not transfer to `{0,1}` subset sum

Status (2026-10-05): a precise barrier statement, not a solution. It isolates the
single extra ingredient a `{0,1}` algorithm would need, and records which
candidate routes the R-probes have already closed.

## The engine of the PESS result

Jin–Williams–Zhang (ESA 2025, Theorem 1) solve Pigeonhole Equal Subset Sum in
`O*(2^(n/3))`. Their structural engine is Lemma 4 of Jin–Wu, which needs three
hypotheses on positive `w_1 < ... < w_n`:

1. **Equation (1):** `w([i]) >= 2^i - 1` for all `i <= n-1` (WLOG, by recursing
   on the smallest failing prefix);
2. **the pigeonhole promise:** `w([n]) < 2^n - 1`;
3. a collision parameter `k` with `2^k <= F(w) < 2^(k+1)`, where
   `F(w) = sum_t max(0, count(t) - 1)` and `count(t)` is the number of subsets
   with sum `t`.

Under these, Lemma 4 proves `-i F <= w_i - 2^(i-1) <= F` for every `i`: **few
collisions force the input to be nearly geometric.** The promise is what makes
this true. It bounds the sum range to `[0, 2^n - 1]`, so every one of the `2^n`
subsets lands in a box of `2^n - 1` values (an `F >= 1` guarantee), and then
`F = 2^n - |{0 <= t < 2^n : count(t) >= 1}|` counts exactly the *missing* sums.
With `F` controlling how many integers are skipped, Claim 14 (`w_i <= 2^(i-1)+F`)
and the gap identity (`w_i >= 2^(i-1) - iF`) pin each weight to its geometric
slot.

## The promise is essential

**Proposition.** No promise-free analogue of Lemma 4 holds: for every `n` and
every bound `B`, there are positive integers `w_1 < ... < w_n <= B` with
`F(w) = 0` but `max_i |w_i - 2^(i-1)| >= B - 2^(n-1)`.

*Proof.* Scale a geometric progression: take `w_i = C * 2^(i-1)` with
`C >= 2`. All `2^n` subset sums are distinct (binary representations of
multiples of `C`), so `F(w) = 0`, while
`|w_n - 2^(n-1)| = (C-1) 2^(n-1)`, which tends to infinity with `B`. ∎

This is the R5/dichotomy observation in symbolic form: **dissociated instances
(`|S(A)| = 2^n`, `F = 0`) exist at every scale and are arbitrarily far from
geometric.** Lemma 4 has no content for them, and vanilla `{0,1}` subset sum
carries no promise at all — the target may have a unique representation, and the
input sum `w([n])` is unrestricted, so `F` can be `0` even when the weights are
enormous (`dichotomy.md`, the "danger zone" row).

## What a `{0,1}` algorithm would need

By the Proposition, a PESS-style attack on `{0,1}` subset sum cannot reuse
Lemma 4. It must supply one of:

- **(A) a promise-forcing reduction** that turns a `{0,1}` instance into a
  near-geometric one without changing satisfiability. The known route to
  surplus structure, coefficient shifting `C = C_1 + C_2`, provably fails for
  `{0,1}` (R12; the representation note's Proposition: `{0,1}` has no useful
  sumset factorisation).
- **(B) a promise-free structure dichotomy**: a statement that every input is
  *either* solvable fast by additive structure *or* has enough collisions/
  representations to be attacked, valid even when `F = 0`. The measured probes
  constrain this: dissociated (`F=0`) inputs are modularly spread like random
  ones (R6), so the representation filter applies, but the balanced sub-solver
  cost is the bottleneck (R7–R11); birthday/subsampling cannot beat it (R9);
  cheap collisions have support `~n/2` and do not multiply solutions (R19–R21).
- **(C) an all-three-block algorithm**: the pairwise-sumset route fails in the
  hard band (P2.1), so a three-block `2^(n/3)`-size 3SUM must exploit
  cancellation across all three blocks simultaneously (a shared modular filter),
  not the size of any pairwise sumset.

The R12 characterisation says exactly why `{0,1}` is the stubborn case: it is
one of the coefficient sets with no zero coefficient and no nontrivial sumset
factorisation, so the worst-case representation technique has no surplus to
exploit. Closing the conjecture therefore requires a genuinely new mechanism, or
a proof that none exists.

## Relation to the open bound

PESS reaches `O*(2^(n/3))` *because of* the promise (many solutions). The
general `{0,1}` question asks for the same exponent with no promise and a
possibly unique solution; the two problems are separated precisely by the gap in
the Proposition. This is the same average-case → worst-case gap identified in
R11, now stated at the level of the structural lemma itself.
