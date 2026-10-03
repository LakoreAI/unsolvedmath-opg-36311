# R20: residue-class sampling for collisions

Random numbers of `round(beta*n)` bits; `inputs` with at least one collision out of 5; median over 9 runs per input. Columns are exponents `e` (cost about `2^(e*n)`): plain birthday sampling, the predicted class-sampling cost `2p`, the measured cost `p + samples` (classes plus samples, without the polynomial `n` factor of the residue table), and the samples alone. Meet-in-the-middle is `0.5`.

| n | beta | inputs | birthday e | predicted e | measured e | samples e |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 16 | 0.9 | 5 | 0.505 | 0.399 | 0.417 | 0.315 |
| 16 | 1.0 | 5 | 0.576 | 0.446 | 0.465 | 0.358 |
| 16 | 1.1 | 5 | 0.634 | 0.485 | 0.495 | 0.396 |
| 16 | 1.25 | 5 | 0.728 | 0.548 | 0.644 | 0.599 |
| 20 | 0.9 | 5 | 0.508 | 0.388 | 0.404 | 0.348 |
| 20 | 1.0 | 5 | 0.557 | 0.421 | 0.438 | 0.370 |
| 20 | 1.1 | 5 | 0.605 | 0.453 | 0.464 | 0.377 |
| 20 | 1.25 | 5 | 0.719 | 0.529 | 0.581 | 0.531 |
| 24 | 0.9 | 5 | 0.506 | 0.379 | 0.392 | 0.338 |
| 24 | 1.0 | 5 | 0.548 | 0.407 | 0.416 | 0.339 |
| 24 | 1.1 | 5 | 0.591 | 0.436 | 0.448 | 0.392 |
| 24 | 1.25 | 5 | 0.683 | 0.497 | 0.515 | 0.456 |
