# R13a: compressible supports versus their shortest relation

`s*` is the smallest size at which two distinct subsets of the support have equal sums (a relation with `|P|, |Q| <= s*`), searched up to the budget shown. `s_b` is the birthday prediction from the box volume `V_s` (sizes from 2, since elements are distinct; an upper bound on reachable sum vectors, so `s_b` errs late). The adversary wants `compressible = yes` together with a large `s*`.

| family | m | d | L or p | log2 Sigma(S) | m/2 | compressible | s* | birthday s_b |
| :-- | ---: | ---: | ---: | ---: | ---: | :-- | :-- | ---: |
| random box | 30 | 3 | 4 | 14.8 | 15 | yes | 2 | 2 |
| random box | 30 | 4 | 3 | 17.3 | 15 | no | 2 | 2 |
| random box | 30 | 6 | 2 | 19.4 | 15 | no | 2 | 2 |
| vandermonde | 30 | 3 | 31 | 18.8 | 15 | no | 3 | 3 |
| vandermonde | 30 | 4 | 31 | > 22 | 15 | no (>2^22) | 4 | 4 |
| vandermonde | 30 | 5 | 31 | > 22 | 15 | no (>2^22) | 5 | >6 |
| random box | 40 | 3 | 4 | 16.0 | 20 | yes | 2 | 2 |
| random box | 40 | 4 | 3 | 18.7 | 20 | yes | 2 | 2 |
| random box | 40 | 6 | 2 | > 22 | 20 | no (>2^22) | 2 | 2 |
| vandermonde | 40 | 3 | 41 | 21.3 | 20 | no | 3 | 3 |
| vandermonde | 40 | 4 | 41 | > 22 | 20 | no (>2^22) | 4 | 4 |
| vandermonde | 40 | 5 | 41 | > 22 | 20 | no (>2^22) | 5 | 6 |
| random box | 60 | 3 | 4 | 17.9 | 30 | yes | 2 | 2 |
| random box | 60 | 4 | 3 | 21.0 | 30 | yes | 2 | 2 |
| random box | 60 | 6 | 2 | > 22 | 30 | no (>2^22) | 2 | 2 |
| vandermonde | 60 | 3 | 61 | > 22 | 30 | no (>2^22) | 3 | 3 |
| vandermonde | 60 | 4 | 61 | > 22 | 30 | no (>2^22) | 4 | 4 |
| vandermonde | 60 | 5 | 61 | > 22 | 30 | no (>2^22) | > 4 | 5 |

## Reading

* Every compressible support found (random boxes) has `s* = 2`: compressibility comes with very short relations at these sizes.
* Vandermonde (MDS) columns guarantee `s* >= d + 1` and the measured `s*` equals `d + 1` or more, but none of them is compressible here: their sum ranges `(mp)^d` exceed `2^{m/2}`. Guaranteed-length algebraic constructions pay for their long relations with large sum sets.
* The birthday prediction errs late (it uses the box volume), consistent with random-like structure colliding early.
