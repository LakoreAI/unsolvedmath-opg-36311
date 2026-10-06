# R13a: decoys with their own short relations (assumption A1 under attack)

`n = 32`: a rank-3 structured support of 16 elements plus 16 adversarial decoys. `whole core` puts every element of every short relation into the compressed side; `components` keeps only relation-graph components that compress; `grow` adds elements one at a time by smallest growth of `Sigma`. All are exact by construction; the table checks it.

| decoys | target | solver | strategy | core | |Sigma(core)| | states | MITM states | speedup | exact |
| :-- | :-- | :-- | :-- | ---: | ---: | ---: | ---: | ---: | :-- |
| random | support | whole core | compress | 16 | 1432 | 21081 | 131072 | 6.2 | True |
| random | support | components | components | 16 | 1432 | 21081 | 131072 | 6.2 | True |
| random | support | grow | grow | 16 | 1432 | 21081 | 131072 | 6.2 | True |
| random | mixed | whole core | compress | 16 | 1432 | 11282 | 131072 | 11.6 | True |
| random | mixed | components | components | 16 | 1432 | 11282 | 131072 | 11.6 | True |
| random | mixed | grow | grow | 16 | 1432 | 10762 | 131072 | 12.2 | True |
| triples | support | whole core | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| triples | support | components | components | 16 | 1348 | 18405 | 131072 | 7.1 | True |
| triples | support | grow | grow | 19 | 10784 | 27834 | 131072 | 4.7 | True |
| triples | mixed | whole core | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| triples | mixed | components | components | 16 | 1348 | 13229 | 131072 | 9.9 | True |
| triples | mixed | grow | grow | 19 | 10784 | 24203 | 131072 | 5.4 | True |
| linked | support | whole core | mitm | 32 | 0 | 131072 | 131072 | 1.0 | True |
| linked | support | components | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| linked | support | grow | grow | 20 | 9413 | 21220 | 131072 | 6.2 | True |
| linked | mixed | whole core | mitm | 32 | 0 | 131072 | 131072 | 1.0 | True |
| linked | mixed | components | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| linked | mixed | grow | grow | 20 | 9413 | 11860 | 131072 | 11.1 | True |
| shifted | support | whole core | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| shifted | support | components | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| shifted | support | grow | grow | 18 | 4674 | 21201 | 131072 | 6.2 | True |
| shifted | mixed | whole core | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| shifted | mixed | components | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| shifted | mixed | grow | grow | 18 | 4674 | 15084 | 131072 | 8.7 | True |

## Reading

* `triples` (short but nearly incompressible gadgets) break the whole-core solver; the component solver recovers 7-10x.
* `linked` and `shifted` decoys merge into the support's relation component and make its sum set too large: both relation-based solvers fall back to plain MITM.
* `grow` (element-wise greedy, preferring related elements) beats all four adversaries, 4.7-12.2x, exact in every row: unrelated elements double `Sigma` and are left out wherever they sit in the relation graph.
* Not covered: an adversary whose compression appears only after a *long* relation is complete. Each single greedy step then doubles `Sigma` and the structure stays invisible, which is the long-relation regime of `HIGH_ENERGY.md` again.
