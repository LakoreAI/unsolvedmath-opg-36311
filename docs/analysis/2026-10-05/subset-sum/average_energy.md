# R13: average collision energy over primes

Planted balanced solution; `Y` representations of weight `n/4`. For every prime `p in [Y, 2Y]`, `E_p = sum_r c_r^2` and coverage `s_p / p`. The elementary bound is `exact + Y^2 * 2 / pi` (with `2beta = 2`); the candidate lemma says the average is `O(Y log Y)`, so a random prime mixes. `min cov` is the pointwise counterexample-hunting quantity.

| n | Y | primes | exact pairs | avg E_p | bound | avg cov | min cov |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 70 | 15 | 0 | 113.3 | 653 | 0.505 | 0.371 |
| 20 | 252 | 43 | 0 | 421.9 | 2954 | 0.490 | 0.325 |
| 22 | 462 | 68 | 0 | 777.6 | 6278 | 0.497 | 0.270 |
