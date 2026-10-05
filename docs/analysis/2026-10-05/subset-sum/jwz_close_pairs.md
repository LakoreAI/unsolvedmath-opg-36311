# R16b: poly(n)-time disjoint close pairs (JWZ Lemma 9)

For a near-geometric valid PESS instance `w_i = 2^(i-1)` (`i < n`) with top element `2^(n-1)-1-2^g`, Equation (1) and the pigeonhole promise hold. `k = floor(log2 F)`, `\|D\|` is the disjoint close-pair set built by `jwz_disjoint_close_pairs`, `naive` is the `3^(n-k)` suffix coefficient-vector enumeration that D replaces, and `bound` is `200 n^5`. D stays polynomially small as the naive enumeration grows exponentially, and within the Lemma 9 bound.

| n | g | k | F | \|D\| | naive 3^(n-k) | 200 n^5 | within bound |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :-- |
| 16 | 4 | 4 | 17 | 205 | 531441 | 209715200 | yes |
| 16 | 8 | 8 | 257 | 245 | 6561 | 209715200 | yes |
| 16 | 12 | 12 | 4097 | 40 | 81 | 209715200 | yes |
| 18 | 4 | 4 | 17 | 247 | 4782969 | 377913600 | yes |
| 18 | 9 | 9 | 513 | 343 | 19683 | 377913600 | yes |
| 18 | 13 | 13 | 8193 | 119 | 243 | 377913600 | yes |
| 20 | 5 | 5 | 33 | 349 | 14348907 | 640000000 | yes |
| 20 | 10 | 10 | 1025 | 475 | 59049 | 640000000 | yes |
| 20 | 15 | 15 | 32769 | 121 | 243 | 640000000 | yes |
