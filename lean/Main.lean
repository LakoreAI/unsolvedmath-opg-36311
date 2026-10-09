import SubsetSum

open SubsetSum

/-- A checked end-to-end decision pipeline for the reference MITM algorithm.

`meetInMiddle_correct` proves that this Boolean answers exactly `HasSum` for
the concatenated input blocks. This executable is deliberately a reference
demonstration, not a claim about the unproved sub-`2^(n/2)` research target.
-/
def demoDecision : Bool :=
  meetInMiddle [3, -2] [7, 0] 5

#eval demoDecision

def main : IO Unit := do
  IO.println s!"subset-sum demo: {demoDecision}"
