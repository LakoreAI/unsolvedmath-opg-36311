# Literature update — 2026-10-09

## Status-changing claim to audit

OpenAI's mathematics collection, released on 2026-10-06, includes a manuscript
dated 2026-10-04 titled *Subset Sum in Time O(2^(0.49n))*. Its stated result is
a uniform randomized classical decision algorithm for polynomial-bit word-RAM
inputs with bounded error and worst-case `O(2^(0.49n))` time. If correct, this
supersedes the repository's former statement that no constant-exponent
improvement on `2^(n/2)` was known.

This repository must treat the result as **unreviewed until independently
checked**. The publisher describes the collection as containing results at
different stages of verification and says that not every manuscript has a Lean
formalization.

- [OpenAI release](https://openai.com/index/sharing-ai-progress-in-mathematics/)
- [Official manuscript collection](https://github.com/openai/math)

## Audit completed on 2026-10-09

The exact primary artifact is
[`preprints/Subset-Sum-in-Time-2-power-0-49n-October-4-2026/subset-sum.pdf`](https://github.com/openai/math/blob/main/preprints/Subset-Sum-in-Time-2-power-0-49n-October-4-2026/subset-sum.pdf),
published in the collection's initial commit on 2026-10-06. Its Theorem 1.1
states a **uniform randomized classical decision algorithm** for positive
integer Subset Sum. It works for repeated inputs, permits the empty subset,
uses word length `ceil(4(n+b+log2(n+2)))`, has success probability at least
`2/3` on every input, and for each fixed `c>0` has a `C_c 2^(0.49n)` bound on
every execution when `b <= n^c`. The manuscript gives the stronger intermediate
bound `2^(0.489995n) poly(n+b+2)`.

This is not a result for this repository's signed-integer API without a
reduction, and it is not a witness-recovery theorem as stated. The official
Lean catalog has no entry for this manuscript, so there is currently no linked
formalization artifact.

The proof pipeline is materially different from HGJ/BCJ. It: (1) isolates a
solution using tie-breaking weights and polynomially many transformed targets;
(2) runs a capped distinct-sum preliminary search; (3) estimates each modular
target bin via a filtered high/low-digit Fourier checksum; (4) enumerates only
the modular aliases through shared-block records and disjoint-mask
compatibility; and (5) subtracts aliases from the checksum. Section 3 fixes
filter parameters and Appendix A provides a finite arithmetic certificate. The
core randomized pieces include prime sampling, random phases, random filtering
tables, random restrictions, and capped match sampling.

The former Python small-instance model was removed in the Lean-first migration.
The current checked executable pipeline covers the proved reference
meet-in-the-middle decision procedure only. A Lean formalization of the
isolation family, shared-mask compatibility, estimator, filter tables, alias
sampler, numerical certificate, and word-RAM implementation remains necessary
before any end-to-end claim about this preprint.

## Next audit work

1. Independently reproduce Theorems 4.1 and 5.1 on small instances, including
   every failure cap and the false-positive alias subtraction.
2. Audit the filtering-moment inequalities and Appendix A's rational interval
   certificate separately from the algorithmic implementation.
3. Prove an explicit positive-to-signed reduction before exposing the result
   through the repository's signed-integer API.
4. Replace the survey's old worst-case landscape only after an independent
   end-to-end review establishes the theorem's stated scope.

## Work that remains useful

The PESS close-pair reduction remains a useful neighboring result and is now
implemented as a reference component. The BCJ port remains valuable as an
average-case benchmark, but it no longer has priority over auditing the claimed
worst-case breakthrough. The all-three-block reduction remains useful only if
it can exploit a compatibility relation that does not materialize pairwise
sumsets.

## Other primary sources checked

- [Jin, Williams, Zhang, ESA 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2025.86): gives randomized `O*(2^(n/3))` PESS via
  close pairs and a high-collision ESS subroutine.
- [Randolph, Węgrzycki, arXiv:2511.10823](https://arxiv.org/abs/2511.10823):
  obtains worst-case improvements for many coefficient sets but leaves the
  binary and Partition cases outside its result.
- [Becker, Coron, Joux](https://eprint.iacr.org/2011/474): documents the
  average-case eight-list BCJ construction and its `0.291n` model.
