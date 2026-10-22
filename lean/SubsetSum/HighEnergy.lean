import SubsetSum.SharedMask
import SubsetSum.Representation

/-! # High-Energy Regime: Disjoint Relations, Cauchy-Schwarz Energy, and Slice Sums

Formalizes:
1. Common-element stripping on colliding subset masks (`diffMask`), proving that
   any two distinct subsets with equal sum yield a nonempty pair of *disjoint*
   subsets with equal sum and no larger weights (the forced-relation kernel of
   `HIGH_ENERGY.md` and `docs/reports/lift/lift.tex`).
2. The discrete Cauchy-Schwarz collision-energy inequality
   `(cs.sum)^2 ≤ cs.length * ∑ c_r^2` underpinning the single-prime lift
   (`LIFT.md`) and the C1–C2 bridge (`REPORT.md`).
3. Executable weight-slice distinct-sum counter (`sliceDistinctSums`) for
   testing Conjecture U (`EXPERT_QUESTIONS.md`). -/
namespace SubsetSum

/-! ## Mask Hamming weight and common-element stripping -/

/-- Hamming weight (number of `true` bits) of a Boolean mask. -/
def maskWeight : List Bool → Nat
  | [] => 0
  | false :: ms => maskWeight ms
  | true :: ms => maskWeight ms + 1

/-- Strip elements selected by `m2` from `m1` (`m1 \ m2`). -/
def diffMask : List Bool → List Bool → List Bool
  | [], _ => []
  | b1 :: m1, m2 =>
      match m2 with
      | [] => []
      | b2 :: m2' => (b1 && !b2) :: diffMask m1 m2'

theorem diffMask_length {m1 m2 : List Bool} (h : m1.length = m2.length) :
    (diffMask m1 m2).length = m1.length := by
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
          simp [diffMask, ih h']

/-- `m1 \ m2` and `m2 \ m1` are always disjoint. -/
theorem masksDisjoint_diffMask (m1 m2 : List Bool) (h : m1.length = m2.length) :
    masksDisjoint (diffMask m1 m2) (diffMask m2 m1) = true := by
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
          have hrec := ih m2' h'
          cases b1 <;> cases b2 <;> simp [diffMask, masksDisjoint, hrec]

/-- Stripping common elements never increases Hamming weight. -/
theorem maskWeight_diffMask_le (m1 m2 : List Bool) (h : m1.length = m2.length) :
    maskWeight (diffMask m1 m2) ≤ maskWeight m1 := by
  induction m1 generalizing m2 with
  | nil =>
      cases m2 with
      | nil => simp [diffMask, maskWeight]
      | cons _ _ => cases h
  | cons b1 m1 ih =>
      cases m2 with
      | nil => cases h
      | cons b2 m2' =>
          have h' := Nat.succ.inj h
          have hrec := ih m2' h'
          cases b1 <;> cases b2 <;> simp only [diffMask, Bool.false_and, Bool.true_and,
            Bool.not_false, Bool.not_true, maskWeight] <;> omega

/-- Difference of subset sums is preserved when common elements are stripped. -/
theorem maskSum_sub_eq_diffMask (xs : List Int) (m1 m2 : List Bool)
    (h1 : m1.length = xs.length) (h2 : m2.length = xs.length) :
    maskSum xs (diffMask m1 m2) - maskSum xs (diffMask m2 m1) =
      maskSum xs m1 - maskSum xs m2 := by
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
              have hrec := ih m1' m2' h1' h2'
              cases b1 <;> cases b2 <;>
                simp only [diffMask, Bool.false_and, Bool.true_and,
                  Bool.not_false, Bool.not_true, maskSum] <;> omega

/-- Two masks have equal subset sums iff their stripped disjoint masks have equal subset sums. -/
theorem maskSum_diffMask_eq_iff (xs : List Int) (m1 m2 : List Bool)
    (h1 : m1.length = xs.length) (h2 : m2.length = xs.length) :
    maskSum xs (diffMask m1 m2) = maskSum xs (diffMask m2 m1) ↔
      maskSum xs m1 = maskSum xs m2 := by
  have hsub := maskSum_sub_eq_diffMask xs m1 m2 h1 h2
  constructor <;> intro _ <;> omega

/-- Distinct masks remain distinct after stripping common elements. -/
theorem diffMask_ne_of_ne {m1 m2 : List Bool}
    (hlen : m1.length = m2.length) (hne : m1 ≠ m2) :
    diffMask m1 m2 ≠ diffMask m2 m1 := by
  induction m1 generalizing m2 with
  | nil =>
      cases m2 with
      | nil => exact False.elim (hne rfl)
      | cons _ _ => cases hlen
  | cons b1 m1 ih =>
      cases m2 with
      | nil => cases hlen
      | cons b2 m2' =>
          have hlen' := Nat.succ.inj hlen
          intro heq
          simp only [diffMask, List.cons.injEq] at heq
          rcases heq with ⟨hb, htail⟩
          have hb_eq : b1 = b2 := by
            cases b1 <;> cases b2 <;> first | rfl | cases hb
          subst hb_eq
          apply ih hlen' (fun hm => hne (congrArg (b1 :: ·) hm)) htail

/-- Complete specification of the forced disjoint relation `(diffMask m1 m2, diffMask m2 m1)`
obtained from any two distinct colliding masks `m1 ≠ m2` of weight `≤ s`. -/
theorem forcedRelation_spec (xs : List Int) (m1 m2 : List Bool) (s : Nat)
    (h1 : m1.length = xs.length) (h2 : m2.length = xs.length)
    (hne : m1 ≠ m2)
    (hw1 : maskWeight m1 ≤ s) (hw2 : maskWeight m2 ≤ s)
    (hsum : maskSum xs m1 = maskSum xs m2) :
    let P := diffMask m1 m2
    let Q := diffMask m2 m1
    P.length = xs.length ∧ Q.length = xs.length ∧
      masksDisjoint P Q = true ∧ P ≠ Q ∧
      maskWeight P ≤ s ∧ maskWeight Q ≤ s ∧
      maskSum xs P = maskSum xs Q := by
  have h12 : m1.length = m2.length := h1.trans h2.symm
  have h21 : m2.length = m1.length := h2.trans h1.symm
  refine ⟨(diffMask_length h12).trans h1, (diffMask_length h21).trans h2,
    masksDisjoint_diffMask m1 m2 h12, diffMask_ne_of_ne h12 hne,
    Nat.le_trans (maskWeight_diffMask_le m1 m2 h12) hw1,
    Nat.le_trans (maskWeight_diffMask_le m2 m1 h21) hw2,
    (maskSum_diffMask_eq_iff xs m1 m2 h1 h2).mpr hsum⟩

/-- Constructive finite pigeonhole principle on lists: if `l` has no duplicate
elements (`l.Nodup`) but `l.map f` has a duplicate (`¬ (l.map f).Nodup`), then
two distinct elements of `l` have the same image under `f`. -/
theorem exists_collision_of_nodup_not_map_nodup {α β : Type} [DecidableEq β]
    (f : α → β) {l : List α} (hnodup : l.Nodup) (hnot : ¬ (l.map f).Nodup) :
    ∃ x ∈ l, ∃ y ∈ l, x ≠ y ∧ f x = f y := by
  induction l with
  | nil => exact False.elim (hnot List.nodup_nil)
  | cons a xs ih =>
      simp only [List.nodup_cons, List.map_cons, List.mem_map] at hnodup hnot
      rcases hnodup with ⟨ha, hxs⟩
      by_cases hfa : f a ∈ xs.map f
      · rw [List.mem_map] at hfa
        rcases hfa with ⟨b, hb, hfab⟩
        have hne : a ≠ b := fun heq => ha (heq ▸ hb)
        exact ⟨a, List.mem_cons_self, b, List.mem_cons_of_mem a hb, hne, hfab.symm⟩
      · have hnot_xs : ¬ (xs.map f).Nodup := fun hnd =>
          hnot ⟨fun ⟨b, hb, hfab⟩ => hfa (List.mem_map.mpr ⟨b, hb, hfab⟩), hnd⟩
        rcases ih hxs hnot_xs with ⟨x, hx, y, hy, hne, hfxy⟩
        exact ⟨x, List.mem_cons_of_mem a hx, y, List.mem_cons_of_mem a hy, hne, hfxy⟩

/-- Lemma T (`HIGH_ENERGY.md` Section 8): if a duplicate-free collection `ms` of
valid masks of weight `≤ s` produces a duplicate subset sum (`¬ (ms.map (maskSum xs)).Nodup`),
then stripping common elements yields two distinct disjoint masks `P, Q` of
weight `≤ s` with equal subset sum. -/
theorem lemma_T_forced_disjoint_relation (xs : List Int) (ms : List (List Bool)) (s : Nat)
    (hnodup : ms.Nodup)
    (hlen : ∀ m ∈ ms, m.length = xs.length)
    (hw : ∀ m ∈ ms, maskWeight m ≤ s)
    (hcoll : ¬ (ms.map (maskSum xs)).Nodup) :
    ∃ P Q : List Bool,
      P.length = xs.length ∧ Q.length = xs.length ∧
      masksDisjoint P Q = true ∧ P ≠ Q ∧
      maskWeight P ≤ s ∧ maskWeight Q ≤ s ∧
      maskSum xs P = maskSum xs Q := by
  rcases exists_collision_of_nodup_not_map_nodup (maskSum xs) hnodup hcoll with
    ⟨m1, hm1, m2, hm2, hne, hsum⟩
  exact ⟨diffMask m1 m2, diffMask m2 m1,
    forcedRelation_spec xs m1 m2 s (hlen m1 hm1) (hlen m2 hm2) hne (hw m1 hm1) (hw m2 hm2) hsum⟩

/-! ## Transfer Barrier Proposition (`TRANSFER.md`)

`TRANSFER.md` proves that no promise-free analogue of the PESS near-geometric
lemma holds: scaling a geometric progression `[2^0, 2^1, ..., 2^(n-1)]` by an
integer `c ≥ 2` keeps all `2^n` subset sums distinct (`F(w) = 0`) while moving
weights arbitrarily far from `[2^0, ..., 2^(n-1)]`. -/

/-- Geometric progression `[1, 2, 4, ..., 2^(n-1)]`. -/
def geomWeights : Nat → List Int
  | 0 => []
  | n + 1 => 1 :: (geomWeights n).map (2 * ·)

theorem geomWeights_length (n : Nat) : (geomWeights n).length = n := by
  induction n with
  | zero => rfl
  | succ n ih => simp [geomWeights, ih]

theorem maskSum_map_mul (c : Int) (xs : List Int) (ms : List Bool) :
    maskSum (xs.map (c * ·)) ms = c * maskSum xs ms := by
  induction xs generalizing ms with
  | nil => simp [maskSum]
  | cons a xs ih =>
      cases ms with
      | nil => simp [maskSum]
      | cons bit ms' =>
          cases bit
          · simp only [List.map_cons, maskSum, ih ms']
          · simp only [List.map_cons, maskSum, ih ms', Int.mul_add]

/-- Every mask of length `n` has a unique subset sum on `geomWeights n`
(dissociated, `|S(A)| = 2^n`, `F = 0`). -/
theorem maskSum_geomWeights_inj {n : Nat} {m1 m2 : List Bool}
    (h1 : m1.length = n) (h2 : m2.length = n)
    (heq : maskSum (geomWeights n) m1 = maskSum (geomWeights n) m2) :
    m1 = m2 := by
  induction n generalizing m1 m2 with
  | zero =>
      cases m1 with
      | nil =>
          cases m2 with
          | nil => rfl
          | cons _ _ => cases h2
      | cons _ _ => cases h1
  | succ n ih =>
      cases m1 with
      | nil => cases h1
      | cons b1 m1' =>
          cases m2 with
          | nil => cases h2
          | cons b2 m2' =>
              have h1' := Nat.succ.inj h1
              have h2' := Nat.succ.inj h2
              cases b1 <;> cases b2 <;>
                simp only [geomWeights, maskSum, maskSum_map_mul] at heq
              · have hsub : maskSum (geomWeights n) m1' = maskSum (geomWeights n) m2' := by omega
                rw [ih h1' h2' hsub]
              · omega
              · omega
              · have hsub : maskSum (geomWeights n) m1' = maskSum (geomWeights n) m2' := by omega
                rw [ih h1' h2' hsub]

/-- Scaling `geomWeights n` by any `c > 0` preserves complete subset-sum
distinctness (`F = 0`), while shifting even the first weight by `c - 1`. -/
theorem maskSum_scaled_geomWeights_inj {c : Int} {n : Nat} {m1 m2 : List Bool}
    (hc : 0 < c) (h1 : m1.length = n) (h2 : m2.length = n)
    (heq : maskSum ((geomWeights n).map (c * ·)) m1 =
           maskSum ((geomWeights n).map (c * ·)) m2) :
    m1 = m2 := by
  rw [maskSum_map_mul, maskSum_map_mul] at heq
  have hsum_eq : maskSum (geomWeights n) m1 = maskSum (geomWeights n) m2 := by
    by_cases hlt : maskSum (geomWeights n) m1 < maskSum (geomWeights n) m2
    · have hle : maskSum (geomWeights n) m1 + 1 ≤ maskSum (geomWeights n) m2 := by omega
      have hmul := Int.mul_le_mul_of_nonneg_left hle (by omega : 0 ≤ c)
      rw [Int.mul_add, Int.mul_one] at hmul
      omega
    · by_cases hgt : maskSum (geomWeights n) m2 < maskSum (geomWeights n) m1
      · have hle : maskSum (geomWeights n) m2 + 1 ≤ maskSum (geomWeights n) m1 := by omega
        have hmul := Int.mul_le_mul_of_nonneg_left hle (by omega : 0 ≤ c)
        rw [Int.mul_add, Int.mul_one] at hmul
        omega
      · omega
  exact maskSum_geomWeights_inj h1 h2 hsum_eq

/-! ## Discrete Cauchy-Schwarz collision-energy bound -/

/-- Sum of squares of natural numbers in a list (the collision energy `∑ c_r^2`). -/
def sumSq : List Nat → Nat
  | [] => 0
  | c :: cs => c * c + sumSq cs

theorem two_mul_le_add_sq_of_le {a b : Nat} (h : a ≤ b) :
    2 * (a * b) ≤ a * a + b * b := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le h
  have h1 : a * (a + d) = a * a + a * d := Nat.mul_add a a d
  have h2 : (a + d) * (a + d) = a * (a + d) + d * (a + d) := Nat.add_mul a d (a + d)
  have h3 : d * (a + d) = d * a + d * d := Nat.mul_add d a d
  have h4 : d * a = a * d := Nat.mul_comm d a
  omega

theorem two_mul_le_add_sq (a b : Nat) :
    2 * (a * b) ≤ a * a + b * b := by
  rcases Nat.le_total a b with h | h
  · exact two_mul_le_add_sq_of_le h
  · have h' := two_mul_le_add_sq_of_le h
    have hcomm : b * a = a * b := Nat.mul_comm b a
    omega

/-- Helper inequality: for any `c` and list `cs`,
`2 * (c * cs.sum) ≤ cs.length * (c * c) + sumSq cs` by summing `(c - x)^2 ≥ 0`. -/
theorem two_mul_sum_le_length_sq_add_sumSq (c : Nat) :
    ∀ cs : List Nat, 2 * (c * cs.sum) ≤ cs.length * (c * c) + sumSq cs
  | [] => by simp [sumSq]
  | x :: xs => by
      have ih := two_mul_sum_le_length_sq_add_sumSq c xs
      have hsq := two_mul_le_add_sq c x
      simp only [List.sum_cons, List.length_cons, sumSq]
      have hdist : c * (x + xs.sum) = c * x + c * xs.sum := Nat.mul_add c x xs.sum
      have hlen : (xs.length + 1) * (c * c) = xs.length * (c * c) + c * c := by
        rw [Nat.add_mul, Nat.one_mul]
      omega

/-- Discrete Cauchy-Schwarz inequality: `(∑ c_r)^2 ≤ k · ∑ c_r^2`.
When `cs` lists the sizes of the `s_p` nonempty residue or sum bins of `Y` subsets,
`Y^2 ≤ s_p · E_p`. -/
theorem sq_sum_le_length_mul_sumSq :
    ∀ cs : List Nat, cs.sum * cs.sum ≤ cs.length * sumSq cs
  | [] => by simp [sumSq]
  | c :: cs => by
      have ih := sq_sum_le_length_mul_sumSq cs
      have hcross := two_mul_sum_le_length_sq_add_sumSq c cs
      simp only [List.sum_cons, List.length_cons, sumSq]
      have hexpand :
          (c + cs.sum) * (c + cs.sum) =
            c * c + 2 * (c * cs.sum) + cs.sum * cs.sum := by
        calc
          (c + cs.sum) * (c + cs.sum)
            = c * (c + cs.sum) + cs.sum * (c + cs.sum) := Nat.add_mul _ _ _
          _ = (c * c + c * cs.sum) + (cs.sum * c + cs.sum * cs.sum) := by
                rw [Nat.mul_add, Nat.mul_add]
          _ = c * c + 2 * (c * cs.sum) + cs.sum * cs.sum := by
                have hcomm : cs.sum * c = c * cs.sum := Nat.mul_comm _ _
                omega
      have hrhs :
          (cs.length + 1) * (c * c + sumSq cs) =
            c * c + cs.length * (c * c) + sumSq cs + cs.length * sumSq cs := by
        calc
          (cs.length + 1) * (c * c + sumSq cs)
            = cs.length * (c * c + sumSq cs) + 1 * (c * c + sumSq cs) := Nat.add_mul _ _ _
          _ = (cs.length * (c * c) + cs.length * sumSq cs) + (c * c + sumSq cs) := by
                rw [Nat.mul_add, Nat.one_mul]
          _ = c * c + cs.length * (c * c) + sumSq cs + cs.length * sumSq cs := by omega
      omega

/-! ## Weight-slice distinct sums (`|Σ_k(X)|`) and Conjecture U probe -/

/-- Number of distinct subset sums of Hamming weight `k` from `xs`. -/
def sliceDistinctCount (xs : List Int) (k : Nat) : Nat :=
  let sliceSums :=
    ((sumMasks xs).filter fun p => maskWeight p.2 == k).map Prod.fst
  sliceSums.eraseDups.length

/-- Profile `[|Σ_0(X)|, |Σ_1(X)|, ..., |Σ_m(X)|]` of distinct subset sums by weight. -/
def sliceProfile (xs : List Int) : List Nat :=
  (List.range (xs.length + 1)).map (sliceDistinctCount xs)

/-! ## Compressible-Core Meet-in-the-Middle (`compressMitm`)

Formalizes the exact compressible-core MITM solver (`src/compress_mitm.py`,
`HIGH_ENERGY.md` Section 7): deduplicating the subset sums of a compressible
core `C` reduces its list size from `2^|C|` to `|Σ(C)|` without losing any
feasible target sum. -/

/-- Deduplicate a list of integers while preserving membership and order of last occurrence. -/
def dedupInts : List Int → List Int
  | [] => []
  | x :: xs =>
      let rest := dedupInts xs
      if rest.contains x then rest else x :: rest

theorem mem_dedupInts_iff (xs : List Int) (a : Int) :
    a ∈ dedupInts xs ↔ a ∈ xs := by
  induction xs with
  | nil => rfl
  | cons x xs ih =>
      simp only [dedupInts]
      cases h : (dedupInts xs).contains x
      · simp only [Bool.false_eq_true, ↓reduceIte, List.mem_cons, ih]
      · simp only [↓reduceIte, List.mem_cons]
        have hx : x ∈ dedupInts xs := List.contains_iff.mp h
        constructor
        · intro ha
          exact Or.inr (ih.mp ha)
        · rintro (rfl | ha)
          · exact hx
          · exact ih.mpr ha

theorem dedupInts_nodup (xs : List Int) : (dedupInts xs).Nodup := by
  induction xs with
  | nil => exact List.nodup_nil
  | cons x xs ih =>
      simp only [dedupInts]
      cases h : (dedupInts xs).contains x
      · rw [Bool.eq_false_iff, ne_eq, List.contains_iff] at h
        simp only [Bool.false_eq_true, ↓reduceIte, List.nodup_cons]
        exact ⟨h, ih⟩
      · simp only [↓reduceIte]
        exact ih

/-- Distinct subset sums `Σ(C)` of a compressible core `C`. -/
def coreSums (core : List Int) : List Int :=
  dedupInts (sums core)

theorem coreSums_nodup (core : List Int) : (coreSums core).Nodup :=
  dedupInts_nodup (sums core)

theorem mem_coreSums_iff (core : List Int) (c : Int) :
    c ∈ coreSums core ↔ HasSum core c := by
  rw [coreSums, mem_dedupInts_iff, mem_sums_iff]

/-- Executable compressible-core MITM decision procedure on `(core, r1, r2)`. -/
def compressMitm (core r1 r2 : List Int) (b : Int) : Bool :=
  (coreSums core).any fun c =>
    (sums r1).any fun u =>
      (sums r2).contains (b - c - u)

theorem compressMitm_correct (core r1 r2 : List Int) (b : Int) :
    compressMitm core r1 r2 b = true ↔ HasSum ((core ++ r1) ++ r2) b := by
  simp only [compressMitm, List.any_eq_true, List.contains_iff,
    mem_coreSums_iff, mem_sums_iff]
  rw [hasSum_append3]
  constructor
  · rintro ⟨c, hc, u, hu, hv⟩
    exact ⟨c, u, b - c - u, hc, hu, hv, by omega⟩
  · rintro ⟨c, u, v, hc, hu, hv, hcuv⟩
    have eq : b - c - u = v := by omega
    exact ⟨c, hc, u, hu, by simpa [eq] using hv⟩

/-! ## Howgrave-Graham-Joux Modular-Filter Solver (`hgjSolve`)

Formalizes the two-way representation search (`docs/reports/representation/representation.tex`
Algorithm 1): enumerate weight-`w` pieces in residue classes `r` and `b - r` modulo `m`,
then match disjoint pairs summing to `b`. -/

/-- Candidate left pieces of Hamming weight `w` in residue class `r (mod m)`. -/
def hgjLeftPieces (xs : List Int) (w : Nat) (m r : Int) : List (Int × List Bool) :=
  (sumMasks xs).filter fun p => (maskWeight p.2 == w) && ((p.1 - r) % m == 0)

/-- Candidate right pieces of Hamming weight `w` in residue class `b - r (mod m)`. -/
def hgjRightPieces (xs : List Int) (w : Nat) (m b r : Int) : List (Int × List Bool) :=
  (sumMasks xs).filter fun q => (maskWeight q.2 == w) && ((q.1 - (b - r)) % m == 0)

/-- All valid witness masks formed by pairing disjoint left and right HGJ pieces summing to `b`. -/
def hgjCandidates (xs : List Int) (w : Nat) (m b r : Int) : List (List Bool) :=
  (hgjLeftPieces xs w m r).flatMap fun p =>
    ((hgjRightPieces xs w m b r).filter fun q =>
      (p.1 + q.1 == b) && masksDisjoint p.2 q.2).map fun q =>
      orMask p.2 q.2

/-- Executable HGJ modular-filter representation solver for a single residue `r (mod m)`. -/
def hgjSolve (xs : List Int) (w : Nat) (m b r : Int) : Option (List Bool) :=
  (hgjCandidates xs w m b r).head?

theorem hgjSolve_sound {xs : List Int} {w : Nat} {m b r : Int} {ms : List Bool}
    (h : hgjSolve xs w m b r = some ms) :
    ms.length = xs.length ∧ maskSum xs ms = b ∧ HasSum xs b := by
  have hmem : ms ∈ hgjCandidates xs w m b r := by
    cases hlist : hgjCandidates xs w m b r with
    | nil =>
        rw [hgjSolve, hlist] at h
        cases h
    | cons x rest =>
        simp only [hgjSolve, hlist, List.head?_cons, Option.some.injEq] at h
        subst h
        exact List.mem_cons_self
  simp only [hgjCandidates, hgjLeftPieces, hgjRightPieces, List.mem_flatMap,
    List.mem_map, List.mem_filter, Bool.and_eq_true, beq_iff_eq, Prod.exists,
    mem_sumMasks_iff] at hmem
  rcases hmem with ⟨u, m1, ⟨⟨hl1, hs1⟩, _, _⟩, v, m2, ⟨⟨⟨hl2, hs2⟩, _, _⟩, huv, hdisj⟩, rfl⟩
  have hlen : (orMask m1 m2).length = xs.length := by
    rw [orMask_length (hl1.trans hl2.symm), hl1]
  have hsum : maskSum xs (orMask m1 m2) = b := by
    rw [maskSum_orMask_of_disjoint xs m1 m2 hl1 hl2 hdisj, hs1, hs2, huv]
  exact ⟨hlen, hsum, (hasSum_iff_exists_mask xs b).mpr ⟨orMask m1 m2, hlen, hsum⟩⟩

/-- Completeness of `hgjSolve` when `r` hits a representation `(m1, m2)` of a solution. -/
theorem hgjSolve_isSome_of_representation {xs : List Int} {w : Nat} {m b r : Int}
    (m1 m2 : List Bool)
    (hl1 : m1.length = xs.length) (hl2 : m2.length = xs.length)
    (hw1 : maskWeight m1 = w) (hw2 : maskWeight m2 = w)
    (hdisj : masksDisjoint m1 m2 = true)
    (hsum : maskSum xs m1 + maskSum xs m2 = b)
    (hres : (maskSum xs m1 - r) % m = 0) :
    (hgjSolve xs w m b r).isSome = true := by
  let u := maskSum xs m1
  let v := maskSum xs m2
  have hres2 : (v - (b - r)) % m = 0 := by
    have hdvd1 : m ∣ u - r := Int.dvd_of_emod_eq_zero hres
    have heq : v - (b - r) = -(u - r) := by omega
    have hdvd2 : m ∣ v - (b - r) := by
      rw [heq]
      exact Int.dvd_neg.mpr hdvd1
    exact Int.emod_eq_zero_of_dvd hdvd2
  have hmem : orMask m1 m2 ∈ hgjCandidates xs w m b r := by
    simp only [hgjCandidates, hgjLeftPieces, hgjRightPieces, List.mem_flatMap,
      List.mem_map, List.mem_filter, Bool.and_eq_true, beq_iff_eq, Prod.exists,
      mem_sumMasks_iff]
    exact ⟨u, m1, ⟨⟨hl1, rfl⟩, hw1, hres⟩,
           v, m2, ⟨⟨⟨hl2, rfl⟩, hw2, hres2⟩, hsum, hdisj⟩, rfl⟩
  cases hlist : hgjCandidates xs w m b r with
  | nil =>
      rw [hlist] at hmem
      cases hmem
  | cons _ _ => simp [hgjSolve, hlist]

/-! ## PESS Crowded-Interval Binary Search Invariant (`survey.tex` Algorithm 1)

In Pigeonhole Equal Subset Sum (`∑ a_i < 2^n - 1`), an interval `[lo, hi]` is
*crowded* if more than `hi - lo + 1` subset sums fall in `[lo, hi]`. Splitting a
crowded interval at `mid` always leaves at least one crowded half. -/

/-- Enumerated subset sums of `xs` falling in the closed interval `[lo, hi]`. -/
def sumsInInterval (xs : List Int) (lo hi : Int) : List Int :=
  (sums xs).filter fun s => decide (lo ≤ s ∧ s ≤ hi)

theorem filter_disjoint_or_length {α : Type} (p q : α → Bool)
    (hdisj : ∀ x, p x = true → q x = false) (l : List α) :
    (l.filter p).length + (l.filter q).length =
      (l.filter (fun x => p x || q x)).length := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      cases hp : p x
      · cases hq : q x <;> simp [List.filter_cons, hp, hq, ← ih] <;> omega
      · have hq : q x = false := hdisj x hp
        simp [List.filter_cons, hp, hq, ← ih]
        omega

/-- Splitting `[lo, hi]` at `mid` (`lo ≤ mid ≤ hi`) partitions `sumsInInterval`
into `[lo, mid]` and `[mid + 1, hi]`. -/
theorem sumsInInterval_split_length (xs : List Int) (lo mid hi : Int)
    (h1 : lo ≤ mid) (h2 : mid ≤ hi) :
    (sumsInInterval xs lo mid).length + (sumsInInterval xs (mid + 1) hi).length =
      (sumsInInterval xs lo hi).length := by
  simp only [sumsInInterval]
  rw [filter_disjoint_or_length
    (fun s => decide (lo ≤ s ∧ s ≤ mid))
    (fun s => decide (mid + 1 ≤ s ∧ s ≤ hi))]
  · have hfun :
        (fun s : Int => decide (lo ≤ s ∧ s ≤ mid) || decide (mid + 1 ≤ s ∧ s ≤ hi)) =
          (fun s : Int => decide (lo ≤ s ∧ s ≤ hi)) := by
      funext s
      by_cases hlo : lo ≤ s <;> by_cases hmid : s ≤ mid <;> by_cases hhi : s ≤ hi <;>
        simp [hlo, hmid, hhi] <;> omega
    rw [hfun]
  · intro s hs
    simp only [decide_eq_true_eq] at hs
    simp only [decide_eq_false_iff_not]
    omega

/-- Invariant of Algorithm 1 (`docs/reports/survey/survey.tex`): if `[lo, hi]`
is crowded (`lo ≤ mid < hi`), then at least one of the two halves `[lo, mid]` or
`[mid + 1, hi]` is crowded. -/
theorem pess_crowded_halving (xs : List Int) (lo mid hi : Int)
    (h1 : lo ≤ mid) (h2 : mid < hi)
    (hcrowd : (hi - lo + 1).toNat < (sumsInInterval xs lo hi).length) :
    (mid - lo + 1).toNat < (sumsInInterval xs lo mid).length ∨
      (hi - mid).toNat < (sumsInInterval xs (mid + 1) hi).length := by
  have hsplit := sumsInInterval_split_length xs lo mid hi h1 (by omega)
  omega

end SubsetSum
