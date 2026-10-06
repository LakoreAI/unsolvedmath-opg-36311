# R13: the profile barrier is polynomial

Correction to `NEXT.md` Sect. 3.2. A random permutation balances a weight-`w` support with probability `C(n/2,w/2)^2/C(n,w)`; at `w=n/2` this is `Theta(1/sqrt(n))`, so `O(sqrt n)` permutations restore completeness. The `2^(0.811n)` all-profiles enumeration is unnecessary.

## Exact probability vs sampling

| n | w | exact p | p*sqrt(n) | sampled p | perms for 99% |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 8 | 0.3807 | 1.523 | 0.3887 | 10 |
| 16 | 4 | 0.4308 | 1.723 | 0.4281 | 9 |
| 32 | 16 | 0.2756 | 1.559 | 0.2710 | 15 |
| 32 | 8 | 0.3149 | 1.781 | 0.3165 | 13 |
| 64 | 32 | 0.1971 | 1.577 | 0.1951 | 21 |
| 64 | 16 | 0.2265 | 1.812 | 0.2208 | 18 |
| 128 | 64 | 0.1402 | 1.586 | 0.1381 | 31 |
| 128 | 32 | 0.1615 | 1.827 | 0.1628 | 27 |
| 256 | 128 | 0.0994 | 1.591 | 0.1011 | 44 |
| 256 | 64 | 0.1147 | 1.835 | 0.1157 | 38 |
| 1024 | 512 | 0.0498 | 1.595 | 0.0510 | 91 |
| 1024 | 256 | 0.0575 | 1.841 | 0.0616 | 78 |

## Real search on concentrated solutions

Planted weight-`n/2` solutions with a controlled first-half share, random `n`-bit values, `hgj_permuted_search` (first attempt keeps the natural order). Compare `hgj_profile.md`, where one permutation at 4 trials gave 0-0.5.

| n | first-half share | perm budget | success | mean work | MITM work |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 24 | 0 | 20 | 1.00 | 18920 | 4096 |
| 24 | 3 | 20 | 1.00 | 14520 | 4096 |
| 24 | 6 | 20 | 1.00 | 550 | 4096 |
| 32 | 0 | 23 | 1.00 | 259805 | 65536 |
| 32 | 4 | 23 | 1.00 | 187915 | 65536 |
| 32 | 8 | 23 | 1.00 | 6370 | 65536 |

## Power-of-two vs prime modulus on adversarial families

Uniformly random weight-`n/2` supports (not balanced), permutation budget `ceil(3 sqrt n)`, 8 residues per permutation. The modulus is `2^m` (default) or the next prime above it.

| n | family | pow2 success | pow2 work | prime success | prime work |
| ---: | :-- | ---: | ---: | ---: | ---: |
| 24 | random-b1.0 | 1.00 | 6.01e+03 | 1.00 | 5.79e+03 |
| 24 | random-b1.5 | 1.00 | 2.49e+03 | 1.00 | 2.2e+03 |
| 24 | geometric | 0.83 | 1.67e+04 | 1.00 | 4.55e+03 |
| 24 | arithmetic-large | 1.00 | 2.93e+03 | 1.00 | 1.83e+03 |
| 24 | two-scale | 1.00 | 4.11e+03 | 1.00 | 4.03e+03 |
| 24 | gap-rank2 | 1.00 | 440 | 1.00 | 440 |
| 24 | q-multiple | 1.00 | 1.1e+03 | 1.00 | 1.03e+03 |
| 32 | random-b1.0 | 1.00 | 1.12e+05 | 1.00 | 1.13e+05 |
| 32 | random-b1.5 | 1.00 | 1.3e+05 | 1.00 | 1.32e+05 |
| 32 | geometric | 0.50 | 3.31e+05 | 1.00 | 6.67e+04 |
| 32 | arithmetic-large | 1.00 | 9.04e+04 | 1.00 | 1.46e+05 |
| 32 | two-scale | 1.00 | 2e+04 | 1.00 | 1.82e+04 |
| 32 | gap-rank2 | 1.00 | 3.64e+03 | 1.00 | 3.64e+03 |
| 32 | q-multiple | 1.00 | 8.49e+03 | 1.00 | 8.49e+03 |

Work is total enumerated subsets across permutations and residues.
