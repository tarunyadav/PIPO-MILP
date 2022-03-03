# PIPO-MILP-Related-Key-Differential
MILP Based Related-key Differential Characteristics Search for Lightweight Block Cipher PIPO-64/128  \
**_Linear inequalities required for MILP problem are generated using MILES (https://github.com/tarunyadav/MILES)._**
## Source Code 
### There are three python files in this source code.
* _MILP_Outer.py_
* _MILP_Inner.py_
* _print_diff_characteristic.py_
* _LinearInequalities_Outer.txt_ (Generated from MILES)
* _LinearInequalities_Inner.txt_ (Generated from MILES)

## MILP model to minimize number of active S-boxes
* _MILP_Outer.py_ is used to minimize number of active S-boxes in PIPO. It uses _LinearInequalities_Outer.txt_ to write linear inequalities of the S-box.
* There are two arugment for _MILP_Outer.py_. First argument defines number of rounds and second argument define minimum number of active S-boxes in all rounds. We have used the value of second arugment as 1.
* The minimum number of active S-boxes for 14 rounds (one round extra) is searched using following command:\
```MILP_Outer.py 14 1```
* The output (_Outer_Result_14.txt_) is in the following format:\
```[[1, 5], [3, 5], [5, 5], [7, 5], [9, 5], [11, 5], [13,5]]```\
[a,b] => In the round number a, S-box b is active.
* This output is the input for next part (_MILP_Inner.py_) at line no. 247.

## MILP model to optimize probability of related-key differential characteristics
* The output of _MILP_Outer.py_ becomes input for _MILP_inner.py_ at line no. 247. MILP_inner.py uses _LinearInequalities_Inner.txt_ to write linear inequalities of the S-box.
* There is one arugment for _MILP_Inner.py_. This define the number of rounds.
* High probablitiy related-key differential characteristics for 14-round PIPO is searhed using following command:\
```MILP_Inner.py 14```
* The output (_Inner_Result_14.txt_) is in the following format:
```
[[1, 5], [3, 5], [5, 5], [7, 5], [9, 5], [11, 5], [13, 5]] 28.0
z1_5_0 z3_5_0 z5_5_0 z7_5_0 z9_5_0 z11_5_0 z13_5_0 x0_12 k12 x0_24 k24 x0_35 k35 x0_54 k54 k93 u1_29 k117 u1_53 x2_12 x2_24 x2_35 x2_54 u3_29 u3_53 x4_12 x4_24 x4_35 x4_54 u5_29 u5_53 x6_12 x6_24 x6_35 x6_54 u7_29 u7_53 x8_12 x8_24 x8_35 x8_54 u9_29 u9_53 x10_12 x10_24 x10_35 x10_54 u11_29 u11_53 x12_12 x12_24 x12_35 x12_54 u13_29 u13_53 y1_13 y1_29 y1_37 y1_53 y3_13 y3_29 y3_37 y3_53 y5_13 y5_29 y5_37 y5_53 y7_13 y7_29 y7_37 y7_53 y9_13 y9_29 y9_37 y9_53 y11_13 y11_29 y11_37 y11_53 y13_13 y13_29 y13_37 y13_53 x14_12 x14_24 x14_35 x14_54 
```

* This output can be converted into the related-key differential characteristics using _print_diff_characteristic.py_

## Print differential characteristics

* Differential characteristics can be printed using _print_diff_characteristic.py_
* There are two argument for _print_diff_characteristic.py_. First argument is _Inner_Result_14.txt_ and second argument is the characteristic number in _Inner_Result_14.txt_.
* The differential characteristic for 14-round PIPO is printed using following command:\
```print_diff_characteristic.py Inner_Result_14.txt 1```
* The output is in the following format:
```
Related-key Differential Probability for 14 rounds of PIPO-64/128 is 2^{-28.0}
Difference in Keybits is: 0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  0000  0000  0100  0000  0000  0000  0000  1000  0000  0001  0000  0000  0001  0000  0000  0000 
Difference in Keybits is (Hex):0x00200000200000000040000801001000
The input difference of plaintext is: 
0000  0000  0100  0000  0000  0000  0000  1000  0000  0001  0000  0000  0001  0000  0000  0000  :: Hex => 0040  0008  0100  1000   :: 0x0040000801001000 :: Probability => 2^{-0}
The Output difference of the round 1 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 2 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 3 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 4 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 5 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 6 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 7 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 8 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 9 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 10 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 11 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 12 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
The Output difference of the round 13 is: 
0000  0000  0010  0000  0000  0000  0000  0000  0010  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0020  0000  2000  0000   :: 0x0020000020000000 :: Probability => 2^{-0}
The Output difference of the round 14 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  0000  0000   :: 0x0000000000000000 :: Probability => 2^{-4}
```
**It is clear that probability of related-key differential characteristic for 13 rounds of PIPO-64/128 is 2<sup>-24</sup> (removing 14<sup>th</sup> round).**
