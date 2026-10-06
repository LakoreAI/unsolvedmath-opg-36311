# R13a: forced relation length in the high-energy regime

Asymptotic exponents (`n -> infinity`, `m = n/2`). `k/n` is the smallest `k` with `C(m/2 + k, k) > D`; below it the support must contain disjoint `P, Q` with `|P| = |Q| <= k` and equal sum (rigorous counting; `HIGH_ENERGY.md`). `find relation exp` is `log2 C(n,k)/n`, the cost of finding an equal-sum pair of `k`-subsets among all `n` inputs by sorting. `residual MITM exp` assumes `P u Q` is known to lie in the solution and solves the remaining `n - 2k` elements by meet-in-the-middle. `LIFT exp` is the `LIFT.md` exponent (`max(0.4057, 0.811 - delta)`, capped by `0.5`). The conditional columns only help if the found relation lies inside the support, which is not guaranteed on adversarial decoys.

| delta (D=2^(delta n)) | k/n | k/m | find relation exp | residual MITM exp | LIFT exp |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0.050 | 0.0078 | 0.0155 | 0.0656 | 0.4922 | 0.7613 |
| 0.100 | 0.0193 | 0.0386 | 0.1376 | 0.4807 | 0.7113 |
| 0.150 | 0.0341 | 0.0681 | 0.2144 | 0.4659 | 0.6613 |
| 0.200 | 0.0521 | 0.1041 | 0.2951 | 0.4479 | 0.6113 |
| 0.250 | 0.0736 | 0.1472 | 0.3792 | 0.4264 | 0.5613 |
| 0.300 | 0.0990 | 0.1981 | 0.4659 | 0.4010 | 0.5113 |
| 0.311 | 0.1052 | 0.2104 | 0.4852 | 0.3948 | 0.5003 |
| 0.350 | 0.1288 | 0.2576 | 0.5541 | 0.3712 | 0.4613 |
| 0.400 | 0.1635 | 0.3270 | 0.6426 | 0.3365 | 0.4113 |
| 0.450 | 0.2038 | 0.4075 | 0.7294 | 0.2962 | 0.4057 |
| 0.500 | 0.2503 | 0.5007 | 0.8118 | 0.2497 | 0.4057 |
