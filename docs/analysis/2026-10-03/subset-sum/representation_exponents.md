# R11: reproduced representation-technique exponents

Base-2 exponent per `n`, from the primary sources (HGJ ePrint 2010/189;
BCJ ePrint 2011/474 Sect. 3.3). These replace the earlier 2-part balanced
model (R8), which used the wrong sub-solver structure.

| quantity | exponent | source |
| --- | ---: | --- |
| HGJ 2-part ideal `D(1/2)` | 0.3113 | HGJ 4.1 |
| HGJ simple algorithm (best beta) | 0.3372 | HGJ 4.2 / May-Meurer |
| BCJ `alpha=beta=gamma=0` | 0.3371 | BCJ 3.3 (recovers HGJ) |
| BCJ minimised | 0.2911 | BCJ 3.3 |

BCJ optimum: alpha=0.0270, beta=0.0170, gamma=0.0030, memory exponent 0.2909.

Reading: `D(1/2) = 0.3113` is the *ideal* two-part exponent HGJ aims at.
The concrete HGJ simple algorithm reaches `0.338` (beta -> 1/4), matching
the May-Meurer-corrected `0.337`. The BCJ three-level `{-1,0,1}`
construction minimises at `0.291`, reproducing the published
`0.291`. These are **average-case** bounds for random hard knapsacks;
they do not give a worst-case `2^(n/3)` algorithm.

The R8 error: the sub-solver is not a balanced meet-in-the-middle on a
2-part representation. HGJ uses a 4-way decomposition whose parts are
weight-`n/8` subsets, solved by the *unbalanced* Schroeppel-Shamir
algorithm; BCJ adds three levels of `{-1,0,1}` decompositions.
