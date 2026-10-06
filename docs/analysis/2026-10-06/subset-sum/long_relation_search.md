# R13a: adversarial search for compressible sets with only long relations

Sets of `m` distinct integers below `R`, so `|Sigma| <= mR < 2^{m/2}` (compressible). `s*` = smallest size with two equal-sum subsets (searched up to `4`; `5` means none found). The annealer maximizes `s*`.

| m | R (values < R) | log2(mR) vs m/2 | pigeonhole s | birthday s | random s* | annealed best s* | collisions at s* | Sidon s* (range) |
| ---: | ---: | :-- | ---: | ---: | ---: | ---: | ---: | :-- |
| 24 | 42 | 10.0 vs 12 | 2 | 2 | 2 | 2 | 533 | 3 (1682, too wide) |
| 32 | 512 | 14.0 vs 16 | 3 | 2 | 2 | 2 | 120 | 3 (2738, too wide) |
| 36 | 1820 | 16.0 vs 18 | 3 | 2 | 2 | 2 | 44 | 3 (2738, too wide) |
| 40 | 6553 | 18.0 vs 20 | 4 | 2 | 2 | 2 | 20 | 3 (3362, fits) |

## Reading

* Annealing never pushed `s*` above 2, though the colliding pairs at `s = 2` fell from hundreds to about 20 as `m` grew: a weak search, not a proof.
* An explicit Sidon set (Erdos-Turan) has `s* >= 3`; it fits inside the compressible range only at `m = 40` (range 3362 < 6553), one above the birthday value there. Algebraic `B_h` sets in general (Bose-Chowla) give `s* = h + 1` with range about `m^h`, compressible only for `h < m / (2 log2 m)`: relation length `O(m / log m)`, which is asymptotically *below* the birthday scale `Theta(m)`. So small `m` flatters algebraic constructions; asymptotically the random-like adversary remains the strongest known.
* The pigeonhole bound (`s = 4` at `m = 40`) is not approached by any construction here.
