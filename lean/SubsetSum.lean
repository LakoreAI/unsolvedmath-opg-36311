import SubsetSum.Basic
import SubsetSum.Witness
import SubsetSum.Reductions
import SubsetSum.Representation
import SubsetSum.SharedMask
import SubsetSum.HighEnergy
import SubsetSum.Audit049

/-! # Exact Subset Sum Research — Root Module

Re-exports the modular Lean 4.19.0 correctness layer:
- `SubsetSum.Basic`: `HasSum`, two- and three-block splits, `meetInMiddle`, `threeBlock`,
  and bounded-magnitude radius lemmas.
- `SubsetSum.Witness`: Boolean occurrence-mask semantics and `meetInMiddleWitness`.
- `SubsetSum.Reductions`: signed-to-nonnegative/positive reductions and the
  tie-breaking solution isolation family.
- `SubsetSum.Representation`: weight-resolved certificates (`HasSumWeight`),
  modular filter completeness (`mem_residues`), mixing concentration/contraction,
  collision-energy decomposition (`collision_energy_split`), and impossibility of
  coefficient shifting for `{0,1}` and `{-1,1}` (`no_coefficient_shifting_01`,
  `no_coefficient_shifting_pm1`).
- `SubsetSum.SharedMask`: disjoint-mask compatibility, shared-block 3-split
  (`sharedMaskSolve`), and modular alias subtraction (`modBin_alias_subtraction`).
- `SubsetSum.HighEnergy`: common-element stripping for colliding subsets
  (`diffMask`, `lemma_T_forced_disjoint_relation`), scaled-geometric transfer
  barrier (`maskSum_scaled_geomWeights_inj`), discrete Cauchy-Schwarz collision
  energy (`sq_sum_le_length_mul_sumSq`), weight-slice sumset profiles
  (`sliceProfile`), compressible-core MITM (`compressMitm`), HGJ modular-filter
  solver (`hgjSolve`), and PESS crowded-interval halving (`pess_crowded_halving`).
- `SubsetSum.Audit049`: high/low-digit decomposition (`maskSum_high_low_split`),
  capped preliminary search (`cappedPrelimSolve`), and end-to-end isolated
  alias-subtraction decision (`isolated_alias_decision_iff`). -/
namespace SubsetSum

#eval meetInMiddle [3, -2] [7, 0] 5
#eval meetInMiddle [2, 4] [8] 7
#eval meetInMiddleWitness [3, -2] [7, 0] 5
#eval sharedMaskSolve [3] [-2, 7] [0] 5
#eval compressMitm [1, 2, 3] [10] [20] 16
#eval hgjSolve [3, 5, 8, 13, 21, 34] 2 6 66 0
#eval cappedPrelimSolve 8 [1, 2, 3] [10, 20] 16
#eval residues 4 [1, 2, 3]
#eval sliceProfile [1, 2, 3, 10, 11, 12]

#print axioms mem_sums_iff
#print axioms sums_length
#print axioms hasSum_append
#print axioms hasSum_append3
#print axioms meetInMiddle_correct
#print axioms threeBlock_correct
#print axioms meetInMiddleWitness_sound
#print axioms meetInMiddleWitness_isSome_iff
#print axioms hasSum_signed_iff_nonneg
#print axioms hasSum_signed_iff_pos
#print axioms isolation_mask_iff
#print axioms isolation_hasSum_iff
#print axioms isolation_unique_mask
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
#print axioms residue_collision_iff
#print axioms collision_energy_split
#print axioms no_coefficient_shifting_01
#print axioms no_coefficient_shifting_pm1
#print axioms maskSum_orMask_of_disjoint
#print axioms sharedMaskSolve_sound
#print axioms sharedMaskSolve_isSome_iff
#print axioms modBin_alias_subtraction
#print axioms masksDisjoint_diffMask
#print axioms maskSum_diffMask_eq_iff
#print axioms diffMask_ne_of_ne
#print axioms lemma_T_forced_disjoint_relation
#print axioms maskSum_scaled_geomWeights_inj
#print axioms sq_sum_le_length_mul_sumSq
#print axioms compressMitm_correct
#print axioms hgjSolve_sound
#print axioms hgjSolve_isSome_of_representation
#print axioms pess_crowded_halving
#print axioms maskSum_high_low_split
#print axioms cappedPrelimSolve_sound
#print axioms isolated_alias_decision_iff

end SubsetSum
