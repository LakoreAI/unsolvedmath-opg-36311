# R13 probe: representation mixing vs additive structure

`coverage` is the fraction of residues mod `p ~ C(n/2, n/4)` hit by the HGJ sums `y . w` over the `C(n/2, n/4)` weight-`n/4` representations `y` of a planted weight-`n/2` solution; `doubling` is `|A+A| / n`; `dissociated` is `|S(A)| = 2^n` (not by itself a hardness proxy: powers of two are dissociated and easy). The candidate mixing dichotomy for the target problem says low coverage should coincide with additive structure (small doubling or superincreasing), so a random residue still retains a representation; only such structured inputs may mix poorly.

| n | family | coverage | doubling | dissociated |
| ---: | :-- | ---: | ---: | :-- |
| 16 | constant | 0.014 | 1.00 | no |
| 16 | geometric | 0.648 | 8.50 | yes |
| 16 | arithmetic | 0.423 | 1.94 | no |
| 16 | random-small | 0.465 | 7.50 | no |
| 16 | random-large | 0.577 | 8.50 | yes |
| 16 | sidon | 0.634 | 8.50 | yes |
| 20 | constant | 0.004 | 1.00 | no |
| 20 | geometric | 0.475 | 10.50 | yes |
| 20 | arithmetic | 0.175 | 1.95 | no |
| 20 | random-small | 0.634 | 9.70 | no |
| 20 | random-large | 0.611 | 10.50 | yes |
| 20 | sidon | 0.638 | 10.50 | yes |
