# R13a: compress-then-MITM beyond toy size

## Part A: solved instances (verified witness)

Structured part: `m` distinct vectors in `[0, L)^d`, random 40-bit generators; `r` random 60-bit decoys; target = a random half of the structured part plus half the decoys. Plain MITM would touch `2^(n/2)` states.

| m | d | L | r | n | core | |Sigma(core)| | compress states | plain MITM 2^(n/2) | ratio | seconds | verified |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |
| 40 | 3 | 4 | 16 | 56 | 40 | 76410 | 154932 | 2.68e+08 | 1.7e+03 | 0 | True |
| 60 | 3 | 4 | 16 | 76 | 60 | 232628 | 322123 | 2.75e+11 | 8.5e+05 | 1 | True |
| 60 | 3 | 4 | 20 | 80 | 60 | 239510 | 828892 | 1.10e+12 | 1.3e+06 | 1 | True |

## Part B: detection at `n = 224` (not solved)

`m = 200` distinct weight-3 vectors in `Z^12`, 64-bit generators, `r = 24` random decoys; relation search took 8 s. The predicted cost uses the box volume as an upper bound on `|Sigma(core)|`; with a full core the remaining random part is only `r` elements.

| s | enumerated | core size | core inside S | coverage of S | log2 Sigma_ub | predicted log2 cost | log2 plain 2^(n/2) |
| ---: | ---: | ---: | :-- | ---: | ---: | ---: | ---: |
| 1 | 224 | 0 | True | 0.00 | 68.1 | 46.0 | 112 |
| 2 | 25200 | 200 | True | 1.00 | 68.1 | 46.0 | 112 |
| 3 | 1873424 | 200 | True | 1.00 | 68.1 | 46.0 | 112 |

## Reading

* Part A: the exact solver finds a verified witness at `n = 56, 76, 80`, where plain meet-in-the-middle would need `2^28 .. 2^40` states, using `1.5e5 .. 8.3e5`: a `1.7e3 .. 1.3e6` fold reduction. The reduction is large because the structured part is rank 3 with `|Sigma|` about `2^18`, not because the method touches a hard instance.
* Part B: at `n = 224` the `s = 2` relation search (about `25 000` subsets) already returns exactly the 200 structured elements and no decoy (the noise threshold for 64-bit decoys is far above `s = 3`). The predicted cost `2^46` against `2^112` is an estimate from the box volume, not a run.
* Honest scope. These supports have a small-doubling structured part (rank `d` far below `m`). With only `r` random decoys the whole set has doubling bounded by a constant times `r`, which is the regime of the small-doubling algorithms of Randolph-Wegrzycki (doubly exponential constants in theory). So this shows a practical exact solver and detector for structured-plus-random inputs, not an advance on the hard band, where no sub-collection is compressible.
