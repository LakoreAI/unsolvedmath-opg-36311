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

/-! ## Weight-resolved certificates (the representation split)

The representation technique balances a solution by its Hamming weight: a
weight-`ℓ` solution is written as `y + z` with `y`, `z` disjoint of weights
`~ℓ/2`. The following weight-resolved specification and its split lemma supply
the combinatorial, weight-tracking analogue of `HasSum` / `hasSum_append`. -/

/-- `HasSumWeight xs b k`: the subset sums to `b` selecting exactly `k`
occurrences. The third index is the Hamming weight used by the representation
technique. -/
inductive HasSumWeight : List Int → Int → Nat → Prop where
  | nil : HasSumWeight [] 0 0
  | skip {a : Int} {xs : List Int} {b : Int} {k : Nat} :
      HasSumWeight xs b k → HasSumWeight (a :: xs) b k
  | take {a : Int} {xs : List Int} {b : Int} {k : Nat} :
      HasSumWeight xs b k → HasSumWeight (a :: xs) (a + b) (k + 1)

/-- Forgetting the weight recovers the original specification. -/
theorem hasSumWeight_sound {xs : List Int} {b : Int} {k : Nat}
    (h : HasSumWeight xs b k) : HasSum xs b := by
  induction h with
  | nil => exact HasSum.nil
  | skip _ ih => exact HasSum.skip ih
  | take _ ih => exact HasSum.take ih

/-- Every subset sum has a weight-resolved certificate. -/
theorem hasSumWeight_complete {xs : List Int} {b : Int}
    (h : HasSum xs b) : ∃ k, HasSumWeight xs b k := by
  induction h with
  | nil => exact ⟨0, HasSumWeight.nil⟩
  | skip _ ih =>
      rcases ih with ⟨k, hk⟩
      exact ⟨k, HasSumWeight.skip hk⟩
  | take _ ih =>
      rcases ih with ⟨k, hk⟩
      exact ⟨k + 1, HasSumWeight.take hk⟩

/-- The selected weight never exceeds the number of occurrences. -/
theorem hasSumWeight_le_length {xs : List Int} {b : Int} {k : Nat}
    (h : HasSumWeight xs b k) : k ≤ xs.length := by
  induction h with
  | nil => simp
  | skip _ ih =>
      simp only [List.length_cons]
      omega
  | take _ ih =>
      simp only [List.length_cons]
      omega

/-- Split lemma for weight-resolved certificates: any contiguous split factors
the certificate into two disjoint parts whose weights add up. This is the
combinatorial core of the representation decomposition `x = y + z`. -/
theorem hasSumWeight_append {left right : List Int} {b : Int} {k : Nat}
    (h : HasSumWeight (left ++ right) b k) :
    ∃ u v ku kv, HasSumWeight left u ku ∧ HasSumWeight right v kv ∧
      u + v = b ∧ ku + kv = k := by
  induction left generalizing b k with
  | nil =>
      simp only [List.nil_append] at h
      exact ⟨0, b, 0, k, HasSumWeight.nil, h, by omega, by omega⟩
  | cons a xs ih =>
      simp only [List.cons_append] at h
      cases h with
      | skip h' =>
          rcases ih h' with ⟨u, v, ku, kv, hu, hv, he, hk⟩
          exact ⟨u, v, ku, kv, HasSumWeight.skip hu, hv, he, hk⟩
      | take h' =>
          rcases ih h' with ⟨u, v, ku, kv, hu, hv, he, hk⟩
          refine ⟨a + u, v, ku + 1, kv, HasSumWeight.take hu, hv, ?_, ?_⟩
          · omega
          · omega

/-! ## Residue enumeration (the modular filter)

The HGJ filter enumerates subsets by the residue of their dot product modulo a
chosen modulus. The following is the completeness half: no feasible sum is
discarded by the filter. -/

/-- Residues of all subset sums under a filter of modulus `m`. -/
def residues (m : Nat) (xs : List Int) : List Int :=
  (sums xs).map (fun s => s % (m : Int))

/-- The filter's residue set contains the residue of every feasible sum, so a
random residue keeps a solution with the probability the representation count
predicts. -/
theorem mem_residues {xs : List Int} {b : Int} {m : Nat} (h : HasSum xs b) :
    b % (m : Int) ∈ residues m xs := by
  simp only [residues, List.mem_map]
  exact ⟨b, (mem_sums_iff xs b).mpr h, rfl⟩

/-! ## Mixing concentration (R13)

The HGJ filter keeps weight-`w` index sets whose value sum lies in a residue
class. If the weight-`w` sums take few residues, the values themselves are
concentrated. The two lemmas below are the elementary kernel of the target
mixing dichotomy (`docs/research/subset-sum-n3/MIXING.md`): two weight-`w` sets
differing only in the index `i` versus `j` have sums differing by `a i - a j`,
so every pairwise value difference is a difference of two weight-`w` sums. -/

/-- Sum of the values selected by a list of occurrence indices. -/
def listSum {m : Nat} (a : Fin m → Int) (s : List (Fin m)) : Int :=
  (s.map a).sum

/-- `x` is a weight-`w` sum: the value sum of a nodup index list of length `w`. -/
def IsWSum {m : Nat} (a : Fin m → Int) (w : Nat) (x : Int) : Prop :=
  ∃ s : List (Fin m), s.Nodup ∧ s.length = w ∧ listSum a s = x

theorem value_diff_mem_wsum_diff {m w : Nat} (a : Fin m → Int)
    {i j : Fin m} {s : List (Fin m)}
    (hs : s.Nodup) (hi : i ∉ s) (hj : j ∉ s) (hlen : s.length + 1 = w) :
    ∃ x y, IsWSum a w x ∧ IsWSum a w y ∧ x - y = a i - a j := by
  refine ⟨listSum a (i :: s), listSum a (j :: s), ?_, ?_, ?_⟩
  · exact ⟨i :: s, List.nodup_cons.mpr ⟨hi, hs⟩, by simpa using hlen, rfl⟩
  · exact ⟨j :: s, List.nodup_cons.mpr ⟨hj, hs⟩, by simpa using hlen, rfl⟩
  · simp only [listSum, List.map_cons, List.sum_cons]
    omega

theorem value_diff_mod_mem_wsum_mod_diff {m w : Nat} (a : Fin m → Int) (p : Int)
    {i j : Fin m} {s : List (Fin m)}
    (hs : s.Nodup) (hi : i ∉ s) (hj : j ∉ s) (hlen : s.length + 1 = w) :
    ∃ x y, IsWSum a w x ∧ IsWSum a w y ∧
      (x % p - y % p) % p = (a i - a j) % p := by
  refine ⟨listSum a (i :: s), listSum a (j :: s), ?_, ?_, ?_⟩
  · exact ⟨i :: s, List.nodup_cons.mpr ⟨hi, hs⟩, by simpa using hlen, rfl⟩
  · exact ⟨j :: s, List.nodup_cons.mpr ⟨hj, hs⟩, by simpa using hlen, rfl⟩
  · rw [← Int.sub_emod]
    have hdiff : listSum a (i :: s) - listSum a (j :: s) = a i - a j := by
      simp only [listSum, List.map_cons, List.sum_cons]
      omega
    rw [hdiff]

/-- `r = 1` contraction kernel: if every value is congruent to `ρ` modulo `p`
(as divisibility), then every weight-`w` sum is congruent to `w · ρ`, so `p` can
be stripped from the instance (`docs/research/subset-sum-n3/MIXING.md`). -/
theorem dvd_listSum_sub_length_mul {m : Nat} (a : Fin m → Int) (p ρ : Int)
    (h : ∀ i, p ∣ a i - ρ) :
    ∀ s : List (Fin m), p ∣ listSum a s - (s.length : Int) * ρ
  | [] => by simp [listSum]
  | i :: t => by
      rw [listSum, List.map_cons, List.sum_cons, List.length_cons]
      have hsum : (a i + (List.map a t).sum) - (↑(t.length + 1) * ρ)
          = (a i - ρ) + ((List.map a t).sum - ↑t.length * ρ) := by
        rw [Int.natCast_succ, Int.add_mul, Int.one_mul]
        omega
      rw [hsum]
      exact Int.dvd_add (h i) (by
        simpa only [listSum] using dvd_listSum_sub_length_mul a p ρ h t)

#eval meetInMiddle [3, -2] [7, 0] 5
#eval meetInMiddle [2, 4] [8] 7
#eval residues 4 [1, 2, 3]
#print axioms mem_sums_iff
#print axioms sums_length
#print axioms hasSum_append
#print axioms meetInMiddle_correct
#print axioms hasSum_magnitude
#print axioms target_outside_impossible
#print axioms restricted_work_bound
#print axioms hasSumWeight_sound
#print axioms hasSumWeight_complete
#print axioms hasSumWeight_le_length
#print axioms hasSumWeight_append
#print axioms mem_residues
#print axioms value_diff_mem_wsum_diff
#print axioms value_diff_mod_mem_wsum_mod_diff
#print axioms dvd_listSum_sub_length_mul

end SubsetSum
