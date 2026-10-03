# Mixing harness: representation counts

Number of coefficient vectors `c in C^n` with `c . w = target`.
Geometric weights are the near-worst case (few representations);
random weights are the near-average case (many).

| weights | C | n | target | representations |
| --- | --- | ---: | ---: | ---: |
| random | vanilla_{0,1} | 16 | 278 | 263 |
| random | signed_{-1,0,1} | 16 | 0 | 171642 |
| random | partition_{-1,1} | 16 | 278 | 31 |
| geometric | vanilla_{0,1} | 16 | 35113 | 1 |
| geometric | signed_{-1,0,1} | 16 | 0 | 0 |
| geometric | partition_{-1,1} | 16 | 35113 | 1 |

## Random subsampling (vanilla `{0,1}`, target fixed)

Fraction of random m-item subsamples that still contain a representation.
The representation technique needs a solution to survive such restrictions.

| weights | m / n | subsamples with a solution |
| --- | ---: | ---: |
| random | 10/16 | 54/60 |
| random | 12/16 | 60/60 |
| random | 14/16 | 60/60 |
| random | 16/16 | 60/60 |
| geometric | 10/16 | 1/60 |
| geometric | 12/16 | 9/60 |
| geometric | 14/16 | 25/60 |
| geometric | 16/16 | 60/60 |
