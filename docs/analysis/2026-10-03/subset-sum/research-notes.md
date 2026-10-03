# Exact Subset Sum — research notes

Date: 2026-10-03. Method: `web-research` router (Tavily / Linkup / Firecrawl)
plus direct primary-source reads. Sources are linked; claims without a source
are marked as background.

## 1. Problem

Given integers `a_1..a_n, b`, decide whether some `x in {0,1}^n` satisfies
`sum_i a_i x_i = b`. Entries may be negative, repeated values are distinct
occurrences, the empty subset is allowed. This is the equality-decision form of
0-1 knapsack; the historical statement is attributed to D. Lipton (2009).

## 2. Worst-case algorithm landscape

| Algorithm | Time | Space | Setting |
| --- | --- | --- | --- |
| Horowitz–Sahni (1974) | `O*(2^(n/2))` | `O*(2^(n/2))` | worst case |
| Schroeppel–Shamir (FOCS'79 / SIAM 1981) | `O*(2^(n/2))` | `O*(2^(n/4))` | worst case |
| Howgrave-Graham–Joux (CRYPTO 2010) | `~2^(0.311n)` | — | hard/random knapsack |
| Becker–Coron–Joux (EUROCRYPT 2011) | `~2^(0.291n)` | — | hard/random knapsack |
| Nederlof–Węgrzycki (STOC 2021) | `O*(2^(0.5n))` | `O*(2^(0.249999n))` | worst case, randomized |
| Chen–Jin–Randolph–Servedio (RANDOM 2023) | `O(2^(n/2) n^(-0.5023))` | `O*(2^(n/4))` | worst case |
| Randolph–Węgrzycki (arXiv 2511.10823, 2025) | `|C|^((0.5-eps)n)` | — | worst case, coefficient sets `C` |

Sources and exact statements:

- **Chen–Jin–Randolph–Servedio**, "Subset Sum in Time `2^(n/2)/poly(n)`",
  arXiv:2301.07134 — abstract: *"a Subset Sum algorithm with worst-case running
  time `O(2^{n/2} n^{-γ})` for a constant `γ > 0.5023` in standard word RAM or
  circuit RAM models ... the first improvement on the classical
  meet-in-the-middle algorithm for worst-case Subset Sum."*
  <https://arxiv.org/abs/2301.07134>
- **Nederlof–Węgrzycki**, "Improving Schroeppel and Shamir's Algorithm for
  Subset Sum via Orthogonal Vectors", STOC 2021 — abstract: *"an
  `O*(2^{0.5n})` time and `O*(2^{0.249999n})` space randomized algorithm for
  solving worst-case Subset Sum ... the first improvement over the
  long-standing `O*(2^{n/2})` time and `O*(2^{n/4})` space algorithm due to
  Schroeppel and Shamir."* <https://arxiv.org/abs/2010.08576>
- **Schroeppel–Shamir**, MIT-LCS-TM-147, "A `T=O(2^{n/2})`, `S=O(2^{n/4})`
  Algorithm for Certain NP-Complete Problems". <https://dspace.mit.edu/handle/1721.1/148974>
- **Howgrave-Graham–Joux** `~2^{0.311n}` and **Becker–Coron–Joux**
  `~2^{0.291n}` are for **hard knapsacks of density close to 1**, not
  arbitrary instances; a sourced answer states they "do not establish a
  worst-case bound". <https://eprint.iacr.org/2011/474>,
  <https://dl.acm.org/doi/10.5555/2008684.2008713>
- **Randolph–Węgrzycki**, "Beating Meet-in-the-Middle for Subset Balancing
  Problems", arXiv:2511.10823 — abstract: *"For `C = {-d..d}, d>1` and
  `C = {-d..d}\\{0}, d>2`, we present algorithms that run in time
  `O(|C|^{(0.5-ε)n})` ... the first algorithms that break the
  `O(|C|^{n/2})`-time Meet-in-the-Middle barrier for these coefficient sets in
  the worst case ... Our results leave two natural cases in which we cannot yet
  break the Meet-in-the-Middle barrier: `C = {-2,-1,1,2}` and `C = {-1,1}`
  (Partition)."* <https://arxiv.org/abs/2511.10823>

## 3. Status of the target bound

Sourced answer (Linkup, 2026-10-03), cross-checked against the primary
abstracts: as of 2025 there is **no worst-case `O(2^{(1/2-ε)n})` algorithm for
standard `{0,1}`-coefficient Subset Sum** for any constant `ε > 0`. The best
worst-case improvement is the Chen et al. polynomial-factor saving
`2^{n/2}/n^{0.5023}`. The classical `2^{n/2}` exponential barrier stands.

## 4. Structural facts that constrain an attack

1. **Bounded values are easy.** If `|a_i| <= poly(n)` then `W = sum|a_i| <=
   poly(n)` and the dense DP `O(n(2W+1))` is polynomial. Hardness needs large
   values.
2. **Superincreasing values are easy.** Powers of two give `W = 2^n - 1` yet
   are solved by reading the binary expansion. So "large values" alone is not
   hardness.
3. **Distinctness is not hardness.** Powers of two yield `2^n` *distinct*
   subset sums while remaining easy, so deduplicating sums cannot by itself
   force a better exponent.
4. **The hard regime is density `d = n / log2(max|a_i|) ~ 1`** — exactly where
   the (non-worst-case) representation bounds (0.291–0.311) live.
5. **A 3-block split does not immediately help.** Enumerating each third is
   `2^{n/3}`, but a naive merge of two block lists is `2^{2n/3}` pairs; the
   obstacle is solving a structured 3-sum over `2^{n/3}`-sized sets faster than
   quadratic.

## 5. Research directions (honest assessment)

- **Representation technique, worst case.** The 2025 result shows the
  Howgrave-Graham–Joux representation method can be moved from average case to
  worst case for several coefficient sets. The open cases (`Partition`,
  `{-2,-1,1,2}`) and standard `{0,1}` subset sum are the frontier. This is the
  most credible path.
- **Density dichotomy.** Prove a tradeoff: low additive energy / few
  representations ⇒ superincreasing-like structure solves fast; high additive
  energy ⇒ many representations ⇒ representation/dissection applies. Closes
  the gap between the two regimes.
- **Faster structured 3-sum.** The three-way split reduces the question to
  3-sum on subset-sum sets; bounded-integer or convolution-based 3-sum may
  apply because the value range is controlled.
- **Bit-packing / word-RAM shaving.** Chen et al. use bit-packing (Baran–
  Demaine–Pătraşcu) to gain a polynomial factor; the question is whether it can
  produce an exponential gain.
- **Barriers.** ETH only gives `2^{Ω(n)}`, so `2^{n/3}` is not excluded; a
  conditional lower bound from 3SUM or (min,+)-convolution would be a
  publishable negative result.
- **Measurement.** Reproducible implementations and open measurement of the
  known baselines (MITM, DP, Schroeppel–Shamir) are scarce; providing them with
  provenance is valuable regardless of the open bound.

## 6. Repository findings

- `src/subset_sum.py` implements MITM and a signed dense DP; both pass a
  brute-force differential suite. No `2^{n/2}`-time / `2^{n/4}`-space
  Schroeppel–Shamir baseline existed.
- The report links in `README.md` and `docs/RESEARCH.md` pointed at a
  date/topic directory that did not exist (fixed: files moved to
  `docs/reports/`).
- The ML-template half-migration left deleted files that the README still
  documented (fixed: restored).
- The restricted `W <= 2^{floor(n/3)}` corollary is the textbook
  pseudopolynomial bound and gives no evidence toward the open target.

## 7. Reproduction

```bash
# differential correctness suite (no third-party deps)
python3 -m unittest tests.test_subset_sum -v
# benchmarks -> docs/analysis/2026-10-03/subset-sum/
python3 scripts/analysis/benchmark.py
# figures + tables -> docs/reports/{figures,tables}/ (needs matplotlib)
uv run --with matplotlib python scripts/analysis/plot_benchmarks.py
```
