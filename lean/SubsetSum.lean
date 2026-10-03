import Std

/-! Exact subset-sum correctness. This file does NOT prove the open
worst-case O*(2^(n/3)) bound, nor a runtime bound for Python. -/
namespace SubsetSum

/-- An independent specification: select or skip each occurrence once. -/
inductive HasSum : List Int → Int → Prop where
  | nil : HasSum [] 0
  | skip {a : Int} {xs : List Int} {b : Int} :
      HasSum xs b → HasSum (a :: xs) b
  | take {a : Int} {xs : List Int} {b : Int} :
      HasSum xs b → HasSum (a :: xs) (a + b)

def sums : List Int → List Int
  | [] => [0]
  | a :: xs => sums xs ++ (sums xs).map (a + ·)

theorem hasSum_cons (a : Int) (xs : List Int) (b : Int) :
    HasSum (a :: xs) b ↔ HasSum xs b ∨ HasSum xs (b - a) := by
  constructor
  · intro h
    cases h with
    | skip h => exact Or.inl h
    | @take _ _ s h =>
        right
        have eq : a + s - a = s := by omega
        simpa only [eq] using h
  · intro h
    rcases h with h | h
    · exact HasSum.skip h
    · have ht := HasSum.take (a := a) h
      have he : a + (b - a) = b := by omega
      rw [he] at ht
      exact ht

theorem mem_sums_iff (xs : List Int) (b : Int) :
    b ∈ sums xs ↔ HasSum xs b := by
  induction xs generalizing b with
  | nil =>
      simp only [sums, List.mem_singleton]
      constructor
      · intro h; subst b; exact HasSum.nil
      · intro h; cases h; rfl
  | cons a xs ih =>
      rw [hasSum_cons]
      simp only [sums, List.mem_append, List.mem_map]
      constructor
      · intro h
        rcases h with h | ⟨s, hs, he⟩
        · exact Or.inl ((ih b).mp h)
        · right
          have eq : b - a = s := by omega
          rw [eq]
          exact (ih s).mp hs
      · intro h
        rcases h with h | h
        · exact Or.inl ((ih b).mpr h)
        · right
          exact ⟨b - a, (ih (b - a)).mpr h, by omega⟩

theorem sums_length (xs : List Int) :
    (sums xs).length = 2 ^ xs.length := by
  induction xs with
  | nil => simp [sums]
  | cons a xs ih =>
      simp only [sums, List.length_append, List.length_map,
        List.length_cons, ih, Nat.pow_succ]
      omega

/-- Splitting into any two contiguous halves preserves all solutions. -/
theorem hasSum_append (left right : List Int) (b : Int) :
    HasSum (left ++ right) b ↔
      ∃ u v, HasSum left u ∧ HasSum right v ∧ u + v = b := by
  induction left generalizing b with
  | nil =>
      simp only [List.nil_append]
      constructor
      · intro h; exact ⟨0, b, HasSum.nil, h, by omega⟩
      · rintro ⟨u, v, hu, hv, he⟩
        cases hu
        have eq : v = b := by omega
        simpa [eq] using hv
  | cons a xs ih =>
      simp only [List.cons_append, hasSum_cons]
      constructor
      · intro h
        rcases h with h | h
        · rcases (ih b).mp h with ⟨u, v, hu, hv, he⟩
          exact ⟨u, v, Or.inl hu, hv, he⟩
        · rcases (ih (b - a)).mp h with ⟨u, v, hu, hv, he⟩
          refine ⟨a + u, v, Or.inr ?_, hv, by omega⟩
          have eq : a + u - a = u := by omega
          simpa only [eq] using hu
      · rintro ⟨u, v, hu, hv, he⟩
        rcases hu with hu | hu
        · left; exact (ih b).mpr ⟨u, v, hu, hv, he⟩
        · right; exact (ih (b - a)).mpr ⟨u - a, v, hu, hv, by omega⟩

/-- Executable reference specification; linear membership is intentionally
simple. Python uses sorting/binary search instead. -/
def meetInMiddle (left right : List Int) (b : Int) : Bool :=
  (sums left).any fun u => (sums right).contains (b - u)

theorem meetInMiddle_correct (left right : List Int) (b : Int) :
    meetInMiddle left right b = true ↔ HasSum (left ++ right) b := by
  simp only [meetInMiddle, List.any_eq_true, List.contains_iff,
    mem_sums_iff]
  rw [hasSum_append]
  constructor
  · rintro ⟨u, hu, hv⟩
    exact ⟨u, b - u, hu, hv, by omega⟩
  · rintro ⟨u, v, hu, hv, he⟩
    have eq : b - u = v := by omega
    exact ⟨u, hu, by simpa [eq] using hv⟩

/-- Sum of absolute magnitudes, giving a radius for every partial sum. -/
def magnitude : List Int → Nat
  | [] => 0
  | a :: xs => a.natAbs + magnitude xs

/-- Every feasible sum lies inside the signed DP's numeric radius. -/
theorem hasSum_magnitude {xs : List Int} {b : Int} (h : HasSum xs b) :
    b.natAbs ≤ magnitude xs := by
  induction h with
  | nil => simp [magnitude]
  | @skip a xs b h ih =>
      simp only [magnitude]
      omega
  | @take a xs b h ih =>
      simp only [magnitude]
      exact Nat.le_trans (Int.natAbs_add_le a b) (Nat.add_le_add_left ih _)

theorem target_outside_impossible {xs : List Int} {b : Int}
    (h : magnitude xs < b.natAbs) : ¬ HasSum xs b := by
  intro hs
  have hb := hasSum_magnitude hs
  omega

/-- Algebraic work envelope for a bounded-magnitude DP, not operational
semantics or a proof that arbitrary instances satisfy the hypothesis. -/
theorem restricted_work_bound (n w : Nat) (h : w ≤ 2 ^ (n / 3)) :
    n * (2 * w + 1) ≤ n * (2 * 2 ^ (n / 3) + 1) := by
  apply Nat.mul_le_mul_left
  omega

#eval meetInMiddle [3, -2] [7, 0] 5
#eval meetInMiddle [2, 4] [8] 7
#print axioms mem_sums_iff
#print axioms sums_length
#print axioms hasSum_append
#print axioms meetInMiddle_correct
#print axioms hasSum_magnitude
#print axioms target_outside_impossible
#print axioms restricted_work_bound

end SubsetSum
