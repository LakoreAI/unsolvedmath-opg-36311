import SubsetSum.Witness

/-! # Signed-to-Positive and Tie-Breaking Isolation Reductions

Formalizes:
1. The signed-to-nonnegative and strictly positive weight reductions
   (`absWeights`, `negOffset`, `flipNegMask`, `nonZeroWeights`), proving a
   bijective correspondence between witnesses.
2. The tie-breaking isolation family (`isolateWeights`, `isolateTarget`),
   proving that a large scale `scale > us.sum` partitions solutions by their tie
   sum `maskSum us ms = s` without false positives. -/
namespace SubsetSum

/-! ## Signed-to-nonnegative and positive-weight reduction -/

/-- Nonnegative weights obtained by negating negative entries. -/
def absWeights : List Int → List Int
  | [] => []
  | a :: xs => (if a < 0 then -a else a) :: absWeights xs

/-- Target shift accumulating `-a` for every negative entry `a < 0`. -/
def negOffset : List Int → Int
  | [] => 0
  | a :: xs => (if a < 0 then -a else 0) + negOffset xs

/-- Bijective witness map complementing the selection bit at negative entries. -/
def flipNegMask : List Int → List Bool → List Bool
  | [], _ => []
  | a :: xs, ms =>
      match ms with
      | [] => []
      | bit :: ms' => (if a < 0 then !bit else bit) :: flipNegMask xs ms'

theorem absWeights_length (xs : List Int) :
    (absWeights xs).length = xs.length := by
  induction xs with
  | nil => rfl
  | cons a xs ih => simp [absWeights, ih]

theorem absWeights_nonneg {xs : List Int} {x : Int} (hx : x ∈ absWeights xs) :
    0 ≤ x := by
  induction xs with
  | nil => simp [absWeights] at hx
  | cons a xs ih =>
      simp only [absWeights, List.mem_cons] at hx
      rcases hx with rfl | hx
      · split <;> omega
      · exact ih hx

theorem flipNegMask_length (xs : List Int) (ms : List Bool)
    (hlen : ms.length = xs.length) :
    (flipNegMask xs ms).length = xs.length := by
  induction xs generalizing ms with
  | nil => rfl
  | cons a xs ih =>
      cases ms with
      | nil => cases hlen
      | cons bit ms' =>
          have hlen' := Nat.succ.inj hlen
          simp [flipNegMask, ih ms' hlen']

theorem flipNegMask_involutive (xs : List Int) (ms : List Bool)
    (hlen : ms.length = xs.length) :
    flipNegMask xs (flipNegMask xs ms) = ms := by
  induction xs generalizing ms with
  | nil =>
      cases ms with
      | nil => rfl
      | cons _ _ => cases hlen
  | cons a xs ih =>
      cases ms with
      | nil => cases hlen
      | cons bit ms' =>
          have hlen' := Nat.succ.inj hlen
          simp only [flipNegMask, ih ms' hlen', List.cons.injEq, and_true]
          split
          · exact Bool.not_not bit
          · rfl

theorem maskSum_absWeights (xs : List Int) (ms : List Bool)
    (hlen : ms.length = xs.length) :
    maskSum (absWeights xs) (flipNegMask xs ms) = maskSum xs ms + negOffset xs := by
  induction xs generalizing ms with
  | nil =>
      cases ms with
      | nil => rfl
      | cons _ _ => cases hlen
  | cons a xs ih =>
      cases ms with
      | nil => cases hlen
      | cons bit ms' =>
          have hlen' := Nat.succ.inj hlen
          have hrec := ih ms' hlen'
          by_cases ha : a < 0
          · cases bit <;>
              simp only [absWeights, flipNegMask, negOffset, ha, ↓reduceIte,
                Bool.not_false, Bool.not_true, maskSum, hrec] <;> omega
          · cases bit <;>
              simp only [absWeights, flipNegMask, negOffset, ha, ↓reduceIte,
                maskSum, hrec] <;> omega

theorem hasSum_signed_iff_nonneg (xs : List Int) (b : Int) :
    HasSum xs b ↔ HasSum (absWeights xs) (b + negOffset xs) := by
  rw [hasSum_iff_exists_mask, hasSum_iff_exists_mask]
  constructor
  · rintro ⟨ms, hlen, hsum⟩
    refine ⟨flipNegMask xs ms, ?_, ?_⟩
    · rw [flipNegMask_length xs ms hlen, absWeights_length]
    · rw [maskSum_absWeights xs ms hlen, hsum]
  · rintro ⟨ms', hlen', hsum'⟩
    rw [absWeights_length] at hlen'
    refine ⟨flipNegMask xs ms', flipNegMask_length xs ms' hlen', ?_⟩
    have h1 := maskSum_absWeights xs (flipNegMask xs ms') (flipNegMask_length xs ms' hlen')
    rw [flipNegMask_involutive xs ms' hlen', hsum'] at h1
    omega

/-- Drop zero occurrences to obtain strictly positive weights after `absWeights`. -/
def nonZeroWeights : List Int → List Int
  | [] => []
  | a :: xs => if a = 0 then nonZeroWeights xs else a :: nonZeroWeights xs

theorem nonZeroWeights_mem_imp {xs : List Int} {x : Int}
    (hx : x ∈ nonZeroWeights xs) : x ∈ xs ∧ x ≠ 0 := by
  induction xs with
  | nil => simp [nonZeroWeights] at hx
  | cons a xs ih =>
      by_cases ha : a = 0
      · simp only [nonZeroWeights, ha, ↓reduceIte] at hx
        rcases ih hx with ⟨hmem, hne⟩
        exact ⟨List.mem_cons_of_mem a hmem, hne⟩
      · simp only [nonZeroWeights, ha, ↓reduceIte, List.mem_cons] at hx
        rcases hx with rfl | hx
        · exact ⟨List.mem_cons_self, ha⟩
        · rcases ih hx with ⟨hmem, hne⟩
          exact ⟨List.mem_cons_of_mem a hmem, hne⟩

theorem nonZeroWeights_absWeights_pos {xs : List Int} {x : Int}
    (hx : x ∈ nonZeroWeights (absWeights xs)) : 0 < x := by
  rcases nonZeroWeights_mem_imp hx with ⟨hmem, hne⟩
  have hnonneg := absWeights_nonneg hmem
  omega

theorem hasSum_nonZeroWeights_iff (xs : List Int) (b : Int) :
    HasSum (nonZeroWeights xs) b ↔ HasSum xs b := by
  induction xs generalizing b with
  | nil => rfl
  | cons a xs ih =>
      by_cases ha : a = 0
      · subst ha
        simp only [nonZeroWeights, ↓reduceIte, ih, hasSum_cons, Int.sub_zero, or_self]
      · simp only [nonZeroWeights, ha, ↓reduceIte, hasSum_cons, ih]

theorem hasSum_signed_iff_pos (xs : List Int) (b : Int) :
    HasSum xs b ↔ HasSum (nonZeroWeights (absWeights xs)) (b + negOffset xs) := by
  rw [hasSum_nonZeroWeights_iff, hasSum_signed_iff_nonneg]

/-! ## Tie-breaking isolation family -/

/-- Transformed weights `scale * a_i + u_i` for solution isolation. -/
def isolateWeights (scale : Int) : List Int → List Int → List Int
  | [], _ => []
  | a :: xs, us =>
      match us with
      | [] => []
      | u :: us' => (scale * a + u) :: isolateWeights scale xs us'

/-- Transformed target `scale * b + s` for tie sum `s`. -/
def isolateTarget (scale b s : Int) : Int :=
  scale * b + s

theorem isolateWeights_length (scale : Int) (xs us : List Int)
    (hu : us.length = xs.length) :
    (isolateWeights scale xs us).length = xs.length := by
  induction xs generalizing us with
  | nil => rfl
  | cons a xs ih =>
      cases us with
      | nil => cases hu
      | cons u us' =>
          have hu' := Nat.succ.inj hu
          simp [isolateWeights, ih us' hu']

theorem maskSum_isolateWeights (scale : Int) (xs us : List Int) (ms : List Bool)
    (hu : us.length = xs.length) :
    maskSum (isolateWeights scale xs us) ms =
      scale * maskSum xs ms + maskSum us ms := by
  induction xs generalizing us ms with
  | nil =>
      cases us with
      | nil => simp [isolateWeights, maskSum]
      | cons _ _ => cases hu
  | cons a xs ih =>
      cases us with
      | nil => cases hu
      | cons u us' =>
          have hu' := Nat.succ.inj hu
          cases ms with
          | nil => simp [isolateWeights, maskSum]
          | cons bit ms' =>
              cases bit
              · simp only [isolateWeights, maskSum, ih us' ms' hu']
              · simp only [isolateWeights, maskSum, ih us' ms' hu', Int.mul_add]
                omega

theorem maskSum_nonneg_of_nonneg {us : List Int} (ms : List Bool)
    (hnonneg : ∀ u ∈ us, 0 ≤ u) : 0 ≤ maskSum us ms := by
  induction us generalizing ms with
  | nil => simp [maskSum]
  | cons u us ih =>
      cases ms with
      | nil => simp [maskSum]
      | cons bit ms' =>
          have hu : 0 ≤ u := hnonneg u List.mem_cons_self
          have hus : ∀ x ∈ us, 0 ≤ x := fun x hx => hnonneg x (List.mem_cons_of_mem u hx)
          have hrec := ih ms' hus
          cases bit <;> simp only [maskSum] <;> omega

theorem maskSum_le_sum_of_nonneg {us : List Int} (ms : List Bool)
    (hnonneg : ∀ u ∈ us, 0 ≤ u) : maskSum us ms ≤ us.sum := by
  induction us generalizing ms with
  | nil => simp [maskSum]
  | cons u us ih =>
      have hu : 0 ≤ u := hnonneg u List.mem_cons_self
      have hus : ∀ x ∈ us, 0 ≤ x := fun x hx => hnonneg x (List.mem_cons_of_mem u hx)
      have hsum_nonneg : 0 ≤ us.sum := by
        have h0 := ih [] hus
        rw [maskSum_nil_right] at h0
        exact h0
      cases ms with
      | nil =>
          simp only [maskSum, List.sum_cons]
          omega
      | cons bit ms' =>
          have hrec := ih ms' hus
          cases bit <;> simp only [maskSum, List.sum_cons] <;> omega

theorem scale_mul_add_inj {scale x b r1 r2 : Int}
    (hr1_lo : 0 ≤ r1) (hr1_hi : r1 < scale)
    (hr2_lo : 0 ≤ r2) (hr2_hi : r2 < scale)
    (heq : scale * x + r1 = scale * b + r2) :
    x = b ∧ r1 = r2 := by
  have hscale_pos : 0 ≤ scale := by omega
  have hxb : x = b := by
    by_cases hlt : x < b
    · have hle : x + 1 ≤ b := by omega
      have hmul := Int.mul_le_mul_of_nonneg_left hle hscale_pos
      rw [Int.mul_add, Int.mul_one] at hmul
      omega
    · by_cases hgt : b < x
      · have hle : b + 1 ≤ x := by omega
        have hmul := Int.mul_le_mul_of_nonneg_left hle hscale_pos
        rw [Int.mul_add, Int.mul_one] at hmul
        omega
      · omega
  subst hxb
  exact ⟨rfl, by omega⟩

/-- Soundness and completeness of the isolated target `isolateTarget scale b s`
for a witness mask `ms`. -/
theorem isolation_mask_iff {scale b s : Int} {xs us : List Int} {ms : List Bool}
    (hu : us.length = xs.length)
    (hnonneg : ∀ u ∈ us, 0 ≤ u)
    (hscale : us.sum < scale)
    (hs_lo : 0 ≤ s) (hs_hi : s < scale) :
    maskSum (isolateWeights scale xs us) ms = isolateTarget scale b s ↔
      maskSum xs ms = b ∧ maskSum us ms = s := by
  rw [maskSum_isolateWeights scale xs us ms hu, isolateTarget]
  constructor
  · intro heq
    have hm_lo := maskSum_nonneg_of_nonneg ms hnonneg
    have hm_le := maskSum_le_sum_of_nonneg ms hnonneg
    have hm_hi : maskSum us ms < scale := by omega
    exact scale_mul_add_inj hm_lo hm_hi hs_lo hs_hi heq
  · rintro ⟨rfl, rfl⟩
    rfl

/-- Decision equivalence: `(xs, b)` is feasible iff some tie sum `0 ≤ s ≤ us.sum`
produces a feasible isolated instance `(isolateWeights scale xs us, isolateTarget scale b s)`. -/
theorem isolation_hasSum_iff {scale b : Int} {xs us : List Int}
    (hu : us.length = xs.length)
    (hnonneg : ∀ u ∈ us, 0 ≤ u)
    (hscale : us.sum < scale) :
    HasSum xs b ↔
      ∃ s : Int, 0 ≤ s ∧ s ≤ us.sum ∧
        HasSum (isolateWeights scale xs us) (isolateTarget scale b s) := by
  rw [hasSum_iff_exists_mask]
  constructor
  · rintro ⟨ms, hlen, hsum⟩
    refine ⟨maskSum us ms, maskSum_nonneg_of_nonneg ms hnonneg,
      maskSum_le_sum_of_nonneg ms hnonneg, ?_⟩
    rw [hasSum_iff_exists_mask]
    refine ⟨ms, ?_, ?_⟩
    · rw [isolateWeights_length scale xs us hu, hlen]
    · rw [maskSum_isolateWeights scale xs us ms hu, isolateTarget, hsum]
  · rintro ⟨s, hs_lo, hs_le, hiso⟩
    rw [hasSum_iff_exists_mask] at hiso
    rcases hiso with ⟨ms, hlen, hsum⟩
    rw [isolateWeights_length scale xs us hu] at hlen
    have hs_hi : s < scale := by omega
    rcases (isolation_mask_iff hu hnonneg hscale hs_lo hs_hi).mp hsum with ⟨hxb, _⟩
    exact ⟨ms, hlen, hxb⟩

/-- If `s` isolates a unique solution of `(xs, b)` by its tie weight `maskSum us ms = s`,
then any two witness masks for the isolated target `isolateTarget scale b s` are equal. -/
theorem isolation_unique_mask {scale b s : Int} {xs us : List Int} {ms1 ms2 : List Bool}
    (hu : us.length = xs.length)
    (hnonneg : ∀ u ∈ us, 0 ≤ u)
    (hscale : us.sum < scale)
    (hs_lo : 0 ≤ s) (hs_hi : s < scale)
    (huniq : ∀ m1 m2 : List Bool,
      maskSum xs m1 = b → maskSum us m1 = s →
      maskSum xs m2 = b → maskSum us m2 = s → m1 = m2)
    (hm1 : maskSum (isolateWeights scale xs us) ms1 = isolateTarget scale b s)
    (hm2 : maskSum (isolateWeights scale xs us) ms2 = isolateTarget scale b s) :
    ms1 = ms2 := by
  rcases (isolation_mask_iff hu hnonneg hscale hs_lo hs_hi).mp hm1 with ⟨hx1, hu1⟩
  rcases (isolation_mask_iff hu hnonneg hscale hs_lo hs_hi).mp hm2 with ⟨hx2, hu2⟩
  exact huniq ms1 ms2 hx1 hu1 hx2 hu2

end SubsetSum
