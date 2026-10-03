# Research

**Question.** Does general signed-integer subset sum admit a worst-case
`O*(2^(n/3))` algorithm, as requested by OPG-36311?

**Why it matters.** This asks for a constant improvement in the exponent of
exact worst-case subset-sum algorithms. Average-case and heuristic bounds do
not answer the universal worst-case question.

## Scope

- **In scope:** exact signed-integer solvers, correctness in Lean 4, independent
  Python checks, mathematical complexity analysis, reproducible measurements,
  and a literature-grounded research program.
- **Out of scope:** treating finite experiments or heuristic/random-instance
  results as a proof of the unrestricted bound.

## Method

Establish independent selection semantics in Lean and verify enumeration and
split correctness. Compare Python witness solvers against exhaustive Boolean
selection enumeration. Implement and measure the standard baselines
(meet-in-the-middle, Schroeppel-Shamir, signed DP, Equal-Subset-Sum, Wagner
dissection, Howgrave-Graham-Joux representation) and probe the structural
hypotheses about the barrier with additive-combinatorics quantities. A
resolution requires a worst-case argument for every allowed input; that remains
unproved.

## Results

- Baselines paper (correctness, implementations, measurements, bounded-magnitude
  theorem): [source](reports/baselines/paper.tex),
  [PDF](reports/baselines/paper.pdf).
- Representation paper (reproduced HGJ/BCJ exponents, frontier):
  [source](reports/representation/representation.tex),
  [PDF](reports/representation/representation.pdf).
- Survey (structured map of the field):
  [source](reports/survey/survey.tex), [PDF](reports/survey/survey.pdf).
- [Validation](reports/validation.md).
- Measured outputs: [`analysis/2026-10-03/subset-sum/`](analysis/2026-10-03/subset-sum/).
- Deep-research program and roadmap toward the open bound:
  [`research/subset-sum-n3/`](research/subset-sum-n3/) — `report.md` (20 sourced
  approach items), `PLAN.md`, and `PHASE1.md`.
