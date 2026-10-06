# R13: single-prime coverage under the distinct-sums hypothesis

`Y = C(n/4, n/8)^2` balanced representations of a planted weight-`n/2` support; `D = D*` the number of distinct sums of balanced weight-`n/4` sub-sets (`n/8` from each half of the support); window `p in [M, 2M]` with `M` the power of two `>= 4D`. `bound` is the `LIFT.md` lower bound `1/(1 + D B / pi)` on mean coverage per distinct sum. The bound is a lower bound, so `mean cover/D >= bound` must hold.

| n | family | Y | D | D/Y | M | mean cover/D | bound | min cover/D |
| ---: | :-- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | random-b1.0 | 400 | 400 | 1.000 | 2048 | 0.942 | 0.215 | 0.610 |
| 24 | random-b1.5 | 400 | 400 | 1.000 | 2048 | 0.933 | 0.156 | 0.690 |
| 24 | geometric | 400 | 400 | 1.000 | 2048 | 0.939 | 0.226 | 0.770 |
| 24 | arithmetic-large | 400 | 75 | 0.188 | 512 | 1.000 | 0.328 | 1.000 |
| 24 | two-scale | 400 | 400 | 1.000 | 2048 | 0.938 | 0.118 | 0.780 |
| 24 | gap-rank2 | 400 | 400 | 1.000 | 2048 | 0.938 | 0.311 | 0.600 |
| 24 | q-multiple | 400 | 396 | 0.990 | 2048 | 0.944 | 0.282 | 0.535 |
| 32 | random-b1.0 | 4900 | 4900 | 1.000 | 32768 | 0.950 | 0.216 | 0.689 |
| 32 | random-b1.5 | 4900 | 4900 | 1.000 | 32768 | 0.950 | 0.157 | 0.700 |
| 32 | geometric | 4900 | 4900 | 1.000 | 32768 | 0.952 | 0.227 | 0.717 |
| 32 | arithmetic-large | 4900 | 88 | 0.018 | 512 | 1.000 | 0.261 | 1.000 |
| 32 | two-scale | 4900 | 4900 | 1.000 | 32768 | 0.950 | 0.118 | 0.690 |
| 32 | gap-rank2 | 4900 | 4748 | 0.969 | 32768 | 0.956 | 0.327 | 0.566 |
| 32 | q-multiple | 4900 | 4884 | 0.997 | 32768 | 0.952 | 0.291 | 0.432 |
