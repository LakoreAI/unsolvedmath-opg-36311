# H1: balanced representations under random partitions

A planted weight-n/2 solution, 200 random equipartitions. A partition is
balanced if it admits at least one representation with n/8 ones on each
side. `total` is the number of representations before balancing (2^(n/2)).

| n | partitions with balance | min reps | median reps | median log2 | total log2 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 32 | 200/200 | 495 | 4410 | 12.11 | 16 |
| 48 | 200/200 | 18564 | 792792 | 19.6 | 24 |
| 64 | 200/200 | 14389650 | 156434850 | 27.22 | 32 |
| 96 | 200/200 | 873253808700 | 7031211223400 | 42.68 | 48 |

Reading: random partitions supply a balanced representation with
probability approaching 1, and retain 2^(n/2 - O(log n)) of the
representations. Balancing is therefore a randomization problem, not a
structural obstruction — supporting H1. The remaining obstruction is
whether *enough* representations exist at all (H2).
