# R13a: the high-energy regime

Planted weight-`n/2` solutions whose support is a rank-`d` GAP (random `n`-bit generators, coordinates in `[0, L)`), with random `n`-bit decoys elsewhere. `pred exp` is the LIFT.md exponent `max(0.4057, log2(C(n,n/4)/D)/n)` capped at `0.5`. `work` is total enumerated subsets of `hgj_permuted_search` (budget `8 sqrt n` permutations x 8 residues) with modulus `~4D` and with the default `~2^(n/2)` modulus; a `>` marks a run that did not find the solution. `core` is the number of elements in some additive quadruple `a_i + a_j = a_k + a_l`.

| n | d | L | D | Y | D/Y | pred exp | work (M~4D) | work (default M) | MITM | core | support in core |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |
| 24 | 2 | 2 | 20 | 924 | 0.02 | 0.500 | 5.28e+03 | 1.10e+05 | 4.1e+03 | 12 | True |
| 24 | 3 | 2 | 62 | 924 | 0.07 | 0.462 | 1.85e+04 | 7.30e+04 | 4.1e+03 | 12 | True |
| 24 | 4 | 2 | 148 | 924 | 0.16 | 0.410 | 4.40e+02 | >1.4e+05 | 4.1e+03 | 11 | False |
| 24 | 6 | 2 | 538 | 924 | 0.58 | 0.406 | 4.40e+03 | 5.19e+04 | 4.1e+03 | 10 | False |
| 32 | 3 | 2 | 168 | 12870 | 0.01 | 0.498 | 1.09e+04 | >1.3e+06 | 6.6e+04 | 16 | True |
| 32 | 4 | 2 | 522 | 12870 | 0.04 | 0.447 | 9.10e+04 | >1.3e+06 | 6.6e+04 | 16 | True |
| 32 | 6 | 2 | 3260 | 12870 | 0.25 | 0.406 | 1.89e+05 | 4.66e+05 | 6.6e+04 | 16 | True |
| 32 | 8 | 2 | 7642 | 12870 | 0.59 | 0.406 | 4.59e+05 | 2.29e+05 | 6.6e+04 | 4 | False |

## Reading

* `D/Y` falls from `0.59` to `0.01-0.07` as the rank `d` drops, so these are genuine
  high-energy supports; the LIFT.md exponent rises toward `0.5` (MITM) as `D/Y` falls.
* Whenever the rank is small (`d <= 6` at `n = 32`, `d <= 3` at `n = 24`) the additive
  quadruple core is exactly the support (`core = n/2`, no decoy elements), so random decoys
  create **no** spurious relations and meet-in-the-middle on the core costs `2^(n/4)`.
* For the largest rank listed (`d = 8` at `n = 32`, `D/Y = 0.59`) the quadruple core misses
  the support: relations among the support are longer than 4 terms.
* The `n = 24, d = 4` small-modulus run (work `440`, a single attempt) is a first-attempt hit
  (probability `~ D/M` per attempt times the balanced-permutation chance), not evidence against
  the `LIFT.md` bound, which is an *expected* cost.
* Toy `n` cannot realize the hard case "Sidon-like yet low-rank": see `relation_length.md` and
  `HIGH_ENERGY.md` for why it only exists for `n` in the hundreds.
