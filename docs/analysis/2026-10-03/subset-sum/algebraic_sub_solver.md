# R10: algebraic methods and the sub-solver floor

Base-2 exponent per `n` to find a weight-`n/4` subset with
`a.y = R (mod 2^(n/2))`.

| method | exponent | what it returns |
| --- | ---: | --- |
| balanced meet-in-the-middle (R8) | 0.4056 | finds all of Y |
| full-residue cardinality DP | 0.5000 | counting, not finding |
| FFT / group-algebra product | 0.5000 | counting, not finding |
| coarse DP + rejection sample | 0.2500 | random element, not the planted one |
| find planted element (uniform) | 0.5000 | needs full distribution |

Reading: counting the residue class is cheap (DP / FFT need only the
full residue space, ~`2^(0.5n)`, already above the balanced MITM
`0.4056n`). A coarse DP plus rejection sampling returns a
*random* element in `0.25n`, but the algorithm needs the planted element
(the unique surviving decomposition, R9), and sampling uniformly from the
residue class requires the full `2^(n/2)` distribution. So the
counting-vs-finding gap blocks the algebraic route: none of these
methods beats the balanced-MITM floor `0.4056n` while
producing the needed element.

Open problem (unchanged after R8-R10): a sub-solver that finds the
planted weight-`n/4` modular subset faster than `2^(0.4056n)`, or a
conditional lower bound showing it is hard (e.g. a reduction from
modular subset sum / k-SUM / lattice problems).
