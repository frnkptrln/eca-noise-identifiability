| n | periodic states in E ∪ O | periodic states by Lemma 6 | periodic states, direct enumeration | equal | fraction of states not on a cycle | decimal | 2^(1 - n/2) (1 - 2^(-2^j)) equal | value quoted from arXiv:2610.10967 | agrees at the quoted precision | states without preimage (fraction) |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 | 10 | 10 | True | 3/8 | 0.375000000000 | True |  |  | 4 (0.250000000000) |
| 6 | 7 | 56 | 56 | True | 1/8 | 0.125000000000 | True |  |  | 8 (0.125000000000) |
| 8 | 1 | 226 | 226 | True | 15/128 | 0.117187500000 | True |  |  | 16 (0.062500000000) |
| 10 | 31 | 992 | 992 | True | 1/32 | 0.031250000000 | True |  |  | 32 (0.031250000000) |
| 12 | 31 | 4000 | 4000 | True | 3/128 | 0.023437500000 | True |  |  | 64 (0.015625000000) |
| 14 | 127 | 16256 | 16256 | True | 1/128 | 0.007812500000 | True |  |  | 128 (0.007812500000) |
| 16 | 1 | 65026 | 65026 | True | 255/32768 | 0.007781982422 | True |  |  | 256 (0.003906250000) |
| 18 | 511 | 261632 | 261632 | True | 1/512 | 0.001953125000 | True |  |  | 512 (0.001953125000) |
| 20 | 511 | 1047040 | 1047040 | True | 3/2048 | 0.001464843750 | True |  |  | 1024 (0.000976562500) |
| 22 | 2047 | 4192256 | 4192256 | True | 1/2048 | 0.000488281250 | True | 0.00048828 | True | 2048 (0.000488281250) |
| 24 | 511 | 16769536 | 16769536 | True | 15/32768 | 0.000457763672 | True | 0.00045776 | True | 4096 (0.000244140625) |
| 26 | 8191 | 67100672 | not computed |  | 1/8192 | 0.000122070312 | True |  |  | not computed |

Lemma 6 count equals the direct count at every even n = 4..24: True. The closed form agrees at every even n = 4..26: True. Both quoted values agree: True. Within n = 4..26 the fraction is below 0.01 for every even n >= 14 and not for smaller even n. CPU time 1.39 s, peak memory 1035 MB (`proofs_43_142/zhu_richard_154.py` -> `proofs_43_142/out/zhu_richard_154.json`).
