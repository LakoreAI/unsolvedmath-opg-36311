# R13a: is |Sigma_k| maximized at the middle size? (Conjecture U)

`ratio = max_k |Sigma_k(X)| / |Sigma_{m/2}(X)|`. Conjecture U asks for `ratio <= poly(m)`; the counts need not be unimodal (a ratio slightly above 1 appears at `m = 8`), but no search found the middle count far from the maximum.

| m | search | sets tried | worst ratio | counts at worst |
| ---: | :-- | ---: | ---: | :-- |
| 8 | random/structured | 3000 | 1.032 | [1, 8, 23, 32, 31, 32, 23, 8, 1] |
| 10 | random/structured | 3000 | 1.023 | [1, 10, 25, 38, 44, 43, 44, 38, 25, 10, 1] |
| 12 | random/structured | 3000 | 1.010 | [1, 12, 45, 70, 89, 102, 101, 102, 89, 70, 45, 12, 1] |
| 8 | hill-climb x4 | 6000 | 1.000 | [1, 8, 28, 56, 70, 56, 28, 8, 1] |
| 10 | hill-climb x4 | 6000 | 1.000 | [1, 10, 44, 114, 195, 232, 195, 114, 44, 10, 1] |
| 12 | hill-climb x4 | 6000 | 1.000 | [1, 9, 32, 66, 96, 115, 122, 115, 96, 66, 32, 9, 1] |
| 14 | hill-climb x4 | 6000 | 1.000 | [1, 12, 67, 232, 561, 1012, 1419, 1584, 1419, 1012, 561, 232, 67, 12, 1] |

## Analytic families at larger m

The two-AP family is the one on which the hill-climb found dips; its worst middle-to-maximum ratio tends to 1 as `m` grows (`0.946` at `m = 12`, `0.998` at `m = 400`).

| family | m | min over parameters of |Sigma_mid| / max_k |Sigma_k| |
| :-- | ---: | ---: |
| two APs with a gap (dips at the middle) | 12 | 0.9464 |
| two APs with a gap (dips at the middle) | 20 | 0.9593 |
| two APs with a gap (dips at the middle) | 40 | 0.9771 |
| two APs with a gap (dips at the middle) | 100 | 0.9906 |
| two APs with a gap (dips at the middle) | 200 | 0.9952 |
| two APs with a gap (dips at the middle) | 400 | 0.9976 |
| AP plus dissociated block | 20 | 1.0000 |
| AP plus dissociated block | 60 | 1.0000 |
| AP plus dissociated block | 120 | 1.0000 |
| AP plus dissociated block | 400 | 1.0000 |

Literature check (2026-10-06): no theorem on unimodality or middle-dominance of restricted sumset sizes `|k^ X|` in `k` was found; the nearest work studies the range of sumset sizes `R(h,k)` (arXiv 2505.07679, 2510.23022) and inverse theorems for restricted sumsets (arXiv 2505.07415), which answer different questions. Conjecture U remains open here.
