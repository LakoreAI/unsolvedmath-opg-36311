# R13a: relation-lattice detection of a low-rank support

Support values in a rank-`d` GAP (side 2) with random `n`-bit generators, decoys random `n`-bit. `inside S` counts reduced-basis vectors whose support is contained in the hidden support. `of the shortest (m-d)` is how many of the `m-d` shortest reduced vectors lie inside `S`. A `*` marks the distinct-vector family (distinct weight-3 vectors, so no duplicate or zero elements and no trivial norm-1 or norm-2 relations).

| n | rank d | S-relations expected (m-d) | reduced vectors inside S | of the shortest (m-d) | min norm^2 inside S | min norm^2 outside S | sec |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 2 | 6 | 6 | 6/6 | 1 | 14 | 2 |
| 16 | 3 | 5 | 5 | 5/5 | 1 | 11 | 3 |
| 16 | 8 | 0 | 1 | 0/0 | 2 | 7 | 4 |
| 24 | 3 | 9 | 9 | 9/9 | 1 | 13 | 28 |
| 24 | 4 | 8 | 8 | 8/8 | 2 | 12 | 32 |
| 24 | 12 | 0 | 0 | 0/0 | - | 9 | 31 |
| 16 | 5* | 3 | 3 | 3/3 | 4 | 7 | 4 |
| 16 | 6* | 2 | 2 | 2/2 | 4 | 9 | 4 |
| 24 | 7* | 5 | 5 | 5/5 | 4 | 8 | 33 |
| 24 | 8* | 4 | 2 | 2/4 | 4 | 12 | 26 |
| 24 | 10* | 2 | 0 | 0/2 | - | 9 | 29 |

## Reading

* With duplicate or zero elements (rows without `*`) the support-internal relations have norm 1-2 and LLL finds every one of them: trivially easy.
* With distinct vectors (`*`) LLL still isolates all `m-d` support relations while they are shorter than generic lattice vectors (`n = 24`, `d = 7`: norm^2 4 vs 8). As `d` grows the support relations lengthen; at `d = 8` only 2 of 4 are found inside `S` and at `d = 10` none (their norm no longer beats the generic shortest relations, norm^2 about 9).
* The generic shortest relation of `n` random `n`-bit numbers has norm^2 `Theta(n)`; a support relation of length `Theta(n)` (exactly the forced-relation scale of `HIGH_ENERGY.md`) is not shorter. So lattice reduction detects the easy corner and meets the shortest-vector barrier in the hard corner (an approximation factor `2^{Theta(n)}` is too coarse).
