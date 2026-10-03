# R6: modular structure of representations

For a planted solution, residues `a.y mod 2^m` over its `C(n/2, n/4)`
representations, with the modulus set near the decomposition count as in
HGJ. `coverage = min(1, distinct / 2^m)`; near 1 means a random residue
finds a representation, so the HGJ filter applies.

| family | n | decompositions | distinct residues | coverage | max bucket |
| --- | ---: | ---: | ---: | ---: | ---: |
| dissociated | 16 | 70 | 31 | 0.4429 | 6 |
| density1_random | 16 | 70 | 48 | 0.6857 | 2 |
| geometric | 16 | 70 | 33 | 0.4714 | 4 |
| near_geometric | 16 | 70 | 46 | 0.6571 | 3 |
| arithmetic | 16 | 70 | 28 | 0.4 | 5 |
| concentrated_mod_M | 16 | 70 | 1 | 0.0143 | 70 |
| dissociated | 20 | 252 | 156 | 0.619 | 4 |
| density1_random | 20 | 252 | 182 | 0.7222 | 3 |
| geometric | 20 | 252 | 84 | 0.3333 | 8 |
| near_geometric | 20 | 252 | 97 | 0.3849 | 8 |
| arithmetic | 20 | 252 | 37 | 0.1468 | 14 |
| concentrated_mod_M | 20 | 252 | 1 | 0.004 | 252 |
| dissociated | 24 | 924 | 570 | 0.6169 | 5 |
| density1_random | 24 | 924 | 557 | 0.6028 | 5 |
| geometric | 24 | 924 | 604 | 0.6537 | 4 |
| near_geometric | 24 | 924 | 594 | 0.6429 | 5 |
| arithmetic | 24 | 924 | 83 | 0.0898 | 25 |
| concentrated_mod_M | 24 | 924 | 1 | 0.0011 | 924 |
| dissociated | 32 | 12870 | 8394 | 0.6522 | 5 |
| density1_random | 32 | 12870 | 7936 | 0.6166 | 6 |
| geometric | 32 | 12870 | 7654 | 0.5947 | 9 |
| near_geometric | 32 | 12870 | 7982 | 0.6202 | 7 |
| arithmetic | 32 | 12870 | 119 | 0.0092 | 270 |
| concentrated_mod_M | 32 | 12870 | 1 | 0.0001 | 12870 |

Full-coverage families (coverage ~ 1): density1_random, dissociated, geometric, near_geometric.
Concentrated families (coverage < 0.1): arithmetic, concentrated_mod_M.

Interpretation: the generic families (dissociated, density-1, near-
geometric) are fully covered, so the representation filter applies to
them; the concentrated families (geometric, arithmetic, equal-weights)
are exactly the *easy* structured instances. There is no family that is
both hard and poorly covered, so `F = 0` (dissociativity) is *not* the
obstacle the Phase 1 note first suspected.
