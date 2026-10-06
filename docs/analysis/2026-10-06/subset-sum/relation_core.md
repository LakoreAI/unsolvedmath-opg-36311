# R13a: short-relation core of a low-rank support

Relations = equal-sum pairs of distinct subsets of size `<= s` among all `n` inputs, common elements removed. `core` is the union of elements in some relation; `core inside S` says no decoy ever appears (the signal is pure structure); `coverage` is the fraction of the hidden support `S` reached.

| family | n | d | s | enumerated | core size | core inside S | coverage of S |
| :-- | ---: | ---: | ---: | ---: | ---: | :-- | ---: |
| distinct | 24 | 7 | 1 | 24 | 0 | True | 0.00 |
| distinct | 24 | 7 | 2 | 300 | 11 | True | 0.92 |
| distinct | 24 | 7 | 3 | 2324 | 12 | True | 1.00 |
| distinct | 24 | 7 | 4 | 12950 | 16 | False | 1.00 |
| distinct | 24 | 7 | 5 | 55454 | 16 | False | 1.00 |
| distinct | 24 | 8 | 1 | 24 | 0 | True | 0.00 |
| distinct | 24 | 8 | 2 | 300 | 7 | True | 0.58 |
| distinct | 24 | 8 | 3 | 2324 | 12 | True | 1.00 |
| distinct | 24 | 8 | 4 | 12950 | 17 | False | 1.00 |
| distinct | 24 | 8 | 5 | 55454 | 17 | False | 1.00 |
| distinct | 24 | 10 | 1 | 24 | 0 | True | 0.00 |
| distinct | 24 | 10 | 2 | 300 | 4 | True | 0.33 |
| distinct | 24 | 10 | 3 | 2324 | 4 | True | 0.33 |
| distinct | 24 | 10 | 4 | 12950 | 4 | True | 0.33 |
| distinct | 24 | 10 | 5 | 55454 | 16 | False | 0.75 |
| distinct | 32 | 10 | 1 | 32 | 0 | True | 0.00 |
| distinct | 32 | 10 | 2 | 528 | 12 | True | 0.75 |
| distinct | 32 | 10 | 3 | 5488 | 14 | True | 0.88 |
| distinct | 32 | 10 | 4 | 41448 | 14 | True | 0.88 |
| distinct | 32 | 12 | 1 | 32 | 0 | True | 0.00 |
| distinct | 32 | 12 | 2 | 528 | 0 | True | 0.00 |
| distinct | 32 | 12 | 3 | 5488 | 6 | True | 0.38 |
| distinct | 32 | 12 | 4 | 41448 | 12 | True | 0.75 |
| gap | 32 | 8 | 1 | 32 | 2 | True | 0.12 |
| gap | 32 | 8 | 2 | 528 | 6 | True | 0.38 |
| gap | 32 | 8 | 3 | 5488 | 15 | True | 0.94 |
| gap | 32 | 8 | 4 | 41448 | 15 | True | 0.94 |
