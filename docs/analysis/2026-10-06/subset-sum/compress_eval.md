# R13a: compress-then-MITM versus plain meet-in-the-middle

`states` counts dictionary entries touched. The solver is exact whatever core the relation detector returns; the core only changes speed. `speedup` is `MITM states / compress states`. The `random` control has no structure and must fall back to plain MITM (speedup 1.0).

| family | n | d | target | strategy | core | distinct sums of core | compress states | MITM states | speedup | exact |
| :-- | ---: | ---: | :-- | :-- | ---: | ---: | ---: | ---: | ---: | :-- |
| distinct | 24 | 7 | support | compress | 12 | 2974 | 10045 | 8192 | 0.8 | True |
| distinct | 24 | 7 | mixed | compress | 12 | 2974 | 7467 | 8192 | 1.1 | True |
| distinct | 24 | 8 | support | compress | 12 | 3414 | 10925 | 8192 | 0.7 | True |
| distinct | 24 | 8 | mixed | compress | 12 | 3414 | 8136 | 8192 | 1.0 | True |
| distinct | 24 | 10 | support | compress | 4 | 15 | 8109 | 8192 | 1.0 | True |
| distinct | 24 | 10 | mixed | compress | 4 | 15 | 5267 | 8192 | 1.6 | True |
| distinct | 32 | 10 | support | compress | 14 | 11522 | 123148 | 131072 | 1.1 | True |
| distinct | 32 | 10 | mixed | compress | 14 | 11522 | 92542 | 131072 | 1.4 | True |
| distinct | 32 | 12 | support | compress | 12 | 4014 | 133783 | 131072 | 1.0 | True |
| distinct | 32 | 12 | mixed | compress | 12 | 4014 | 114201 | 131072 | 1.1 | True |
| gap | 32 | 3 | support | compress | 16 | 360 | 10217 | 131072 | 12.8 | True |
| gap | 32 | 3 | mixed | compress | 16 | 360 | 5168 | 131072 | 25.4 | True |
| gap | 32 | 4 | support | compress | 16 | 1172 | 18741 | 131072 | 7.0 | True |
| gap | 32 | 4 | mixed | compress | 16 | 1172 | 11641 | 131072 | 11.3 | True |
| gap | 32 | 8 | support | compress | 15 | 19268 | 123341 | 131072 | 1.1 | True |
| gap | 32 | 8 | mixed | compress | 15 | 19268 | 109982 | 131072 | 1.2 | True |
| random | 24 | 0 | support | compress | 5 | 31 | 5998 | 8192 | 1.4 | True |
| random | 24 | 0 | mixed | compress | 5 | 31 | 4679 | 8192 | 1.8 | True |
| random | 32 | 0 | support | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
| random | 32 | 0 | mixed | mitm | 0 | 0 | 131072 | 131072 | 1.0 | True |
