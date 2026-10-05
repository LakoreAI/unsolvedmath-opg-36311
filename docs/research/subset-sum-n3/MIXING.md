# Toward the target mixing dichotomy

Status (2026-10-05): an elementary step is proved; the additive-combinatorics
lifting step is stated as the precise gap. This is the (a) half of the attack;
the (b) half is the candidate pipeline `src/representation.py` /
`subset_sum_pipeline.md`.

## Setup

Fix `A = {a_1, ..., a_m} ⊆ Z` (the support of a balanced solution, `m = n/2`),
a prime `p`, and a weight `w` with `1 ≤ w ≤ m-1`. The HGJ filter uses the
weight-`w` sums

    V := { (Σ_{i∈T} a_i) mod p : T ⊆ [m], |T| = w },    s := |V|.

"Good mixing" is `s ≈ p`; "poor mixing" is `s` small. The conjecture of
`ATTACK.md` is that poor mixing forces additive structure that makes the target
easy.

## What is proved: poor mixing concentrates `A` modulo `p`

**Lemma (concentration).** `|{ (a_i - a_j) mod p : i,j ∈ [m] }| ≤ s²`.

*Proof.* Fix `i,j`. Since `w ≤ m-1` and `m ≥ 2`, choose `S ⊆ [m] \ {i,j}` with
`|S| = w-1`. Then `T_i = S ∪ {i}` and `T_j = S ∪ {j}` both have weight `w`, so
`a_i + Σ_{k∈S} a_k ∈ V` and `a_j + Σ_{k∈S} a_k ∈ V`. Subtracting,
`a_i - a_j ≡ (a_i + Σ_S) - (a_j + Σ_S) ∈ V - V`, and `|V - V| ≤ s²`. ∎

**Corollary.** `|{ a_i mod p }| ≤ s² + 1`.

So poor mixing forces the residues of `A` modulo `p` into a set with a small
difference set. If additionally `s² + 1 < m`, some two weights satisfy
`a_i ≡ a_j (mod p)`; i.e. `A` is *concentrated* modulo `p`.

## The `s = 1` case is fully solvable

If all weight-`w` sums are congruent, the lemma gives `a_i ≡ a_j (mod p)` for
all `i,j`; write `a_i ≡ r (mod p)`. Then every weight-`w` sum is `w·r`, and every
subset sum is `|T|·r + p·(subset sum of B)` where `B = (a_i - r)/p`. The target
`t` fixes `|T|·r`, and the remaining instance on `B` is smaller by
`≈ log2 p` bits in each value. This is a recursion: **concentration modulo `p`
lets us strip `p` from all weights**, which is exactly the structural branch the
candidate pipeline approximates with gcd reduction. More generally, a small `s`
puts `A mod p` in a short generalized arithmetic progression (Freiman / Kneser),
so the same stripping-and-recursing applies.

### A cautionary example

`A = { p·2^0, p·2^1, ..., p·2^(m-1) }` has `s = 1` (all weight-`w` sums `≡ 0`),
yet `|S(A)| = 2^m` (all subset sums distinct) — poor mixing does **not** imply a
small sumset. It implies *structure*: every weight is divisible by `p`, so
divide and recurse to a geometric instance, which is superincreasing and solved
greedily. This is why the dichotomy's conclusion must be "structured/solvable",
never "small `|S(A)|`" (consistent with powers of two being dissociated yet
easy).

## The gap: lifting modulo `p` to structure over `Z`

The lemma is only about a fixed `p`. The algorithm chooses `p` at random, so the
dichotomy must read:

> **Conjecture (target mixing dichotomy, refined).** For a **randomly chosen**
> prime `p ≈ 2^(n/2)`, either the weight-`n/4` representation sums of `x*` cover
> `≥ 2^(−δn)` of the residues, or `(w, t)` is solvable in `O*(2^((1/2−δ)n))`.

What is missing is a *random-prime lifting*: from "`A mod p` concentrates for a
random `p`" to "`A` has a common factor or lies in a short GAP over `Z`". The
adversarial example `A = p·geometric` concentrates only for the *one* prime `p`
that divides every weight; a random prime does not divide all of `A` unless
`gcd(A)` is large (which the candidate's gcd branch handles). This is precisely
the shape of Randolph–Węgrzycki's Lemma 5.1 argument, but their conclusion
("unbalanced solution or many solutions") is about balancing and does not solve
the target; the target version must conclude with GAP/gcd structure and a
recursion.

## Evidence

- `mixing_dichotomy.md`: the only low-coverage families (constant, arithmetic,
  geometric) are exactly the structured ones; hard large-value and Sidon families
  mix at `~0.6`.
- `subset_sum_pipeline.md`: the candidate pipeline (gcd + superincreasing greedy
  + HGJ filter + disjointness + MITM fallback) is correct on every planted
  instance and routes structured families to the greedy branch, hard families to
  the representation branch (`work exponent ~0.36–0.43 < 0.5`).

## Formalization (Lean 4.19, `Std` only)

The kernel lemmas are formalized in `lean/SubsetSum.lean`, all with axioms
`[propext, Quot.sound]`:

- `value_diff_mem_wsum_diff` — the concentration lemma in exact arithmetic:
  two weight-`w` index sets differing only in `i` versus `j` have sums differing
  by `a i - a j`, witnessed by a common `S`.
- `value_diff_mod_mem_wsum_mod_diff` — the residue form: `(x % p - y % p) % p`
  equals `(a i - a j) % p`, via `Int.sub_emod`.
- `dvd_listSum_sub_length_mul` — the `s = 1` contraction kernel: if `p ∣ a i - ρ`
  for all `i`, then `p ∣ listSum a s - s.length · ρ`, so `p` can be stripped and
  the instance recursed.

## Brutal attack on the lifting

### 1. The contraction is exact and proved

**Contraction lemma.** If `|A mod p| = r` with classes `C_1, …, C_r` of residues
`ρ_1, …, ρ_r`, then for every `T ⊆ [m]`

    Σ_{i∈T} a_i = Σ_j |T ∩ C_j| · ρ_j + p · Σ_j Σ_{i∈T∩C_j} b_i,   b_i = (a_i - ρ_j)/p.

The `r = 1` case is formalized (`dvd_listSum_sub_length_mul`). So poor mixing
*does* give exact structure: `A` splits into `r` classes, each contracted by `p`.

### 2. The exact analytic object: the collision energy

Let `M = C(m,w)`, `ζ = e^{2πi/p}`, `c_r = #{|T| = w : Σ_T ≡ r (mod p)}`. Then

    E_p := Σ_r c_r² = (1/p) Σ_{k=0}^{p-1} |e_w(ζ^k)|²,   e_w(ζ^k) = Σ_{|T|=w} ζ^{k Σ_T},

(write `[p | N] = (1/p)Σ_k ζ^{kN}` and expand). Poor mixing means small
coverage `s_p`, and `E_p ≥ M²/s_p`, so the dichotomy is exactly:
**either `e_w` is small on average (generic, mixing), or the elementary
symmetric polynomial is anomalously large (structure).** This is the object a
lifting proof must bound; note it is a *higher-order* energy (over the
weight-`w` slice), not the ordinary additive energy of `A`.

### 3. Why the first-moment number-theoretic count fails

For a nonzero difference `N_d = d·a`, the number of primes `p ∈ [P,2P]`
dividing `N_d` is at most `log|N_d| / log P ≤ 2β` (a constant for `β` the bit
density). This bounds the *per-difference* bad-prime count but not the
per-prime collision count: the baseline birthday count is `M²/p ≈ M`, already
far larger than the number of primes, so the union bound over `M²` differences is
vacuous. A lifting proof needs a **second-moment / higher-order energy bound**
(a `weight-w`-slice Balog–Szemerédi–Gowers-type statement), which is the genuine
gap.

### 4. Counterexample search (`mixing_counterexample.md`)

Over adversarial families (`n = 18, 20`; several random primes each, taking the
best coverage because the algorithm may retry):

- Every **hard** family (`gcd 1`, not superincreasing, `|S(A)|/2^n > 0.5`) —
  `random-b1.0`, `random-b1.25`, `common-factor`, `Sidon` — had best coverage
  `≥ 0.47`; no poorly-mixing hard instance exists at these sizes.
- The only low-coverage families are structured: `short-ap` (best coverage
  `0.13–0.25`, doubling `≈ 2`) and the easy dense/near-geometric families.

Consistent with `mixing_dichotomy.md`. The random-prime qualifier is doing real
work: `common-factor` (a large common factor with one element perturbed) mixes
at `≥ 0.47` because a random prime almost never divides the factor.

## Honest verdict

The elementary half of the target mixing dichotomy is **proved and formally
verified** (concentration + contraction kernels), the collision energy gives the
exact analytic criterion, and the counterexample search finds no poorly-mixing
hard instance. The remaining gap is a **higher-order energy bound** on the
weight-`w` sum slice for a random prime, from which structure (a short GAP or a
common factor) would follow; closing it yields `O*(2^((1/2−ε)n))` for `{0,1}`
subset sum. This is a concrete, well-posed target rather than a vague barrier.
