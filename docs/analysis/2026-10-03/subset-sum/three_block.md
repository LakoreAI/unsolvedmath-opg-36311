# P2.1: pairwise sumsets in the three-block split

Exponent `e` of the smallest pairwise sumset `|Si + Sj|` (size about `2^(e*n)`). Listing it and matching against the third block beats meet-in-the-middle only if `e < 0.5`. `predicted` is `min(2/3, (log2(2n/3) + bits)/n)`. `index` is the mean over 3 inputs with consecutive blocks; `best` is the smallest over 8 random splits per input.

| n | beta | predicted e | index e | best e |
| ---: | ---: | ---: | ---: | ---: |
| 18 | 0.4 | 0.588 | 0.511 | 0.462 |
| 18 | 0.5 | 0.667 | 0.593 | 0.583 |
| 18 | 0.6 | 0.667 | 0.643 | 0.626 |
| 18 | 0.7 | 0.667 | 0.649 | 0.646 |
| 18 | 0.8 | 0.667 | 0.660 | 0.656 |
| 18 | 0.9 | 0.667 | 0.665 | 0.663 |
| 18 | 1.0 | 0.667 | 0.666 | 0.664 |
| 21 | 0.4 | 0.562 | 0.493 | 0.466 |
| 21 | 0.5 | 0.657 | 0.571 | 0.557 |
| 21 | 0.6 | 0.667 | 0.650 | 0.642 |
| 21 | 0.7 | 0.667 | 0.662 | 0.659 |
| 21 | 0.8 | 0.667 | 0.665 | 0.661 |
| 21 | 0.9 | 0.667 | 0.666 | 0.666 |
| 21 | 1.0 | 0.667 | 0.666 | 0.666 |
| 24 | 0.4 | 0.583 | 0.522 | 0.514 |
| 24 | 0.5 | 0.667 | 0.586 | 0.564 |
| 24 | 0.6 | 0.667 | 0.639 | 0.633 |
| 24 | 0.7 | 0.667 | 0.661 | 0.660 |
| 24 | 0.8 | 0.667 | 0.665 | 0.659 |
| 24 | 0.9 | 0.667 | 0.667 | 0.666 |
| 24 | 1.0 | 0.667 | 0.666 | 0.666 |
