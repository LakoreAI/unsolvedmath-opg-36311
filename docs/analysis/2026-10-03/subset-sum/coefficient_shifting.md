# R12: coefficient shifting and the open cases

Factorisations `C1 + C2 = C` with `C1, C2` subsets of
`[-3, 3]`, size <= 3. `max reps` is the largest
number of representations any coefficient acquires; shifting needs a
coefficient with >= 2 representations.

| C | # factorisations | # nontrivial | best max reps | best min reps | example |
| --- | ---: | ---: | ---: | ---: | --- |
| Subset Sum {0,1} | 12 | 0 | 1 | 1 | `(-2,) + (2, 3)` |
| Partition {+-1} | 10 | 0 | 1 | 1 | `(-2,) + (1, 3)` |
| Equal Subset Sum {-1,0,1} | 16 | 6 | 2 | 1 | `(-3, -2) + (2, 3)` |
| Balancing [+-2] | 14 | 0 | 1 | 1 | `(-1,) + (-1, 0, 2, 3)` |
| Balancing [+-3] | 10 | 4 | 2 | 1 | `(-1, 0) + (-2, -1, 2, 3)` |
| Balancing [-2:2] | 39 | 39 | 3 | 1 | `(-3, -2, -1) + (1, 2, 3)` |

Reading: `{0,1}` (Subset Sum) and `{+-1}` (Partition) admit only trivial
factorisations, so no coefficient acquires extra representations and
coefficient shifting cannot be applied. `{-1,0,1}` already has the
0 = 0+0 / 1+(-1) / (-1)+1 freedom; `[+-3]` is handled by the paper's
`{0,1} + {-3,-2,1,2}` factorisation, where `+-2` gets two
representations. This is exactly the paper's stated frontier: the lack
of a nontrivial sumset factorisation (equivalently, of a 0 coefficient)
is why the worst-case technique stalls at `C={0,1}` and `C={+-1}`.
