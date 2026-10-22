import SubsetSum.Witness

/-! # Disjoint-Mask Compatibility, Shared-Block 3-Split, and Modular Alias Subtraction

Formalizes:
1. Disjoint Boolean mask union (`masksDisjoint`, `orMask`) and additive sum
   preservation (`maskSum_orMask_of_disjoint`).
2. The shared-block 3-split compatibility solver (`SharedMaskRecord`,
   `sharedMaskRecords`, `sharedMaskSolve`) from Section 5 of the October 2026
   preprint.
3. Exact modular bin decomposition (`modBinRecords`, `modBinAliases`,
   `modBinTrueHits`) proving that every modular bin hit is either a true target
   solution or a nonzero integer discrepancy (modular alias), so subtracting
   aliases recovers the exact solution count in the bin. -/
namespace SubsetSum

/-- Two Boolean masks of equal length are disjoint if they never both select `true`. -/
def masksDisjoint : List Bool → List Bool → Bool
  | [], m2 =>
      match m2 with
      | [] => true
      | _ :: _ => false
  | b1 :: m1, m2 =>
      match m2 with
      | [] => false
      | b2 :: m2' => (!(b1 && b2)) && masksDisjoint m1 m2'

/-- Pointwise Boolean union of two masks. -/
def orMask : List Bool → List Bool → List Bool
  | [], _ => []
  | b1 :: m1, m2 =>
      match m2 with
      | [] => []
      | b2 :: m2' => (b1 || b2) :: orMask m1 m2'

theorem orMask_length {m1 m2 : List Bool} (h : m1.length = m2.length) :
    (orMask m1 m2).length = m1.length := by
  induction m1 generalizing m2 with
  | nil =>
      cases m2 with
      | nil => rfl
      | cons _ _ => cases h
  | cons b1 m1 ih =>
      cases m2 with
      | nil => cases h
      | cons b2 m2' =>
          have h' := Nat.succ.inj h
          simp [orMask, ih h']

/-- If two masks on `xs` are disjoint, the sum of their pointwise union equals
the sum of their individual subset sums (`y + z ∈ {0,1}^n`). -/
theorem maskSum_orMask_of_disjoint (xs : List Int) (m1 m2 : List Bool)
    (h1 : m1.length = xs.length) (h2 : m2.length = xs.length)
    (hdisj : masksDisjoint m1 m2 = true) :
    maskSum xs (orMask m1 m2) = maskSum xs m1 + maskSum xs m2 := by
  induction xs generalizing m1 m2 with
  | nil =>
      cases m1 with
      | nil =>
          cases m2 with
          | nil => rfl
          | cons _ _ => cases h2
      | cons _ _ => cases h1
  | cons a xs ih =>
      cases m1 with
      | nil => cases h1
      | cons b1 m1' =>
          cases m2 with
          | nil => cases h2
          | cons b2 m2' =>
              have h1' := Nat.succ.inj h1
              have h2' := Nat.succ.inj h2
              simp only [masksDisjoint, Bool.and_eq_true] at hdisj
              have hrec := ih m1' m2' h1' h2' hdisj.2
              cases b1 <;> cases b2
              · simp only [orMask, Bool.or_false, maskSum, hrec]
              · simp only [orMask, Bool.false_or, maskSum, hrec]
                omega
              · simp only [orMask, Bool.true_or, maskSum, hrec]
                omega
              · exact False.elim (by cases hdisj.1)

/-- An all-`false` mask of the same length as `xs`. -/
def zeroMask : List Int → List Bool
  | [] => []
  | _ :: xs => false :: zeroMask xs

theorem zeroMask_length (xs : List Int) : (zeroMask xs).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons _ xs ih => simp [zeroMask, ih]

theorem maskSum_zeroMask (xs : List Int) : maskSum xs (zeroMask xs) = 0 := by
  induction xs with
  | nil => rfl
  | cons _ xs ih => simp [zeroMask, maskSum, ih]

theorem masksDisjoint_zeroMask_right (xs : List Int) (ms : List Bool)
    (hlen : ms.length = xs.length) :
    masksDisjoint ms (zeroMask xs) = true := by
  induction xs generalizing ms with
  | nil =>
      cases ms with
      | nil => rfl
      | cons _ _ => cases hlen
  | cons _ xs ih =>
      cases ms with
      | nil => cases hlen
      | cons bit ms' =>
          have hlen' := Nat.succ.inj hlen
          simp [zeroMask, masksDisjoint, ih ms' hlen']

/-- A partial record selecting a mask on one side block and a mask on the shared block. -/
structure SharedMaskRecord where
  sideMask : List Bool
  sharedMask : List Bool
  total : Int
  deriving Repr, DecidableEq

/-- Enumerate all unfiltered `(sideMask, sharedMask, total)` records for one side. -/
def sharedMaskRecords (side shared : List Int) : List SharedMaskRecord :=
  (sumMasks side).flatMap fun p =>
    (sumMasks shared).map fun q =>
      { sideMask := p.2, sharedMask := q.2, total := p.1 + q.1 }

theorem mem_sharedMaskRecords_iff (side shared : List Int) (r : SharedMaskRecord) :
    r ∈ sharedMaskRecords side shared ↔
      r.sideMask.length = side.length ∧
      r.sharedMask.length = shared.length ∧
      maskSum side r.sideMask + maskSum shared r.sharedMask = r.total := by
  simp only [sharedMaskRecords, List.mem_flatMap, List.mem_map, Prod.exists]
  constructor
  · rintro ⟨u, mSide, hSide, v, mShared, hShared, rfl⟩
    rcases (mem_sumMasks_iff side u mSide).mp hSide with ⟨hl1, hs1⟩
    rcases (mem_sumMasks_iff shared v mShared).mp hShared with ⟨hl2, hs2⟩
    exact ⟨hl1, hl2, by simp [hs1, hs2]⟩
  · rintro ⟨hl1, hl2, htot⟩
    refine ⟨maskSum side r.sideMask, r.sideMask,
      (mem_sumMasks_iff side _ _).mpr ⟨hl1, rfl⟩,
      maskSum shared r.sharedMask, r.sharedMask,
      (mem_sumMasks_iff shared _ _).mpr ⟨hl2, rfl⟩, ?_⟩
    cases r
    simp only [SharedMaskRecord.mk.injEq, true_and]
    exact htot

/-- Compatible witness masks across `(left, shared, right)` formed by pairing a
left record and a right record with disjoint shared masks. -/
def sharedMaskPairs (left shared right : List Int) (b : Int) : List (List Bool) :=
  (sharedMaskRecords left shared).flatMap fun rL =>
    ((sharedMaskRecords right shared).filter fun rR =>
      (rL.total + rR.total == b) && masksDisjoint rL.sharedMask rR.sharedMask).map fun rR =>
      (rL.sideMask ++ orMask rL.sharedMask rR.sharedMask) ++ rR.sideMask

/-- Executable 3-block solver using shared-mask compatibility. -/
def sharedMaskSolve (left shared right : List Int) (b : Int) : Option (List Bool) :=
  (sharedMaskPairs left shared right b).head?

theorem sharedMaskSolve_sound {left shared right : List Int} {b : Int} {ms : List Bool}
    (h : sharedMaskSolve left shared right b = some ms) :
    ms.length = ((left ++ shared) ++ right).length ∧
      maskSum ((left ++ shared) ++ right) ms = b := by
  have hmem : ms ∈ sharedMaskPairs left shared right b := by
    cases hlist : sharedMaskPairs left shared right b with
    | nil =>
        rw [sharedMaskSolve, hlist] at h
        cases h
    | cons x xs =>
        simp only [sharedMaskSolve, hlist, List.head?_cons, Option.some.injEq] at h
        subst h
        exact List.mem_cons_self
  simp only [sharedMaskPairs, List.mem_flatMap, List.mem_map, List.mem_filter,
    Bool.and_eq_true, beq_iff_eq] at hmem
  rcases hmem with ⟨rL, hrL, rR, ⟨hrR, htot, hdisj⟩, rfl⟩
  rcases (mem_sharedMaskRecords_iff left shared rL).mp hrL with ⟨hlL, hlSL, hsumL⟩
  rcases (mem_sharedMaskRecords_iff right shared rR).mp hrR with ⟨hlR, hlSR, hsumR⟩
  have hlOr : (orMask rL.sharedMask rR.sharedMask).length = shared.length := by
    rw [orMask_length (hlSL.trans hlSR.symm), hlSL]
  have hlLeftShared :
      (rL.sideMask ++ orMask rL.sharedMask rR.sharedMask).length =
        (left ++ shared).length := by
    simp [List.length_append, hlL, hlOr]
  refine ⟨?_, ?_⟩
  · simp [List.length_append, hlL, hlOr, hlR]
  · rw [maskSum_append (left ++ shared) right _ rR.sideMask hlLeftShared,
      maskSum_append left shared rL.sideMask _ hlL,
      maskSum_orMask_of_disjoint shared rL.sharedMask rR.sharedMask hlSL hlSR hdisj]
    omega

theorem sharedMaskSolve_isSome_iff (left shared right : List Int) (b : Int) :
    (sharedMaskSolve left shared right b).isSome = true ↔
      HasSum ((left ++ shared) ++ right) b := by
  constructor
  · intro h
    rcases Option.isSome_iff_exists.mp h with ⟨ms, hms⟩
    rcases sharedMaskSolve_sound hms with ⟨hlen, hsum⟩
    exact (hasSum_iff_exists_mask ((left ++ shared) ++ right) b).mpr ⟨ms, hlen, hsum⟩
  · intro h
    rcases (hasSum_append3 left shared right b).mp h with ⟨x, y, z, hx, hy, hz, hxyz⟩
    rcases (hasSum_iff_exists_mask left x).mp hx with ⟨mL, hlL, hsL⟩
    rcases (hasSum_iff_exists_mask shared y).mp hy with ⟨mS, hlS, hsS⟩
    rcases (hasSum_iff_exists_mask right z).mp hz with ⟨mR, hlR, hsR⟩
    let rL : SharedMaskRecord := { sideMask := mL, sharedMask := mS, total := x + y }
    let rR : SharedMaskRecord := { sideMask := mR, sharedMask := zeroMask shared, total := z }
    have hrL : rL ∈ sharedMaskRecords left shared :=
      (mem_sharedMaskRecords_iff left shared rL).mpr ⟨hlL, hlS, by simp [rL, hsL, hsS]⟩
    have hrR : rR ∈ sharedMaskRecords right shared :=
      (mem_sharedMaskRecords_iff right shared rR).mpr
        ⟨hlR, zeroMask_length shared, by simp [rR, hsR, maskSum_zeroMask]⟩
    have hdisj : masksDisjoint rL.sharedMask rR.sharedMask = true :=
      masksDisjoint_zeroMask_right shared mS hlS
    have hmem : (rL.sideMask ++ orMask rL.sharedMask rR.sharedMask) ++ rR.sideMask ∈
        sharedMaskPairs left shared right b := by
      simp only [sharedMaskPairs, List.mem_flatMap, List.mem_map, List.mem_filter,
        Bool.and_eq_true, beq_iff_eq]
      exact ⟨rL, hrL, rR, ⟨hrR, by simp [rL, rR]; omega, hdisj⟩, rfl⟩
    cases hlist : sharedMaskPairs left shared right b with
    | nil =>
        rw [hlist] at hmem
        cases hmem
    | cons _ _ => simp [sharedMaskSolve, hlist]

/-! ## Modular bin checksum and alias subtraction (Track B)

In the October 2026 preprint's pipeline, a modular target bin `(s - b) % p = 0`
collects both true solutions (`s = b`) and modular false positives (`s ≠ b` with
`p ∣ s - b`, called *aliases*). Subtracting the alias count from the total modular
bin count leaves the exact count of true target solutions. -/

/-- All `(sum, mask)` entries falling into the modular target bin `(s - b) % p == 0`. -/
def modBinEntries (xs : List Int) (b p : Int) : List (Int × List Bool) :=
  (sumMasks xs).filter fun q => (q.1 - b) % p == 0

/-- True target witnesses `(s == b)` inside the modular bin. -/
def modBinTrueHits (xs : List Int) (b p : Int) : List (Int × List Bool) :=
  (modBinEntries xs b p).filter fun q => q.1 == b

/-- Modular false positives (`s != b` but `(s - b) % p == 0`) inside the modular bin. -/
def modBinAliases (xs : List Int) (b p : Int) : List (Int × List Bool) :=
  (modBinEntries xs b p).filter fun q => q.1 != b

theorem filter_compl_length {α : Type} (p : α → Bool) (l : List α) :
    (l.filter p).length + (l.filter (fun x => !p x)).length = l.length := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      cases hp : p x <;> simp [List.filter_cons, hp, ← ih] <;> omega

/-- Exact alias-subtraction identity: the number of true target witnesses in the
modular bin equals the modular bin count minus the modular alias count. -/
theorem modBin_alias_subtraction (xs : List Int) (b p : Int) :
    (modBinTrueHits xs b p).length + (modBinAliases xs b p).length =
      (modBinEntries xs b p).length := by
  simp only [modBinTrueHits, modBinAliases]
  have hfun : (fun q : Int × List Bool => q.1 != b) = (fun q => !(q.1 == b)) := by
    funext q
    simp [bne]
  rw [hfun]
  exact filter_compl_length (fun q => q.1 == b) (modBinEntries xs b p)

/-- Every true target witness `(b, ms)` lies in `modBinTrueHits xs b p`. -/
theorem mem_modBinTrueHits_iff (xs : List Int) (b p : Int) (s : Int) (ms : List Bool) :
    (s, ms) ∈ modBinTrueHits xs b p ↔
      s = b ∧ ms.length = xs.length ∧ maskSum xs ms = b := by
  simp only [modBinTrueHits, modBinEntries, List.mem_filter, beq_iff_eq,
    mem_sumMasks_iff]
  constructor
  · rintro ⟨⟨⟨hlen, hsum⟩, _⟩, rfl⟩
    exact ⟨rfl, hlen, hsum⟩
  · rintro ⟨rfl, hlen, hsum⟩
    exact ⟨⟨⟨hlen, hsum⟩, by simp⟩, rfl⟩

end SubsetSum
