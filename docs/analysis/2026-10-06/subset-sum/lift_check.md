# R13: single-prime coverage under the distinct-sums hypothesis

`Y = C(n/2, n/4)` representations of a planted weight-`n/2` support; `D` the number of distinct weight-`n/4` sub-sums; window `p in [M, 2M]` with `M` the power of two `>= 4D`. `bound` is the `LIFT.md` lower bound `1/(1 + D B / pi)` on mean coverage per distinct sum. The bound is a lower bound, so `mean cover/D >= bound` must hold.

| n | family | Y | D | D/Y | M | mean cover/D | bound | min cover/D |
| ---: | :-- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | random-b1.0 | 924 | 924 | 1.000 | 4096 | 0.925 | 0.190 | 0.680 |
| 24 | random-b1.5 | 924 | 924 | 1.000 | 4096 | 0.927 | 0.137 | 0.587 |
| 24 | geometric | 924 | 924 | 1.000 | 4096 | 0.932 | 0.201 | 0.509 |
| 24 | arithmetic-large | 924 | 83 | 0.090 | 512 | 1.000 | 0.306 | 1.000 |
| 24 | two-scale | 924 | 924 | 1.000 | 4096 | 0.923 | 0.103 | 0.364 |
| 24 | gap-rank2 | 924 | 916 | 0.991 | 4096 | 0.942 | 0.278 | 0.648 |
| 24 | q-multiple | 924 | 908 | 0.983 | 4096 | 0.942 | 0.252 | 0.144 |
| 28 | random-b1.0 | 3432 | 3432 | 1.000 | 16384 | 0.930 | 0.185 | 0.631 |
| 28 | random-b1.5 | 3432 | 3432 | 1.000 | 16384 | 0.931 | 0.130 | 0.675 |
| 28 | geometric | 3432 | 3432 | 1.000 | 16384 | 0.937 | 0.191 | 0.695 |
| 28 | arithmetic-large | 3432 | 95 | 0.028 | 512 | 1.000 | 0.263 | 1.000 |
| 28 | two-scale | 3432 | 3432 | 1.000 | 16384 | 0.930 | 0.093 | 0.663 |
| 28 | gap-rank2 | 3432 | 3284 | 0.957 | 16384 | 0.942 | 0.275 | 0.632 |
| 28 | q-multiple | 3432 | 3348 | 0.976 | 16384 | 0.941 | 0.246 | 0.231 |
