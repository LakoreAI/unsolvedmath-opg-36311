# R21: do cheap collisions multiply solutions?

Planted weight-n/2 solution; collisions collected by the R20 class sampler with a budget of `2^(n/2)` samples. Means over inputs with at least one collision. `support` is the fraction of nonzero entries of a collision vector; `compatible` counts collisions usable on the planted solution; `solutions` is the exact number of subsets with the target sum.

| n | beta | inputs | found | support | compatible | solutions |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 0.9 | 5 | 16.0 | 0.506 | 1.00 | 3.0 |
| 16 | 1.0 | 5 | 7.2 | 0.560 | 0.00 | 1.0 |
| 16 | 1.1 | 5 | 2.0 | 0.550 | 0.00 | 1.2 |
| 20 | 0.9 | 5 | 46.2 | 0.501 | 0.20 | 1.6 |
| 20 | 1.0 | 5 | 16.2 | 0.527 | 0.20 | 1.6 |
| 20 | 1.1 | 5 | 7.4 | 0.516 | 0.00 | 1.0 |
| 24 | 0.9 | 5 | 128.4 | 0.500 | 0.20 | 1.6 |
| 24 | 1.0 | 5 | 43.0 | 0.508 | 0.00 | 1.2 |
| 24 | 1.1 | 5 | 15.2 | 0.536 | 0.00 | 1.0 |
