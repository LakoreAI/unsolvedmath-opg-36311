# R13a: greedy core growth at larger n with adversarial decoys

`core` is the size of the chosen compressed set and `core in support` how many of its elements belong to the structured support (`mitm` if no compressible prefix was found).

| m | d | L | decoys | n | core | core in support | |Sigma(core)| | states | plain 2^(n/2) | seconds | verified |
| ---: | ---: | ---: | :-- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |
| 40 | 3 | 4 | random | 56 | 40 | 40/40 | 65662 | 145319 | 2.7e+08 | 2 | True |
| 40 | 3 | 4 | shifted | 56 | 41 | 37/41 | 484552 | 632989 | 2.7e+08 | 4 | True |
| 60 | 3 | 4 | random | 80 | 60 | 60/60 | 242274 | 842433 | 1.1e+12 | 4 | True |
| 60 | 3 | 4 | shifted | 80 | 61 | 60/61 | 483968 | 987230 | 1.1e+12 | 4 | True |
| 150 | 2 | 13 | random | 180 | 150 | 150/150 | 441251 | 21662072 | 1.2e+27 | 16 | True |
| 150 | 2 | 13 | shifted | 180 | 154 | 150/154 | 3810400 | 23878374 | 1.2e+27 | 21 | True |

## Reading

* Every instance is solved with a verified witness, up to `n = 180` (plain MITM would need `1.2e27` states; greedy growth used `2.2e7-2.4e7`).
* `shifted` decoys, which defeated the relation-component solver at `n = 32`, are almost entirely kept out of the core (`37/41`, `60/61`, `150/154` of the chosen elements are support).
* Scope: these supports have small doubling (rank 2-3), the regime of known small-doubling algorithms. The run shows the detector and solver scale and survive this decoy attack; it says nothing about supports without compressible structure.
