# Lean-first development

The authoritative algorithms and correctness claims in this repository belong
in `lean/`. This repository contains no Python implementation.

## Workflow

- Express a new algorithmic stage as an executable Lean definition and state
  its correctness relation to `SubsetSum.HasSum` before adding optimizations.
- Keep theorem statements explicit about input domain, decision versus witness
  output, randomness, and resource model. Do not assign an asymptotic bound to
  a demo unless it has been formalized.
- Use `cd lean && lake build` to check proofs and
  `cd lean && lake env lean Main.lean` to evaluate the end-to-end demo.
- Preserve occurrence semantics: equal values at different list positions are
  distinct selectable items.
- Update `README.md` whenever an executable or its supported theorem changes.

The checked executable pipeline is the project entrypoint. Historical
measurements and reports under `docs/` are evidence records, not runnable
implementations.
