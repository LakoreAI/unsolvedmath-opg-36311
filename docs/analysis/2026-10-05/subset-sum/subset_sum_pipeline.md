# (b) Candidate representation pipeline across families

Planted balanced (`|x| = n/2`) instances. `strategy` is the branch that returned the witness, `valid` checks the witness sum, `coverage` is the mixing coverage of the planted solution's `weight-n/4` representations (`p ~ C(n/2, n/4)`), and `work e` is `log2(enumerated)/n` against the meet-in-the-middle exponent 0.5.

| n | family | strategy | valid | coverage | work e |
| ---: | :-- | :-- | :-- | ---: | ---: |
| 16 | superincreasing | superincreasing | yes | 0.732 | 0.250 |
| 16 | geometric | superincreasing | yes | 0.493 | 0.250 |
| 16 | constant | mitm | yes | 0.014 | 0.562 |
| 16 | arithmetic | representation | yes | 0.366 | 0.363 |
| 16 | random-small | representation | yes | 0.620 | 0.363 |
| 16 | random-large | representation | yes | 0.746 | 0.425 |
| 20 | superincreasing | superincreasing | yes | 0.716 | 0.216 |
| 20 | geometric | superincreasing | yes | 0.436 | 0.216 |
| 20 | constant | mitm | yes | 0.004 | 0.550 |
| 20 | arithmetic | representation | yes | 0.187 | 0.454 |
| 20 | random-small | representation | yes | 0.677 | 0.325 |
| 20 | random-large | mitm | yes | 0.630 | 0.550 |
| 24 | superincreasing | superincreasing | yes | 0.568 | 0.191 |
| 24 | geometric | superincreasing | yes | 0.552 | 0.191 |
| 24 | constant | mitm | yes | 0.001 | 0.542 |
| 24 | arithmetic | representation | yes | 0.071 | 0.408 |
| 24 | random-small | representation | yes | 0.634 | 0.366 |
| 24 | random-large | representation | yes | 0.640 | 0.408 |

The pipeline is correct on every planted instance (the meet-in-the-middle
fallback guarantees it). The representation branch carries the hard
large-value families; the structural families route to gcd/greedy. What
is not shown here is a *worst-case* exponent `0.5 - eps`, which needs the
target-problem mixing dichotomy of `ATTACK.md`.
