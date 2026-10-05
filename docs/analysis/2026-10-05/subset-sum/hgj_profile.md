# R13: the profile barrier of the balanced sub-solver

Planted weight-`n/2` solutions with `share` elements in the first half (`share = n/4` is balanced). `no perm` is the success rate with the input's natural contiguous halves; `perm` is after one random permutation of the values (the target is unchanged). A concentrated solution has no balanced representation, so the balanced sub-solver misses it and wrongly answers ``no''; a permutation only repairs it with the probability that the solution lands balanced.

| n | first-half share | no perm success | perm success |
| ---: | ---: | ---: | ---: |
| 32 | 0 | 0.00 | 0.50 |
| 32 | 2 | 0.00 | 0.00 |
| 32 | 4 | 0.00 | 0.00 |
| 32 | 8 | 1.00 | 0.50 |
| 40 | 0 | 0.00 | 0.25 |
| 40 | 2 | 0.00 | 0.50 |
| 40 | 5 | 0.00 | 0.25 |
| 40 | 10 | 1.00 | 0.50 |
| 48 | 0 | 0.00 | 0.25 |
| 48 | 3 | 0.00 | 0.25 |
| 48 | 6 | 0.00 | 0.25 |
| 48 | 12 | 1.00 | 0.00 |

## Cost of completeness

The balanced profile alone costs `C(n/2, n/8)^2 = 2^(0.4057n)` and is incomplete. Enumerating every weight profile `i + j = n/4` costs `sum_i C(n/2,i) C(n/2,n/4-i) = C(n, n/4) = 2^(0.811n)`, above meet-in-the-middle. Broadening the representations (overlaps) is what recovers completeness below `2^(n/2)`.

| n | balanced profile e | all profiles e | meet-in-the-middle e |
| ---: | ---: | ---: | ---: |
| 32 | 0.3697 | 0.7289 | 0.5000 |
| 40 | 0.3730 | 0.7415 | 0.5000 |
| 48 | 0.3758 | 0.7504 | 0.5000 |
