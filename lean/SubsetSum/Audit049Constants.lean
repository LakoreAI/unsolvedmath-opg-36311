/-! # Scalar Constants of the October 2026 `O(2^(0.49n))` Preprint

Kernel-checked ledger of every scalar inequality that the preprint's exponent
bookkeeping uses (Sections 2–5 and Appendix A). Decimal constants are scaled to
integers; inequalities involving `log₂` or `2^x` are exponentiated to exact
`Nat` comparisons, which the kernel decides with arbitrary-precision arithmetic.

Scope: this certifies the arithmetic only. It does not certify the filtering
moment integrals of Proposition 3.1 (which need real analysis), nor that the
listed quantities are the algorithm's running times. -/
namespace SubsetSum.Audit049Constants

/-! ## Parameters (`η`, `τ`, `Δ`, `Γ`, `a` in units of `10⁻⁵`) -/

def eta : Int := 51772
def tau : Int := 48996
def delta : Int := 2776
def gamma : Int := 46220

/-- `Δ = η - τ` and `Γ = 2τ - η` (equation (3.3)). -/
theorem delta_gamma_def : eta - tau = delta ∧ 2 * tau - eta = gamma := by decide

/-! ## Section 4: checksum estimator -/

/-- Error exponent (4.25): `-τ - Δ + 0.5169 + 48ε = -0.00081952 < -0.0007`
with `ε = 10⁻⁸`, in units of `10⁻⁸`. -/
theorem checksum_error_exponent :
    -tau * 1000 - delta * 1000 + 51690000 + 48 = -81952 ∧ (-81952 : Int) < -70000 := by
  decide

/-- Rounding loss in (4.23): `8.3 (4a + 3) < 30` with `a = Δ/Γ`, i.e.
`83 (4Δ + 3Γ) < 300 Γ`. -/
theorem checksum_rounding : 83 * (4 * delta + 3 * gamma) < 300 * gamma := by decide

/-- Checksum time exponent `τ + 20ε < 0.49`, in units of `10⁻⁸`. -/
theorem checksum_time : tau * 1000 + 20 < 49000000 := by decide

/-! ## Appendix A: final moment comparison -/

/-- `1.4295 · 1.00001 + 0.00007 = 1.429584295` (units of `10⁻⁹`). -/
theorem appendix_sum : 14295 * 100001 + 70000 = 1429584295 := by decide

set_option exponentiation.threshold 200000 in
/-- `1.429584295 < 2^0.5168`, i.e. `1429584295^10000 < 2^5168 · 10^90000`. -/
theorem appendix_moment_threshold :
    1429584295 ^ 10000 < 2 ^ 5168 * 10 ^ 90000 := by decide

set_option exponentiation.threshold 200000 in
/-- The stated enclosure `2^0.5168 > 1.4307781`, i.e.
`14307781^10000 < 2^5168 · 10^70000`. -/
theorem appendix_pow_enclosure :
    14307781 ^ 10000 < 2 ^ 5168 * 10 ^ 70000 := by decide

/-! ## Section 5: alias extraction (`m ≈ 0.0567 n`, `γ_alias = 0.48925`) -/

set_option exponentiation.threshold 200000 in
/-- Binary entropy `h(1/4) = 2 - (3/4) log₂ 3 < 0.81128`, equivalently
`log₂ 3 > 1.58496`, i.e. `2^158496 < 3^100000`. -/
theorem entropy_quarter_lt : 2 ^ 158496 < 3 ^ 100000 := by decide

set_option exponentiation.threshold 200000 in
/-- `h(0.0567) + 0.0567 < 0.40` (Lemma 5.2 vector count). With `x = 567/10000`,
`10000 h(x) = log₂(10000^10000 / (567^567 · 9433^9433))`, so the claim is
`10000^10000 < 2^3433 · 567^567 · 9433^9433`. -/
theorem entropy_sparse_lt :
    10000 ^ 10000 < 2 ^ 3433 * 567 ^ 567 * 9433 ^ 9433 := by decide

/-- Filtered-list exponent (5.8) from `h(1/4) < 0.81128`:
`1/2 + (0.81128 - 1/2 - 0.48925) · 0.0567 = 0.489909101 < 0.48992 < τ`
(units of `10⁻⁹`; the `m` coefficient is negative, so `m ≥ 0.0567n - 2` costs `O(1)`). -/
theorem alias_list_exponent :
    (500000000 : Int) + (81128 - 50000 - 48925) * 567 = 489909101 ∧
      (489909101 : Int) < 489920000 ∧ (489920000 : Int) < tau * 10000 := by
  decide

/-- Visited-pair exponent (5.11) with the bit guard `10⁻⁵`:
`1 - η + (2 · 0.81128 - 1 - 0.48925) · 0.0567 + 0.00001 = 0.489848677 < 0.48988 < τ`. -/
theorem alias_pair_exponent :
    (100000 - eta) * 10000 + (2 * 81128 - 100000 - 48925) * 567 + 10000 = 489848677 ∧
      (489848677 : Int) < 489880000 ∧ (489880000 : Int) < tau * 10000 := by
  decide

/-- Setup work (5.6): `m + max(l,r)/2 ≤ 0.0567 + 0.25 = 0.3067 < τ` (units of `10⁻⁴`). -/
theorem alias_generation_exponent : 567 + 2500 = 3067 ∧ (3067 : Int) * 10 < tau := by decide

/-- Sparse distinctions (Lemma 5.2) union bound: `η - 0.40 - 0.00001 > 0`. -/
theorem sparse_union_margin : (0 : Int) < eta - 40000 - 1 := by decide

/-- Seventeen blocks of size `m/2` fit in `⌊n/2⌋`: `17 · 0.0567 < 1`. -/
theorem seventeen_blocks_fit : 17 * 567 < 10000 := by decide

/-- Markov step (5.15): `1 - 0.01004 / (17 · 0.0106 · 0.0567) > 0.017 > 0.005`,
i.e. `0.01004 < 0.983 · 0.01021734`, scaled to `1004 · 10⁶ < 983 · 1021734`. -/
theorem markov_useful_block :
    17 * 106 * 567 = 1021734 ∧ 1004 * 10 ^ 6 < 983 * 1021734 := by decide

/-- Many weights (5.16): `0.5 - 0.0106 = 0.4894 > γ_alias = 0.48925`. -/
theorem many_weights_exceed_filter : 5000 - 106 = 4894 ∧ 489250 < 4894 * 100 := by decide

/-! ## Section 2: capped preliminary search -/

/-- Chebyshev gap `0.01004 - 0.010025 = 0.000015 > 0`, and the list cap
`1/2 - 0.010025 = 0.489975 < 0.489985 < 0.49` (units of `10⁻⁶`). -/
theorem prelim_cap :
    10040 - 10025 = 15 ∧ 500000 - 10025 = 489975 ∧
      489975 < 489985 ∧ 489985 < 490000 := by
  decide

/-- All-history exponent `0.489995 < 0.49`, covering the preliminary cap
`0.489985` and the checksum/alias bound `τ + 20ε`. -/
theorem all_history_exponent :
    (489985 : Int) < 489995 ∧ tau * 10 + 1 < 489995 ∧ (489995 : Int) < 490000 := by
  decide

end SubsetSum.Audit049Constants
