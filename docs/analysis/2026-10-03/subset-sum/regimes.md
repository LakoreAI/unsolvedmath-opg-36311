# Regime-aware subset-sum benchmark

Infeasible instances (even values, odd target). Least-squares slope of
`log2(seconds)` and `log2(states)` against `n` estimates the bit-exponent.

| family | algorithm | points | time bits/n | states bits/n | time R^2 |
| --- | --- | ---: | ---: | ---: | ---: |
| bounded | brute | 3 | 1.092 | 1.000 | 0.998 |
| bounded | dp | 7 | 0.144 | 0.145 | 0.960 |
| bounded | mitm | 7 | 0.519 | 0.500 | 0.980 |
| bounded | ss | 7 | 0.499 | 0.530 | 0.986 |
| sparse | brute | 3 | 1.168 | 1.000 | 1.000 |
| sparse | mitm | 7 | 0.564 | 0.500 | 0.994 |
| sparse | ss | 7 | 0.515 | 0.501 | 0.996 |
