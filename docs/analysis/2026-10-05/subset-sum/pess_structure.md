# R16: cost of the structured close-pair search

Base-2 exponents per `n` of the branch-and-bound node count (`visit e`) and of the number of close pairs `(X, Y)` (`pairs e`), for a near-geometric PESS instance (`1, 2, 4, ..., 2^(n-1)` with the top element reduced by 1) and a collision-heavy dense instance of weights in `[1, 4]`. `k` is the prefix cutoff. A near-zero `visit e` on the geometric family is the structured regime the `O*(2^(n/3))` algorithm relies on; the dense family is where it must subsample instead.

| n | k | family | visit e | pairs e |
| ---: | ---: | :-- | ---: | ---: |
| 16 | 5 | geometric | 0.410 | 0.000 |
| 16 | 5 | dense | 1.103 | 0.981 |
| 16 | 8 | geometric | 0.379 | 0.000 |
| 16 | 8 | dense | 0.823 | 0.714 |
| 19 | 6 | geometric | 0.358 | 0.000 |
| 19 | 6 | dense | 1.099 | 1.000 |
| 19 | 9 | geometric | 0.337 | 0.000 |
| 19 | 9 | dense | 0.865 | 0.780 |
| 22 | 7 | geometric | 0.319 | 0.000 |
| 22 | 7 | dense | 1.086 | 0.999 |
| 22 | 11 | geometric | 0.298 | 0.000 |
| 22 | 11 | dense | 0.818 | 0.744 |
