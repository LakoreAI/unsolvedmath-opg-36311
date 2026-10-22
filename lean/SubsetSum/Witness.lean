import SubsetSum.Basic

/-! # Occurrence-Witness Semantics and Witness-Returning MITM

Equal values at different list positions are distinct selectable occurrences.
A Boolean mask `ms : List Bool` of length `xs.length` records which occurrences
are selected, and `meetInMiddleWitness` recovers an explicit witness mask. -/
namespace SubsetSum

/-- Sum of the occurrences in `xs` selected by a Boolean mask `ms`. -/
def maskSum : List Int → List Bool → Int
  | [], _ => 0
  | a :: xs, ms =>
      match ms with
      | [] => 0
      | false :: ms' => maskSum xs ms'
      | true :: ms' => a + maskSum xs ms'

theorem maskSum_nil_left (ms : List Bool) : maskSum [] ms = 0 := rfl

theorem maskSum_nil_right (xs : List Int) : maskSum xs [] = 0 := by
  cases xs <;> rfl

theorem maskSum_sound {xs : List Int} {ms : List Bool}
    (hlen : ms.length = xs.length) : HasSum xs (maskSum xs ms) := by
  induction xs generalizing ms with
  | nil =>
      rw [maskSum_nil_left]
      exact HasSum.nil
  | cons a xs ih =>
      cases ms with
      | nil => cases hlen
      | cons bit ms' =>
          have hlen' := Nat.succ.inj hlen
          cases bit with
          | false =>
              simp only [maskSum]
              exact HasSum.skip (ih hlen')
          | true =>
              simp only [maskSum]
              exact HasSum.take (ih hlen')

theorem hasSum_iff_exists_mask (xs : List Int) (b : Int) :
    HasSum xs b ↔ ∃ ms : List Bool, ms.length = xs.length ∧ maskSum xs ms = b := by
  constructor
  · intro h
    induction h with
    | nil => exact ⟨[], rfl, rfl⟩
    | skip _ ih =>
        rcases ih with ⟨ms, hlen, hsum⟩
        exact ⟨false :: ms, by simp [hlen], by simpa [maskSum] using hsum⟩
    | take _ ih =>
        rcases ih with ⟨ms, hlen, hsum⟩
        exact ⟨true :: ms, by simp [hlen], by simp [maskSum, hsum]⟩
  · rintro ⟨ms, hlen, rfl⟩
    exact maskSum_sound hlen

theorem maskSum_append (left right : List Int) (ml mr : List Bool)
    (hl : ml.length = left.length) :
    maskSum (left ++ right) (ml ++ mr) = maskSum left ml + maskSum right mr := by
  induction left generalizing ml with
  | nil =>
      cases ml with
      | nil => simp [maskSum]
      | cons _ _ => cases hl
  | cons a xs ih =>
      cases ml with
      | nil => cases hl
      | cons bit ms =>
          have hl' := Nat.succ.inj hl
          cases bit <;> simp only [List.cons_append, maskSum, ih ms hl'] <;> omega

/-- Exhaustive enumeration of `(sum, mask)` pairs for a block. -/
def sumMasks : List Int → List (Int × List Bool)
  | [] => [(0, [])]
  | a :: xs =>
      (sumMasks xs).map (fun p => (p.1, false :: p.2)) ++
      (sumMasks xs).map (fun p => (a + p.1, true :: p.2))

theorem mem_sumMasks_iff (xs : List Int) (b : Int) (ms : List Bool) :
    (b, ms) ∈ sumMasks xs ↔ ms.length = xs.length ∧ maskSum xs ms = b := by
  induction xs generalizing b ms with
  | nil =>
      simp only [sumMasks, List.mem_singleton, Prod.ext_iff, List.length_nil]
      constructor
      · rintro ⟨rfl, rfl⟩
        exact ⟨rfl, rfl⟩
      · rintro ⟨hlen, hsum⟩
        have hms : ms = [] := List.eq_nil_of_length_eq_zero hlen
        subst hms
        exact ⟨hsum.symm, rfl⟩
  | cons a xs ih =>
      simp only [sumMasks, List.mem_append, List.mem_map, Prod.exists, Prod.ext_iff]
      constructor
      · rintro (⟨s, ms', hmem, rfl, rfl⟩ | ⟨s, ms', hmem, rfl, rfl⟩)
        · rcases (ih s ms').mp hmem with ⟨hlen, hsum⟩
          exact ⟨by simp [hlen], by simpa [maskSum] using hsum⟩
        · rcases (ih s ms').mp hmem with ⟨hlen, hsum⟩
          exact ⟨by simp [hlen], by simp [maskSum, hsum]⟩
      · rintro ⟨hlen, hsum⟩
        cases ms with
        | nil => cases hlen
        | cons bit ms' =>
            have hlen' := Nat.succ.inj hlen
            cases bit with
            | false =>
                left
                simp only [maskSum] at hsum
                exact ⟨b, ms', (ih b ms').mpr ⟨hlen', hsum⟩, rfl, rfl⟩
            | true =>
                right
                simp only [maskSum] at hsum
                refine ⟨b - a, ms', (ih (b - a) ms').mpr ⟨hlen', by omega⟩, by omega, rfl⟩

/-- All combined witness masks produced by matching left and right sum tables. -/
def meetInMiddlePairs (left right : List Int) (b : Int) : List (List Bool) :=
  (sumMasks left).flatMap fun p =>
    ((sumMasks right).filter fun q => p.1 + q.1 == b).map fun q => p.2 ++ q.2

theorem mem_meetInMiddlePairs_iff (left right : List Int) (b : Int) (ms : List Bool) :
    ms ∈ meetInMiddlePairs left right b ↔
      ∃ u ml v mr, (u, ml) ∈ sumMasks left ∧ (v, mr) ∈ sumMasks right ∧
        u + v = b ∧ ml ++ mr = ms := by
  simp only [meetInMiddlePairs, List.mem_flatMap, List.mem_map, List.mem_filter,
    Prod.exists, beq_iff_eq]
  constructor
  · rintro ⟨u, ml, hL, v, mr, ⟨hR, huv⟩, hms⟩
    exact ⟨u, ml, v, mr, hL, hR, huv, hms⟩
  · rintro ⟨u, ml, v, mr, hL, hR, huv, hms⟩
    exact ⟨u, ml, hL, v, mr, ⟨hR, huv⟩, hms⟩

/-- Executable witness-returning meet-in-the-middle solver. -/
def meetInMiddleWitness (left right : List Int) (b : Int) : Option (List Bool) :=
  (meetInMiddlePairs left right b).head?

theorem meetInMiddleWitness_sound {left right : List Int} {b : Int} {ms : List Bool}
    (h : meetInMiddleWitness left right b = some ms) :
    ms.length = (left ++ right).length ∧ maskSum (left ++ right) ms = b := by
  have hmem : ms ∈ meetInMiddlePairs left right b := by
    cases hlist : meetInMiddlePairs left right b with
    | nil =>
        rw [meetInMiddleWitness, hlist] at h
        cases h
    | cons x xs =>
        simp only [meetInMiddleWitness, hlist, List.head?_cons, Option.some.injEq] at h
        subst h
        exact List.mem_cons_self
  rcases (mem_meetInMiddlePairs_iff left right b ms).mp hmem with
    ⟨u, ml, v, mr, hL, hR, huv, rfl⟩
  rcases (mem_sumMasks_iff left u ml).mp hL with ⟨hlenL, hsumL⟩
  rcases (mem_sumMasks_iff right v mr).mp hR with ⟨hlenR, hsumR⟩
  refine ⟨?_, ?_⟩
  · simp [List.length_append, hlenL, hlenR]
  · rw [maskSum_append left right ml mr hlenL, hsumL, hsumR, huv]

theorem meetInMiddleWitness_hasSum {left right : List Int} {b : Int} {ms : List Bool}
    (h : meetInMiddleWitness left right b = some ms) :
    HasSum (left ++ right) b := by
  rcases meetInMiddleWitness_sound h with ⟨hlen, hsum⟩
  exact (hasSum_iff_exists_mask (left ++ right) b).mpr ⟨ms, hlen, hsum⟩

theorem meetInMiddleWitness_isSome_iff (left right : List Int) (b : Int) :
    (meetInMiddleWitness left right b).isSome = true ↔ HasSum (left ++ right) b := by
  constructor
  · intro h
    rcases Option.isSome_iff_exists.mp h with ⟨ms, hms⟩
    exact meetInMiddleWitness_hasSum hms
  · intro h
    rw [hasSum_append] at h
    rcases h with ⟨u, v, hu, hv, huv⟩
    rcases (hasSum_iff_exists_mask left u).mp hu with ⟨ml, hlenL, hsumL⟩
    rcases (hasSum_iff_exists_mask right v).mp hv with ⟨mr, hlenR, hsumR⟩
    have hmem : ml ++ mr ∈ meetInMiddlePairs left right b :=
      (mem_meetInMiddlePairs_iff left right b (ml ++ mr)).mpr
        ⟨u, ml, v, mr, (mem_sumMasks_iff left u ml).mpr ⟨hlenL, hsumL⟩,
          (mem_sumMasks_iff right v mr).mpr ⟨hlenR, hsumR⟩, huv, rfl⟩
    cases hlist : meetInMiddlePairs left right b with
    | nil =>
        rw [hlist] at hmem
        cases hmem
    | cons _ _ => simp [meetInMiddleWitness, hlist]

end SubsetSum
