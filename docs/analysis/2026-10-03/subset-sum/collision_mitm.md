# R19: do colliding subset sums make subset sum easier?

Random numbers in `[1, 2^bits)` with `bits = round(beta*n)`; means over 5 inputs. `mitm` is the work of meet-in-the-middle on distinct half sums relative to the plain method (1 = no saving); `best` is the best of 32 random balanced splits. `birthday` is the exponent `e` such that about `2^(e*n)` random subsets are needed before two share a sum (`e < 0.5` beats meet-in-the-middle for finding a collision).

| n | beta | bits | excess | mitm (index split) | mitm (best split) | birthday e |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 0.5 | 8 | 0.9732 | 0.8234 | 0.6984 | 0.314 |
| 16 | 0.6 | 10 | 0.9071 | 0.9195 | 0.8637 | 0.376 |
| 16 | 0.7 | 11 | 0.8284 | 0.9613 | 0.8742 | 0.407 |
| 16 | 0.8 | 13 | 0.5265 | 0.9953 | 0.9641 | 0.471 |
| 16 | 0.9 | 14 | 0.2992 | 1.0000 | 0.9938 | 0.512 |
| 16 | 1.0 | 16 | 0.1152 | 1.0000 | 0.9938 | 0.564 |
| 16 | 1.25 | 20 | 0.0044 | 1.0000 | 1.0000 | 0.721 |
| 16 | 1.5 | 24 | 0.0000 | 1.0000 | 1.0000 | inf |
| 20 | 0.5 | 10 | 0.9916 | 0.8812 | 0.8030 | 0.305 |
| 20 | 0.6 | 12 | 0.9683 | 0.9285 | 0.9021 | 0.357 |
| 20 | 0.7 | 14 | 0.8952 | 0.9887 | 0.9541 | 0.405 |
| 20 | 0.8 | 16 | 0.6774 | 0.9938 | 0.9797 | 0.456 |
| 20 | 0.9 | 18 | 0.3039 | 1.0000 | 0.9898 | 0.508 |
| 20 | 1.0 | 20 | 0.1090 | 1.0000 | 0.9906 | 0.553 |
| 20 | 1.25 | 25 | 0.0030 | 1.0000 | 0.9998 | 0.687 |
| 20 | 1.5 | 30 | 0.0002 | 1.0000 | 1.0000 | inf |
