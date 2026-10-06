# R13a: forced relation length in the high-energy regime

Asymptotic exponents (`n -> infinity`, `m = n/2`). `k/n` is the smallest `k` with `C(m/4 + k/2, k/2)^2 > D*`; below it the support must contain disjoint `P, Q` with `|P| = |Q| <= k` and equal sum (rigorous counting; `HIGH_ENERGY.md`). `find relation exp` is `log2 C(n,k)/n`, the cost of finding an equal-sum pair of `k`-subsets among all `n` inputs by sorting. `residual MITM exp` assumes `P u Q` is known to lie in the solution and solves the remaining `n - 2k` elements by meet-in-the-middle. `LIFT exp` is the `LIFT.md` exponent (`max(0.4057, 0.811 - delta)`, capped by `0.5`). The conditional columns only help if the found relation lies inside the support, which is not guaranteed on adversarial decoys.

| delta (D=2^(delta n)) | k/n | k/m | find relation exp | residual MITM exp | LIFT exp |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.050 | 0.0078 | 0.0156 | 0.0658 | 0.4922 | 0.7613 |
| 0.100 | 0.0194 | 0.0388 | 0.1379 | 0.4806 | 0.7113 |
| 0.150 | 0.0341 | 0.0683 | 0.2148 | 0.4659 | 0.6613 |
| 0.200 | 0.0522 | 0.1043 | 0.2956 | 0.4478 | 0.6113 |
| 0.250 | 0.0737 | 0.1475 | 0.3797 | 0.4263 | 0.5613 |
| 0.300 | 0.0992 | 0.1984 | 0.4664 | 0.4008 | 0.5113 |
| 0.311 | 0.1053 | 0.2107 | 0.4857 | 0.3947 | 0.5003 |
| 0.350 | 0.1290 | 0.2580 | 0.5547 | 0.3710 | 0.4613 |
| 0.400 | 0.1637 | 0.3274 | 0.6431 | 0.3363 | 0.4113 |
| 0.450 | 0.2040 | 0.4080 | 0.7299 | 0.2960 | 0.4057 |
| 0.500 | 0.2506 | 0.5013 | 0.8123 | 0.2494 | 0.4057 |
