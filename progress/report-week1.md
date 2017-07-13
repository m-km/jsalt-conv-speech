# Results that are worth reporting. 

## AMI ASR Results 
### Kaldi baseline

Dataset | Dev | Eval
--------|-----|-----
IHM     | 21.5 | 21.6
SDM1    | 38.8 | 42.7
MDM8    | 35.8 | 38.6


## AMI DER Results
### Kaldi baseline **using** oracle SAD, collar size of ??

Dataset | Dev
--------|------
SDM1    | 22.??
MDM8    | 18.??

### Brno baseline, ** not using ** oracle SAD

Dataset | Collar Size [ms] *|	EVAL	| DEV
--------|-------------------|-------|------
MDM8    | 500	              | 78.16	| 75.09
MDM8    | 750	              | 68.32	| 65.75
MDM8    | 1000	            | 61.33	| 58.94
MDM8    | 1500	            | 54.18	| 50.21
MDM8    | 2000	            | 47.59	| 45.17

