import SubsetSum.Reductions
import SubsetSum.SharedMask
import SubsetSum.HighEnergy

/-! # End-to-End Structural Audit of the October 2026 `O(2^(0.49n))` Preprint

Formalizes the deterministic structural stages of the October 4, 2026 manuscript
(*Subset Sum in Time O(2^(0.49n))*):
1. **High/Low-Digit Decomposition (`highDigits`, `lowDigits`):**
   Every subset sum decomposes linearly as
   `maskSum xs ms = base * maskSum (highDigits base xs) ms + maskSum (lowDigits base xs) ms`,
   supplying the exact algebraic identity behind the Section 4 filtered digit
   checksum.
2. **Capped Distinct-Sum Preliminary Search (`cappedPrelimSolve`):**
   When the number of distinct subset sums `|Σ(left)|` is at most `cap`, the
   preliminary solver decides `HasSum (left ++ right) b` exactly.
3. **End-to-End Isolated Alias-Subtraction Decision (`isolated_alias_decision_iff`):**
   Couples Stage 1 (tie-breaking isolation `isolateWeights`, `isolateTarget`),
   Stage 3/4 (modular bin and alias enumeration `modBinEntries`, `modBinAliases`),
   and Stage 5 (alias subtraction and thresholding `0 < aliasSubtractedCount`),
   proving that the 5-stage pipeline decides `HasSum xs b` without false
   positives or false negatives. -/
namespace SubsetSum

/-! ## High/low-digit decomposition (Section 4) -/

/-- High-digit quotients `a_i / base` of input weights. -/
def highDigits (base : Int) (xs : List Int) : List Int :=
  xs.map (· / base)

/-- Low-digit remainders `a_i % base` of input weights. -/
def lowDigits (base : Int) (xs : List Int) : List Int :=
  xs.map (· % base)

/-- Every subset sum splits into `base` times the high-digit subset sum plus
the low-digit subset sum. -/
theorem maskSum_high_low_split (base : Int) (xs : List Int) (ms : List Bool) :
    maskSum xs ms =
      base * maskSum (highDigits base xs) ms + maskSum (lowDigits base xs) ms := by
  induction xs generalizing ms with
  | nil => simp [highDigits, lowDigits, maskSum]
  | cons a xs ih =>
      cases ms with
      | nil => simp [highDigits, lowDigits, maskSum]
      | cons bit ms' =>
          cases bit
          · simp only [highDigits, lowDigits, List.map_cons, maskSum, ih ms']
          · simp only [highDigits, lowDigits, List.map_cons, maskSum, ih ms', Int.mul_add]
            have hdiv := Int.ediv_add_emod a base
            omega

/-! ## Capped distinct-sum preliminary search (Section 3) -/

/-- Preliminary search that decides `(left ++ right, b)` whenever the number of
distinct subset sums in `left` is at most `cap`, and returns `none` otherwise. -/
def cappedPrelimSolve (cap : Nat) (left right : List Int) (b : Int) : Option Bool :=
  let cs := coreSums left
  if cs.length ≤ cap then
    some (cs.any fun u => (sums right).contains (b - u))
  else
    none

theorem cappedPrelimSolve_sound {cap : Nat} {left right : List Int} {b : Int} {ans : Bool}
    (h : cappedPrelimSolve cap left right b = some ans) :
    ans = true ↔ HasSum (left ++ right) b := by
  simp only [cappedPrelimSolve] at h
  split at h
  · simp only [Option.some.injEq] at h
    subst h
    simp only [List.any_eq_true, List.contains_iff, mem_coreSums_iff, mem_sums_iff]
    rw [hasSum_append]
    constructor
    · rintro ⟨u, hu, hv⟩
      exact ⟨u, b - u, hu, hv, by omega⟩
    · rintro ⟨u, v, hu, hv, huv⟩
      have eq : b - u = v := by omega
      exact ⟨u, hu, by simpa [eq] using hv⟩
  · cases h

/-! ## Alias subtraction and thresholding (Sections 4–5) -/

/-- Modular bin count minus the modular alias count. -/
def aliasSubtractedCount (xs : List Int) (b p : Int) : Nat :=
  (modBinEntries xs b p).length - (modBinAliases xs b p).length

/-- Subtracting modular aliases from the modular bin leaves the exact count of
true target witnesses. -/
theorem aliasSubtractedCount_eq_trueHits (xs : List Int) (b p : Int) :
    aliasSubtractedCount xs b p = (modBinTrueHits xs b p).length := by
  have h := modBin_alias_subtraction xs b p
  simp only [aliasSubtractedCount]
  omega

/-- The alias-subtracted modular bin count is positive iff `HasSum xs b` holds. -/
theorem aliasSubtractedCount_pos_iff (xs : List Int) (b p : Int) :
    0 < aliasSubtractedCount xs b p ↔ HasSum xs b := by
  rw [aliasSubtractedCount_eq_trueHits, hasSum_iff_exists_mask]
  constructor
  · intro hpos
    cases hlist : modBinTrueHits xs b p with
    | nil =>
        rw [hlist, List.length_nil] at hpos
        cases hpos
    | cons head tail =>
        rcases head with ⟨s, ms⟩
        have hmem : (s, ms) ∈ modBinTrueHits xs b p := by
          rw [hlist]
          exact List.mem_cons_self
        rcases (mem_modBinTrueHits_iff xs b p s ms).mp hmem with ⟨_, hlen, hsum⟩
        exact ⟨ms, hlen, hsum⟩
  · rintro ⟨ms, hlen, hsum⟩
    have hmem : (b, ms) ∈ modBinTrueHits xs b p :=
      (mem_modBinTrueHits_iff xs b p b ms).mpr ⟨rfl, hlen, hsum⟩
    cases hlist : modBinTrueHits xs b p with
    | nil =>
        rw [hlist] at hmem
        cases hmem
    | cons _ _ =>
        simp

/-- End-to-end structural theorem for the October 2026 preprint pipeline:
For any instance `(xs, b)`, tie weights `us` with `us.sum < scale`, and modulus `p`,
`HasSum xs b` holds if and only if some isolated target `isolateTarget scale b s`
(`0 ≤ s ≤ us.sum`) has a positive alias-subtracted modular bin count. -/
theorem isolated_alias_decision_iff {scale b p : Int} {xs us : List Int}
    (hu : us.length = xs.length)
    (hnonneg : ∀ u ∈ us, 0 ≤ u)
    (hscale : us.sum < scale) :
    HasSum xs b ↔
      ∃ s : Int, 0 ≤ s ∧ s ≤ us.sum ∧
        0 < aliasSubtractedCount (isolateWeights scale xs us) (isolateTarget scale b s) p := by
  rw [isolation_hasSum_iff hu hnonneg hscale]
  constructor
  · rintro ⟨s, hlo, hhi, hsum⟩
    exact ⟨s, hlo, hhi, (aliasSubtractedCount_pos_iff _ _ p).mpr hsum⟩
  · rintro ⟨s, hlo, hhi, hpos⟩
    exact ⟨s, hlo, hhi, (aliasSubtractedCount_pos_iff _ _ p).mp hpos⟩

end SubsetSum
