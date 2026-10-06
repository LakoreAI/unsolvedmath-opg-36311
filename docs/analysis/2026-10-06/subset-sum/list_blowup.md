# R13: filtered-list blow-up on structured inputs

`ratio = |Y_r| / E` where `Y_r` is the balanced weight-`n/4` sub-solver output for a random prime `M in [P, 2P]` (`P = C(n/4,n/8)^2`) and a random residue, and `E = C(n/2,n/8)^2 / M` its expectation on random inputs. Ratio `~1` = no blow-up; a large mean or max ratio is a cost the disjointness step must absorb.

| n | family | E = ambient/M | mean ratio | max ratio |
| ---: | :-- | ---: | ---: | ---: |
| 24 | random-b1.0 | 62.9 | 1.01 | 1.3 |
| 24 | random-b1.5 | 62.9 | 1.02 | 1.2 |
| 24 | geometric | 83.9 | 1.01 | 1.2 |
| 24 | arithmetic-large | 83.9 | 0.90 | 19.5 |
| 24 | two-scale | 70.9 | 1.01 | 1.3 |
| 24 | gap-rank2 | 95.1 | 1.03 | 1.8 |
| 24 | q-multiple | 115.5 | 0.99 | 1.3 |
| 24 | near-ap | 65.5 | 1.34 | 8.8 |
| 24 | mod-cluster | 70.9 | 0.95 | 1.3 |
| 32 | random-b1.0 | 466.3 | 1.00 | 1.1 |
| 32 | random-b1.5 | 386.4 | 1.01 | 1.1 |
| 32 | geometric | 647.1 | 1.00 | 1.2 |
| 32 | arithmetic-large | 647.1 | 0.00 | 0.0 |
| 32 | two-scale | 397.7 | 1.00 | 1.1 |
| 32 | gap-rank2 | 661.0 | 1.02 | 1.8 |
| 32 | q-multiple | 661.0 | 1.13 | 2.8 |
| 32 | near-ap | 463.2 | 0.00 | 0.0 |
| 32 | mod-cluster | 488.6 | 1.02 | 1.1 |
| 40 | random-b1.0 | 2955.5 | 1.00 | 1.0 |
| 40 | random-b1.5 | 2955.5 | 0.99 | 1.0 |
| 40 | geometric | 3308.8 | 1.01 | 1.0 |
| 40 | arithmetic-large | 2060.1 | 0.00 | 0.0 |
| 40 | two-scale | 2484.2 | 1.00 | 1.0 |
| 40 | gap-rank2 | 3766.3 | 1.12 | 6.9 |
| 40 | q-multiple | 3612.4 | 1.01 | 1.0 |
| 40 | near-ap | 3705.4 | 0.00 | 0.0 |
| 40 | mod-cluster | 2591.5 | 1.00 | 1.0 |
