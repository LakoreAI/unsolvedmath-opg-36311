# R15: three-level BCJ tree, measured vs modelled list sizes

Planted weight-`n/2` solutions, random `n`-bit values, fresh random residues per attempt (`300` attempts x `3` instances). Model sizes are BCJ Sect. 3.3 (`N_x / prod M`); `N_x` counts vectors of profile `x`. The `kappa`/`nu` model ignores the consistency filter, so measured sizes are expected to sit below it (BCJ call it an upper bound).

| n | (a,b,g) | moduli | level | model size | measured mean | ratio |
| ---: | :-- | :-- | :-- | ---: | ---: | ---: |
| 16 | (2,1,0) | (13, 173, 17) | leaf | 129.2 | 129.2 | 1.00 |
| 16 | (2,1,0) | (13, 173, 17) | kappa | 53.4 | 48.9 | 0.92 |
| 16 | (2,1,0) | (13, 173, 17) | nu | 9.4 | 10.9 | 1.16 |
| 32 | (2,1,0) | (41, 4673, 733) | leaf | 3508.3 | 3509.1 | 1.00 |
| 32 | (2,1,0) | (41, 4673, 733) | kappa | 1537.2 | 1500.7 | 0.98 |
| 32 | (2,1,0) | (41, 4673, 733) | nu | 106.1 | 143.0 | 1.35 |

## Per-attempt success

| n | (a,b,g) | attempts | successes | per-attempt success |
| ---: | :-- | ---: | ---: | ---: |
| 16 | (2,1,0) | 900 | 115 | 0.128 |
| 32 | (2,1,0) | 900 | 181 | 0.201 |

Toy sizes only: the exponent curve (`0.291n`) is asymptotic and cannot be read off `n <= 32`.
