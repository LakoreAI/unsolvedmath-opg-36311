import SubsetSum

open SubsetSum

/-- Checked end-to-end decision and witness pipeline for the reference
algorithms in `SubsetSum`.

- `meetInMiddle_correct` and `meetInMiddleWitness_sound` verify two-block MITM.
- `threeBlock_correct` and `sharedMaskSolve_sound` verify three-block 3SUM and
  shared-mask compatibility.
- `modBin_alias_subtraction` verifies modular bin alias cancellation.
This executable is a reference demonstration, not a claim about the unproved
sub-`2^(n/2)` worst-case research target. -/
def demoDecision : Bool :=
  meetInMiddle [3, -2] [7, 0] 5

def demoWitness : Option (List Bool) :=
  meetInMiddleWitness [3, -2] [7, 0] 5

def demoSharedMask : Option (List Bool) :=
  sharedMaskSolve [3] [-2, 7] [0] 5

def demoAliasCounts : Nat × Nat × Nat :=
  let xs := [3, -2, 7, 0]
  let b := 5
  let p := 3
  ((modBinEntries xs b p).length,
   (modBinAliases xs b p).length,
   (modBinTrueHits xs b p).length)

def demoCompressMitm : Bool :=
  compressMitm [1, 2, 3] [10] [20] 16

def demoHgj : Option (List Bool) :=
  hgjSolve [3, 5, 8, 13, 21, 34] 2 6 66 0

def demoCappedPrelim : Option Bool :=
  cappedPrelimSolve 8 [1, 2, 3] [10, 20] 16

def demoFlip : Int × Int :=
  let xs := [3, -2, 7, 0]
  let fs := [true, false, true, false]
  (maskSum (flipWeights fs xs) (xorMask [true, true, false, false] fs), 1 - maskSum xs fs)

def demoFilterMoments : Float × Float × Float :=
  let t := Audit049Filter.filterTable 64
  (t.moment1, t.moment2, Audit049Filter.threshold)

#eval demoDecision
#eval demoWitness
#eval demoSharedMask
#eval demoAliasCounts
#eval demoCompressMitm
#eval demoHgj
#eval demoCappedPrelim
#eval demoFlip
#eval demoFilterMoments

def main : IO Unit := do
  IO.println s!"subset-sum decision: {demoDecision}"
  IO.println s!"subset-sum witness:  {repr demoWitness}"
  IO.println s!"shared-mask witness: {repr demoSharedMask}"
  IO.println s!"modular bin (total, aliases, true): {repr demoAliasCounts}"
  IO.println s!"compressible-core MITM: {demoCompressMitm}"
  IO.println s!"HGJ witness: {repr demoHgj}"
  IO.println s!"capped preliminary search: {repr demoCappedPrelim}"
  IO.println s!"flip (signed sum, a(I) - a(F)): {repr demoFlip}"
  IO.println s!"Prop. 3.1 moments (T64, T64', 2^0.5168): {demoFilterMoments}"
