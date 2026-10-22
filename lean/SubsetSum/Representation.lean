import SubsetSum.Basic

/-! # Weight-Resolved Certificates, Modular Filter, and Mixing Kernels

Formalizes:
1. Weight-resolved subset certificates (`HasSumWeight`) and the representation
   split (`hasSumWeight_append`).
2. Modular filter completeness (`residues`, `mem_residues`).
3. The mixing concentration and contraction kernels (`value_diff_mem_wsum_diff`,
   `value_diff_mod_mem_wsum_mod_diff`, `residue_collision_iff`,
   `dvd_listSum_sub_length_mul`). -/
namespace SubsetSum

/-! ## Weight-resolved certificates (the representation split) -/

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

/-! ## Residue enumeration (the modular filter) -/

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

/-! ## Mixing concentration (R13) -/

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

/-- The summand of the collision energy `E_p` (`NEXT.md`): two representation
sums collide modulo `p` exactly when their difference is `0` modulo `p`. -/
theorem residue_collision_iff (a b p : Int) :
    a % p = b % p ↔ (a - b) % p = 0 :=
  Int.emod_eq_emod_iff_emod_sub_eq_zero

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

/-! ## Collision-energy decomposition (`E_p = E_∞ + K_p`)

In `MIXING.md` and `LIFT.md`, the modular collision energy `E_p` (number of
pairs `(x, y)` with `x % p == y % p`) splits into exact collisions (`x == y`,
counted by `E_∞` for every modulus `p`) plus proper modular collisions
(`x != y` and `x % p == y % p`, counted by `K_p`). -/

/-- Exact collisions (`x == y`) always collide modulo any `p`. -/
theorem exact_imp_mod_eq (p : Int) {x y : Int} (h : (x == y) = true) :
    (x % p == y % p) = true := by
  have heq : x = y := beq_iff_eq.mp h
  subst heq
  simp

/-- Filter partitioning for a predicate `q` implied by `p`. -/
theorem filter_implication_split {α : Type} (p q : α → Bool)
    (himp : ∀ x, p x = true → q x = true) (l : List α) :
    (l.filter p).length + (l.filter (fun x => (!p x) && q x)).length =
      (l.filter q).length := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      cases hp : p x
      · cases hq : q x <;> simp [List.filter_cons, hp, hq, ← ih] <;> omega
      · have hq : q x = true := himp x hp
        simp [List.filter_cons, hp, hq, ← ih]
        omega

/-- Exact decomposition `E_p = E_∞ + K_p` on any list of sum pairs:
the number of pairs colliding modulo `p` equals the number of exact-collision
pairs (`xy.1 == xy.2`) plus the number of proper modular-collision pairs
(`xy.1 != xy.2` and `xy.1 % p == xy.2 % p`). -/
theorem collision_energy_split (p : Int) (pairs : List (Int × Int)) :
    (pairs.filter (fun xy => xy.1 == xy.2)).length +
      (pairs.filter (fun xy => (xy.1 != xy.2) && (xy.1 % p == xy.2 % p))).length =
      (pairs.filter (fun xy => xy.1 % p == xy.2 % p)).length := by
  have hfun :
      (fun xy : Int × Int => (xy.1 != xy.2) && (xy.1 % p == xy.2 % p)) =
        (fun xy : Int × Int => (!(xy.1 == xy.2)) && (xy.1 % p == xy.2 % p)) := by
    funext xy
    simp [bne]
  rw [hfun]
  exact filter_implication_split
    (fun xy => xy.1 == xy.2)
    (fun xy => xy.1 % p == xy.2 % p)
    (fun xy h => exact_imp_mod_eq p h)
    pairs

/-! ## Impossibility of coefficient shifting for `{0,1}` and `{-1,1}` (R12)

Randolph-Węgrzycki's worst-case representation technique writes a coefficient
set `C` as a sumset `C_1 + C_2` with `|C_1| ≥ 2` and `|C_2| ≥ 2` so that at
least one coefficient has multiple representations. If `u1 < u2` in `C_1` and
`v1 < v2` in `C_2`, then `u1 + v1 < u1 + v2 < u2 + v2` are three strictly
increasing values in `C_1 + C_2`, which cannot fit inside any two-element
coefficient set `{a, b}` (such as `{0, 1}` for Subset Sum or `{-1, 1}` for
Partition). -/

/-- Three strictly ordered integers cannot all lie in a two-element set `{a, b}`. -/
theorem strict_chain3_not_in_pair {x y z a b : Int}
    (hxy : x < y) (hyz : y < z)
    (hx : x = a ∨ x = b) (hy : y = a ∨ y = b) (hz : z = a ∨ z = b) : False := by
  rcases hx with rfl | rfl <;> rcases hy with rfl | rfl <;> rcases hz with rfl | rfl <;> omega

/-- No two sets each containing at least two distinct integers can have their
sumset contained in a two-element set `{a, b}`. -/
theorem no_nontrivial_factorization_pair {u1 u2 v1 v2 a b : Int}
    (hu : u1 < u2) (hv : v1 < v2)
    (h11 : u1 + v1 = a ∨ u1 + v1 = b)
    (h12 : u1 + v2 = a ∨ u1 + v2 = b)
    (h22 : u2 + v2 = a ∨ u2 + v2 = b) : False := by
  have hlt1 : u1 + v1 < u1 + v2 := by omega
  have hlt2 : u1 + v2 < u2 + v2 := by omega
  exact strict_chain3_not_in_pair hlt1 hlt2 h11 h12 h22

/-- `{0, 1}` (Subset Sum) admits no sumset factorization `C_1 + C_2 ⊆ {0, 1}`
with `|C_1| ≥ 2` and `|C_2| ≥ 2`. -/
theorem no_coefficient_shifting_01 {u1 u2 v1 v2 : Int}
    (hu : u1 < u2) (hv : v1 < v2)
    (h11 : u1 + v1 = 0 ∨ u1 + v1 = 1)
    (h12 : u1 + v2 = 0 ∨ u1 + v2 = 1)
    (h22 : u2 + v2 = 0 ∨ u2 + v2 = 1) : False :=
  no_nontrivial_factorization_pair hu hv h11 h12 h22

/-- `{-1, 1}` (Partition) admits no sumset factorization `C_1 + C_2 ⊆ {-1, 1}`
with `|C_1| ≥ 2` and `|C_2| ≥ 2`. -/
theorem no_coefficient_shifting_pm1 {u1 u2 v1 v2 : Int}
    (hu : u1 < u2) (hv : v1 < v2)
    (h11 : u1 + v1 = -1 ∨ u1 + v1 = 1)
    (h12 : u1 + v2 = -1 ∨ u1 + v2 = 1)
    (h22 : u2 + v2 = -1 ∨ u2 + v2 = 1) : False :=
  no_nontrivial_factorization_pair hu hv h11 h12 h22

end SubsetSum
