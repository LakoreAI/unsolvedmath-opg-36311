# R9: birthday/subsampling sub-solver

For a planted balanced solution: `D` decompositions, modulus `M ~ D`
(so the expected number of surviving decompositions for a random residue
is ~1). `P(survival>=1)` is the fraction of residues that keep a
decomposition; `|Y|` is the residue class the needle hides in.

| n | D | M | P(survival>=1) | max survivors | \|Y\| |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 30 | 30 | 0.6667 | 3 | 27 |
| 20 | 90 | 90 | 0.6111 | 4 | 65 |
| 24 | 350 | 350 | 0.6229 | 4 | 138 |
| 28 | 1120 | 1120 | 0.6527 | 5 | 325 |

Reading: exactly ~1 decomposition survives the residue filter (as HGJ
designs), but it hides in a residue class of size `|Y|`. Uniform
sampling of `s` candidates per side hits the needle with probability
`~ (s/|Y|)`, so constant success requires `s ~ |Y| = L` — i.e. the full
balanced enumeration. There is no subsampling gain for finding the
*specific* decomposition; the birthday idea finds *a* residue match but
not the one whose complement closes the exact target. The `0.4056n`
floor stands for this sub-solver.
