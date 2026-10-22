import SubsetSum.HighEnergy

/-! # Deficiency, Flip, and Carry Lemmas of the October 2026 Preprint

Deterministic combinatorial lemmas used by the preprint's preliminary search
and alias extraction, stated over the distinct-sum list `coreSums`:
1. **Lemma 2.2 (deficiency).** With `d(V) = |V| - log₂ |Σ(V)|`, the statements
   `d(∅) = 0`, `d ≥ 0`, `0 ≤ d(V ∪ {i}) - d(V) ≤ 1`, superadditivity, and the
   exchange bound are proved in exponentiated form: `|Σ(∅)| = 1`,
   `|Σ(V)| ≤ 2^|V|`, `|Σ(V)| ≤ |Σ(a :: V)| ≤ 2|Σ(V)|`,
   `|Σ(U ++ V)| ≤ |Σ(U)| |Σ(V)|`, and `|Σ(i :: U)| ≤ 2 |Σ(j :: U)|`.
2. **Flip bijection (5.5).** For a flip mask `F`, `J = I △ F` selects signed
   weights `(-1)^[i∈F] a_i` with sum `a(I) - a(F)`, and the flip is involutive.
3. **Carry (5.4).** If reduced weights lie in `[0, P)` and a subset sum is
   `≡ t (mod P)`, then it equals `(t mod P) + qP` for some `q ≤ n`. -/
namespace SubsetSum

/-! ## Pigeonhole for duplicate-free lists -/

/-- Remove the first occurrence of `a` (local copy keeps axioms choice-free). -/
def eraseInt (a : Int) : List Int → List Int
  | [] => []
  | b :: l => if b = a then l else b :: eraseInt a l

theorem mem_eraseInt_of_ne {a x : Int} (hne : x ≠ a) :
    ∀ {l : List Int}, x ∈ l → x ∈ eraseInt a l
  | [], h => nomatch h
  | b :: l, h => by
      simp only [eraseInt]
      split
      · next hb =>
          rcases List.mem_cons.mp h with h | h
          · exact absurd (h.trans hb) hne
          · exact h
      · rcases List.mem_cons.mp h with h | h
        · exact h ▸ List.mem_cons_self
        · exact List.mem_cons_of_mem b (mem_eraseInt_of_ne hne h)

theorem length_eraseInt {a : Int} : ∀ {l : List Int}, a ∈ l → (eraseInt a l).length + 1 = l.length
  | [], h => nomatch h
  | b :: l, h => by
      simp only [eraseInt]
      split
      · simp
      · next hb =>
          rcases List.mem_cons.mp h with h | h
          · exact absurd h.symm hb
          · simp only [List.length_cons, length_eraseInt h]

theorem length_le_of_nodup_subset :
    ∀ {l₁ l₂ : List Int}, l₁.Nodup → (∀ x ∈ l₁, x ∈ l₂) → l₁.length ≤ l₂.length
  | [], _, _, _ => Nat.zero_le _
  | a :: t, l₂, hnd, hsub => by
      rw [List.nodup_cons] at hnd
      have ha : a ∈ l₂ := hsub a List.mem_cons_self
      have ht : ∀ x ∈ t, x ∈ eraseInt a l₂ := by
        intro x hx
        have hne : x ≠ a := fun h => hnd.1 (h ▸ hx)
        exact mem_eraseInt_of_ne hne (hsub x (List.mem_cons_of_mem a hx))
      have ih := length_le_of_nodup_subset hnd.2 ht
      have hlen := length_eraseInt ha
      simp only [List.length_cons]
      omega

/-! ## Lemma 2.2: deficiency in exponentiated form -/

theorem coreSums_nil_length : (coreSums []).length = 1 := by decide

/-- Adding an index never shrinks the support: `d(V ∪ {a}) ≤ d(V) + 1`. -/
theorem coreSums_length_le_cons (a : Int) (V : List Int) :
    (coreSums V).length ≤ (coreSums (a :: V)).length :=
  length_le_of_nodup_subset (coreSums_nodup V) fun c hc =>
    (mem_coreSums_iff _ c).mpr (HasSum.skip ((mem_coreSums_iff V c).mp hc))

/-- Adding an index at most doubles the support: `d(V) ≤ d(V ∪ {a})`. -/
theorem coreSums_cons_length_le (a : Int) (V : List Int) :
    (coreSums (a :: V)).length ≤ 2 * (coreSums V).length := by
  have h := length_le_of_nodup_subset (coreSums_nodup (a :: V))
    (l₂ := coreSums V ++ (coreSums V).map (a + ·)) fun c hc => by
      rw [mem_coreSums_iff, hasSum_cons] at hc
      rw [List.mem_append, List.mem_map]
      rcases hc with hc | hc
      · exact Or.inl ((mem_coreSums_iff V c).mpr hc)
      · exact Or.inr ⟨c - a, (mem_coreSums_iff V _).mpr hc, by omega⟩
  simp only [List.length_append, List.length_map] at h
  omega

/-- `d(V) ≥ 0`: at most `2^|V|` distinct subset sums. -/
theorem coreSums_length_le_pow (V : List Int) : (coreSums V).length ≤ 2 ^ V.length := by
  induction V with
  | nil => simp [coreSums_nil_length]
  | cons a V ih =>
      have := coreSums_cons_length_le a V
      rw [List.length_cons, Nat.pow_succ]
      omega

theorem sum_map_const_length {α : Type} (l : List α) (k : Nat) :
    (l.map fun _ => k).sum = l.length * k := by
  induction l with
  | nil => simp
  | cons _ t ih => simp [ih, Nat.succ_mul, Nat.add_comm]

/-- Superadditivity `d(U ∪ V) ≥ d(U) + d(V)`, i.e. `|Σ(U ∪ V)| ≤ |Σ(U)| |Σ(V)|`. -/
theorem coreSums_append_length_le (U V : List Int) :
    (coreSums (U ++ V)).length ≤ (coreSums U).length * (coreSums V).length := by
  have h := length_le_of_nodup_subset (coreSums_nodup (U ++ V))
    (l₂ := (coreSums U).flatMap fun u => (coreSums V).map (u + ·)) fun c hc => by
      rw [mem_coreSums_iff, hasSum_append] at hc
      rcases hc with ⟨u, v, hu, hv, huv⟩
      rw [List.mem_flatMap]
      exact ⟨u, (mem_coreSums_iff U u).mpr hu,
        List.mem_map.mpr ⟨v, (mem_coreSums_iff V v).mpr hv, huv⟩⟩
  rw [List.length_flatMap] at h
  simp only [List.length_map, sum_map_const_length] at h
  exact h

/-- Exchange bound `|d(U ∪ {i}) - d(U ∪ {j})| ≤ 1`, in one direction. -/
theorem coreSums_exchange_length_le (i j : Int) (U : List Int) :
    (coreSums (i :: U)).length ≤ 2 * (coreSums (j :: U)).length := by
  have h1 := coreSums_cons_length_le i U
  have h2 := coreSums_length_le_cons j U
  omega

/-! ## Flip bijection (equation (5.5)) -/

/-- Signed weights `(-1)^[i ∈ F] a_i`. -/
def flipWeights : List Bool → List Int → List Int
  | f :: fs, a :: xs => (if f then -a else a) :: flipWeights fs xs
  | _, _ => []

/-- Symmetric difference `I △ F` of occurrence masks. -/
def xorMask : List Bool → List Bool → List Bool
  | m :: ms, f :: fs => (m != f) :: xorMask ms fs
  | _, _ => []

theorem xorMask_length {ms fs : List Bool} (h : ms.length = fs.length) :
    (xorMask ms fs).length = ms.length := by
  induction ms generalizing fs with
  | nil => simp [xorMask]
  | cons m ms ih =>
      cases fs with
      | nil => cases h
      | cons f fs => simp [xorMask, ih (Nat.succ.inj h)]

theorem xorMask_involutive {ms fs : List Bool} (h : ms.length = fs.length) :
    xorMask (xorMask ms fs) fs = ms := by
  induction ms generalizing fs with
  | nil => simp [xorMask]
  | cons m ms ih =>
      cases fs with
      | nil => cases h
      | cons f fs => cases m <;> cases f <;> simp [xorMask, ih (Nat.succ.inj h)]

/-- `Σ_{i∈J} b^F_i = Σ_{i∈I} b_i - Σ_{i∈F} b_i` with `J = I △ F`. -/
theorem maskSum_flip (xs : List Int) {ms fs : List Bool}
    (hm : ms.length = xs.length) (hf : fs.length = xs.length) :
    maskSum (flipWeights fs xs) (xorMask ms fs) = maskSum xs ms - maskSum xs fs := by
  induction xs generalizing ms fs with
  | nil => simp [flipWeights, maskSum]
  | cons a xs ih =>
      cases ms with
      | nil => cases hm
      | cons m ms =>
          cases fs with
          | nil => cases hf
          | cons f fs =>
              have h := ih (Nat.succ.inj hm) (Nat.succ.inj hf)
              cases m <;> cases f <;> simp only [flipWeights, xorMask, maskSum] at h ⊢ <;>
                simp <;> omega

/-- Flipping is a bijection on solutions: `I` hits `t` iff `I △ F` hits the
translated target `t - a(F)` under the signed weights. -/
theorem flip_hits_iff (xs : List Int) {ms fs : List Bool} (t : Int)
    (hm : ms.length = xs.length) (hf : fs.length = xs.length) :
    maskSum xs ms = t ↔
      maskSum (flipWeights fs xs) (xorMask ms fs) = t - maskSum xs fs := by
  rw [maskSum_flip xs hm hf]
  exact ⟨fun h => by omega, fun h => by omega⟩

/-! ## Carry decomposition (equation (5.4)) -/

theorem maskSum_nonneg {xs : List Int} (ms : List Bool) (h : ∀ x ∈ xs, 0 ≤ x) :
    0 ≤ maskSum xs ms := by
  induction xs generalizing ms with
  | nil => simp [maskSum]
  | cons a xs ih =>
      have ha := h a List.mem_cons_self
      have ih' := fun ms' => ih ms' (fun x hx => h x (List.mem_cons_of_mem a hx))
      cases ms with
      | nil => simp [maskSum]
      | cons m ms => cases m <;> simp only [maskSum] <;> have := ih' ms <;> omega

theorem maskSum_le_length_mul {xs : List Int} {P : Int} (ms : List Bool) (hP : 0 ≤ P)
    (h : ∀ x ∈ xs, x ≤ P) : maskSum xs ms ≤ xs.length * P := by
  induction xs generalizing ms with
  | nil => simp [maskSum]
  | cons a xs ih =>
      have ha := h a List.mem_cons_self
      have ih' := fun ms' => ih ms' (fun x hx => h x (List.mem_cons_of_mem a hx))
      have hsucc : ((xs.length + 1 : Nat) : Int) * P = (xs.length : Int) * P + P := by
        rw [Int.natCast_add, Int.add_mul]; simp
      rw [List.length_cons, hsucc]
      cases ms with
      | nil => simp only [maskSum_nil_right]; have := Int.mul_nonneg (Int.ofNat_zero_le xs.length) hP; omega
      | cons m ms => cases m <;> simp only [maskSum] <;> have := ih' ms <;> omega

/-- Every alias of `t` modulo `P` with reduced weights in `[0, P)` has a carry
`q ∈ {0, …, n}` with `Σ_{i∈I} b_i = (t mod P) + qP`. -/
theorem alias_carry {xs : List Int} {P t : Int} (ms : List Bool) (hP : 0 < P)
    (hx : ∀ x ∈ xs, 0 ≤ x ∧ x < P) (hmod : maskSum xs ms % P = t % P) :
    ∃ q : Nat, q ≤ xs.length ∧ maskSum xs ms = t % P + q * P := by
  have h0 := maskSum_nonneg ms fun x hm => (hx x hm).1
  have h1 := maskSum_le_length_mul ms (Int.le_of_lt hP) fun x hm => Int.le_of_lt (hx x hm).2
  have hdiv := Int.ediv_add_emod (maskSum xs ms) P
  have hq0 : 0 ≤ maskSum xs ms / P := Int.ediv_nonneg h0 (Int.le_of_lt hP)
  have hrem := Int.emod_nonneg (maskSum xs ms) (Int.ne_of_gt hP)
  have hq1 : maskSum xs ms / P ≤ xs.length := by
    apply Int.not_lt.mp
    intro hlt
    have hge : P * ((xs.length : Int) + 1) ≤ P * (maskSum xs ms / P) :=
      Int.mul_le_mul_of_nonneg_left hlt (Int.le_of_lt hP)
    rw [Int.mul_add, Int.mul_one, Int.mul_comm] at hge
    omega
  refine ⟨(maskSum xs ms / P).toNat, ?_, ?_⟩
  · have := Int.toNat_of_nonneg hq0
    omega
  · rw [Int.toNat_of_nonneg hq0, ← hmod, Int.mul_comm]
    omega

end SubsetSum
