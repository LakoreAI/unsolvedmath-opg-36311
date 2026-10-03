# Howgrave-Graham-Joux representation search vs meet-in-the-middle

Planted balanced weight-n/2 solutions. Enumeration work is
`2 * C(n/2, n/8)` per residue attempt (the cost driver), against
meet-in-the-middle enumeration `2^(n/2)`.

| n | analytical enumeration | 2^(n/2) | log2(enum)/n | seconds |
| ---: | ---: | ---: | ---: | ---: |
| 16 | 56 | 2.560e+02 | 0.3630 | 0.000 |
| 24 | 440 | 4.096e+03 | 0.3659 | 0.001 |
| 32 | 3640 | 6.554e+04 | 0.3697 | 0.011 |
| 40 | 31008 | 1.049e+06 | 0.3730 | 0.092 |
| 48 | 269192 | 1.678e+07 | 0.3758 | 0.935 |
| 56 | 2368080 | 2.684e+08 | 0.3781 | 10.300 |

Fitted enumeration bit-exponent: **0.3846** (R^2=0.9999);
meet-in-the-middle is 0.5. Fitted wall-time exponent: 0.4187.
The theoretical HGJ value is `h(1/4)/2 = 0.4057`; the optimized 0.291n
recursion is not implemented.
