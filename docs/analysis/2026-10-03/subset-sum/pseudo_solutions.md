# R7: pseudo-solution load by cardinality

`T` = target representations of cardinality n/2 (true solutions);
`P` = target representations of cardinality < n/2 (pseudo-solution source);
`F` = total collisions.

| family | n | T | P | F |
| --- | ---: | ---: | ---: | ---: |
| dissociated | 12 | 1 | 0 | 0 |
| density1_random | 12 | 1 | 0 | 416 |
| geometric | 12 | 1 | 0 | 0 |
| near_geometric | 12 | 1 | 0 | 476 |
| arithmetic | 12 | 51 | 52 | 4017 |
| dense_random | 12 | 21 | 14 | 3901 |
| concentrated_mod_M | 12 | 1 | 1 | 300 |
| dissociated | 14 | 1 | 0 | 0 |
| density1_random | 14 | 1 | 1 | 1062 |
| geometric | 14 | 1 | 0 | 0 |
| near_geometric | 14 | 1 | 0 | 1350 |
| arithmetic | 14 | 136 | 199 | 16278 |
| dense_random | 14 | 21 | 78 | 16109 |
| concentrated_mod_M | 14 | 3 | 2 | 7274 |
| dissociated | 16 | 1 | 0 | 0 |
| density1_random | 16 | 1 | 0 | 9240 |
| geometric | 16 | 1 | 0 | 0 |
| near_geometric | 16 | 1 | 0 | 7032 |
| arithmetic | 16 | 499 | 274 | 65399 |
| dense_random | 16 | 204 | 79 | 65247 |
| concentrated_mod_M | 16 | 3 | 0 | 45592 |
| dissociated | 18 | 1 | 0 | 0 |
| density1_random | 18 | 1 | 0 | 32412 |
| geometric | 18 | 1 | 0 | 0 |
| near_geometric | 18 | 1 | 0 | 27936 |
| arithmetic | 18 | 1499 | 2064 | 261972 |
| dense_random | 18 | 603 | 514 | 261773 |
| concentrated_mod_M | 18 | 4 | 0 | 241323 |
| dissociated | 20 | 1 | 0 | 0 |
| density1_random | 20 | 1 | 0 | 104128 |
| geometric | 20 | 1 | 0 | 0 |
| near_geometric | 20 | 1 | 0 | 62567 |
| arithmetic | 20 | 1652 | 9553 | 1048365 |
| dense_random | 20 | 287 | 26 | 1048021 |
| concentrated_mod_M | 20 | 24 | 40 | 1016573 |

Families with P=0 across all n: dissociated, geometric, near_geometric

Reading: dissociated and geometric instances have a unique solution and
no pseudo-solutions, so the HGJ merge is *cleanest* exactly where the
worst-case instances are believed to live. Pseudo-solution load grows
with collisions and is largest for dense/arithmetic instances, which are
easy. The barrier to 2^(n/3) is therefore the sub-solver cost, not
pseudo-solution blow-up on hard instances.
