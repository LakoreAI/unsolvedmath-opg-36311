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
