# R13: HGJ filter + sub-solver on adversarial families

Planted balanced solutions; up to 16 residue attempts. `success` is the fraction solved, `cov avg`/`cov min` the representation coverage over several primes, `work` the mean enumeration (the sub-solver baseline is `2*C(n/2,n/8) = 2^0.4057n`; MITM is `0.5`). Prediction: hard families mix (coverage `~0.5`) and succeed; low-coverage families are structured, not hard.

| n | family | success | cov avg | cov min | work | baseline |
| ---: | :-- | ---: | ---: | ---: | ---: | ---: |
| 24 | random-b1.0 | 1.00 | 0.909 | 0.848 | 5.133e+02 | 440 |
| 24 | random-b1.5 | 1.00 | 0.869 | 0.681 | 5.133e+02 | 440 |
| 24 | geometric | 0.67 | 0.923 | 0.830 | 3.080e+03 | 440 |
| 24 | arithmetic-large | 0.83 | 0.165 | 0.152 | 2.288e+03 | 440 |
| 24 | two-scale | 1.00 | 0.914 | 0.843 | 5.133e+02 | 440 |
| 24 | gap-rank2 | 1.00 | 0.869 | 0.748 | 4.400e+02 | 440 |
| 24 | q-multiple | 1.00 | 0.899 | 0.845 | 4.400e+02 | 440 |
| 32 | random-b1.0 | 1.00 | 0.921 | 0.901 | 6.673e+03 | 3640 |
| 32 | random-b1.5 | 1.00 | 0.927 | 0.907 | 4.853e+03 | 3640 |
| 32 | geometric | 0.33 | 0.944 | 0.924 | 2.184e+04 | 3640 |
| 32 | arithmetic-large | 0.00 | 0.025 | 0.023 | — | 3640 |
| 32 | two-scale | 1.00 | 0.907 | 0.844 | 4.853e+03 | 3640 |
| 32 | gap-rank2 | 1.00 | 0.915 | 0.845 | 3.640e+03 | 3640 |
| 32 | q-multiple | 1.00 | 0.931 | 0.905 | 3.640e+03 | 3640 |
| 40 | random-b1.0 | 1.00 | 0.947 | 0.936 | 3.618e+04 | 31008 |
| 40 | random-b1.5 | 1.00 | 0.948 | 0.912 | 3.618e+04 | 31008 |
| 40 | geometric | 0.17 | 0.936 | 0.846 | 2.791e+05 | 31008 |
| 40 | arithmetic-large | 0.33 | 0.003 | 0.003 | 2.171e+05 | 31008 |
| 40 | two-scale | 1.00 | 0.942 | 0.930 | 4.651e+04 | 31008 |
| 40 | gap-rank2 | 1.00 | 0.914 | 0.750 | 3.101e+04 | 31008 |
| 40 | q-multiple | 1.00 | 0.946 | 0.922 | 3.101e+04 | 31008 |
