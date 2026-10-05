# A worst-case attack on `{0,1}` subset sum: reduce to one mixing dichotomy

Status (2026-10-05): a concrete reduction of the open bound to a single
target-problem mixing dichotomy, plus evidence. This is not a solution; it
isolates what a solution now needs, and why the leading worst-case framework
(Randolph–Węgrzycki, STOC 2026) does not already supply it.

## What is already known

- Horowitz–Sahni / Schroeppel–Shamir: `O*(2^(n/2))` worst case (the barrier).
- Howgrave-Graham–Joux (2010), refined by Becker–Coron–Joux (2011) and
  Bonnetain et al. (2020): `2^(0.337n)`, `2^(0.291n)`, `2^(0.283n)` for **random**
  density-1 knapsacks, via the representation technique. The ePrint long version
  of HGJ states the ideal `2^(0.3113n)`.
- Randolph–Węgrzycki (arXiv:2511.10823, STOC 2026) make the representation
  technique **worst-case** for coefficient sets `[−d:d]` (`d>1`) and `[±d]`
  (`d>2`), using a *mixing dichotomy* plus *coefficient shifting* plus
  *compatibility certificates*. They leave `[±1]` (Partition) and `[±2]` open;
  Partition is exactly `{0,1}` subset sum up to the standard complement gadget.

## The `{0,1}` representation

Let `(w, t)`, `w ∈ Z_+^n`, be a subset sum instance with a **balanced** solution
`x* ∈ {0,1}^n`, `|x*| = n/2` (unbalanced solutions are handled by a folklore
variant of meet-in-the-middle). HGJ write

    x* = y + z,   y, z ∈ {0,1}^n disjoint, |y| = |z| = n/4,

which has `C(n/2, n/4) ≈ 2^(n/2)/poly(n)` representations. The algorithm:

1. choose a random prime `p ≈ C(n/2, n/4)` and a residue `r`;
2. enumerate `Z = { y ∈ {0,1}^n : |y| = n/4, y·w ≡ r (mod p) }`, of size
   `C(n,n/4)/p ≈ 2^(0.311n)` **if the representations mix**;
3. find `(y,z) ∈ Z × Z` with `y + z ∈ {0,1}^n` (disjointness) and
   `(y+z)·w = t` exactly.

Step 2 is output-linear only if the sums `y·w` spread over the `p` residues;
otherwise the chosen class may miss every representation of `x*`. This is the
mixing condition. (Enumerating `Z` itself is the *balanced sub-solver*, costing
`C(n/2,n/8) ≈ 2^(0.4056n)` by balanced meet-in-the-middle; HGJ's ideal `0.3113n`
and BCJ's `0.291n` come from replacing it with a 4-way decomposition plus the
unbalanced Schroeppel–Shamir sub-solver. That piece is orthogonal to the
contents here and is treated by R8–R11.)

## Two of the three steps are within reach

- **Disjointness is sparse Orthogonal Vectors.** The condition
  `y + z ∈ {0,1}^n` is `supp(y) ∩ supp(z) = ∅`, i.e. the sparse OV predicate.
  The compatibility-certificate machinery of Nederlof–Węgrzycki and Theorem 8.1
  of Randolph–Węgrzycki recovers a compatible pair from lists admitting
  pseudo-solutions in near-linear time in the list size (up to a `2^(c·n)`
  factor). Adapting their certificate to the disjointness predicate is a
  technical but tractable step.
- **Unbalanced solutions** are folklore fast (`O*(|C|^(0.5−δ)n)`), as in
  Randolph–Węgrzycki Section 4.

## The missing lemma: a target-problem mixing dichotomy

Everything reduces to the following, which is **not** implied by the existing
mixing dichotomies.

> **Conjecture (target mixing dichotomy).** There is a `δ > 0` such that for
> every instance `(w, t)` with a balanced solution `x*`, at least one holds:
> (a) the weight-`n/4` representation sums `y·w` of `x*` hit `≥ 2^(−δn)` of the
> residues modulo a random prime `p ≈ C(n/2,n/4)` (they mix); or
> (b) `(w, t)` is solvable in time `O*(2^(1/2−δ)n)`.

If the Conjecture holds, the HGJ pipeline above solves `{0,1}` subset sum in
`O*(2^(1/2−ε)n)` for a constant `ε`, and the conjecture's own proof method is
what fixes `ε`; the `2^(n/3)` target corresponds to `ε = 1/6` and would need the
sub-solver of step 2 at `2^(n/3)` as well.

### Why Randolph–Węgrzycki do not already give it

Their zero-coefficient dichotomy (Lemma 5.1, `C = [−d:d]`) concludes that poor
mixing produces an **unbalanced solution or many solutions** — useful for a
*balancing* goal `c·w = 0`. For the *target* problem `x·w = t`, many zero
relations (`ESS` solutions) do **not** produce a subset summing to `t`; this is
the average-case → worst-case gap of `TRANSFER.md`. For `[±1]`/`[±2]` they fall
back on **coefficient shifting**, which provably fails for `{0,1}`/`[±1]`/`[±2]`
(R12: no useful sumset factorisation). So the target form of the dichotomy must
conclude with *structure that solves the target*, not with many zero relations.

## Evidence for the dichotomy

`mixing_dichotomy.md` measures representation coverage versus additive structure
across adversarial families (planted balanced solution; `p ≈ C(n/2,n/4)`):

| family | coverage (n=20) | doubling |
| :-- | ---: | ---: |
| constant | 0.004 | 1.0 |
| arithmetic | 0.175 | 1.95 |
| geometric | 0.475 | 10.5 |
| random-small | 0.634 | 9.7 |
| random-large (dissociated) | 0.611 | 10.5 |
| Sidon | 0.638 | 10.5 |

The **only** low-coverage families are the structurally easy ones (constant,
arithmetic — small doubling; geometric — superincreasing). The hard,
large-value/dissociated families all mix at `~0.6`, so a random residue retains
a representation. This is the behaviour the Conjecture predicts, and it is
consistent with R6 (modular coverage `~0.6` for hard families) and H1 (random
restrictions always supply a balanced representation). No low-coverage hard
family was found at these sizes.

## Failure modes and how to attack them

1. **Mixed but shallow.** Coverage `~0.6` is constant-bounded, not `1`. The
   filtered class contains a representation with constant probability only if
   `p` is chosen so `p·coverage ≤ #reps`; the covering argument must budget the
   `2^(c·n)` compatibility factor against it.
2. **Pseudo-solutions.** Disjointness certificates must handle the `2^(c(ε)n)`
   overhead (RW Theorem 8.1); for `{0,1}` the predicate is simpler and the
   constant should improve.
3. **Sub-solver.** Even with perfect mixing, step 2's enumeration is the
   `0.4056n` balanced sub-solver unless replaced by the 4-way/SS decomposition
   (R8–R11). A complete `2^(1/2−ε)n` algorithm needs this too.

## Honest verdict

This is a real reduction: it turns "beat meet-in-the-middle for `{0,1}`" into
one target-problem mixing dichotomy plus one adaptation of an existing
compatibility certificate. The measurement supports the dichotomy; the
remaining work is a proof, or a counterexample instance that mixes poorly while
staying hard — which would itself be a clean barrier and a refutation of the
optimistic reading of Randolph–Węgrzycki's results.
