# Brutal search for a poorly-mixing hard instance

For a random balanced support of size `n/2`, `best coverage` is the largest fraction of residues hit (`p ~ C(n/2,n/4)`) over several random primes (the algorithm may retry). A `hard` instance has `gcd 1`, is not superincreasing, and has `|S(A)|/2^n > 0.5`. A hard instance with small best coverage would refute the target mixing dichotomy.

| n | family | mean best coverage | min best coverage | hard trials | min best coverage (hard) |
| ---: | :-- | ---: | ---: | ---: | ---: |
| 18 | random-b0.75 | 0.598 | 0.449 | 0/6 | — |
| 18 | random-b1.0 | 0.582 | 0.503 | 6/6 | 0.503 |
| 18 | random-b1.25 | 0.578 | 0.523 | 6/6 | 0.523 |
| 18 | short-range | 0.616 | 0.533 | 0/6 | — |
| 18 | short-ap | 0.248 | 0.174 | 0/6 | — |
| 18 | near-geometric | 0.573 | 0.489 | 0/6 | — |
| 18 | common-factor | 0.580 | 0.474 | 6/6 | 0.474 |
| 18 | sidon | 0.619 | 0.498 | 6/6 | 0.498 |
| 20 | random-b0.75 | 0.532 | 0.454 | 0/6 | — |
| 20 | random-b1.0 | 0.615 | 0.504 | 6/6 | 0.504 |
| 20 | random-b1.25 | 0.558 | 0.467 | 6/6 | 0.467 |
| 20 | short-range | 0.573 | 0.430 | 0/6 | — |
| 20 | short-ap | 0.156 | 0.132 | 0/6 | — |
| 20 | near-geometric | 0.650 | 0.631 | 0/6 | — |
| 20 | common-factor | 0.593 | 0.574 | 6/6 | 0.574 |
| 20 | sidon | 0.577 | 0.515 | 6/6 | 0.515 |
