# PIPO-MILP
MILP Based Differential Characteristics Search for Lightweight Block Cipher PIPO-64/128 (https://link.springer.com/chapter/10.1007%2F978-3-030-68890-5_6) \
**_Linear inequalities required for MILP problem are generated using MILES (https://github.com/tarunyadav/MILES)._**
## Source Code 
### There are five files and two folders in this source code.
* _MILP_Outer.py_
* _MILP_Inner.py_
* _print_diff_characteristic.py_
* _LinearInequalities_Outer.txt_ (Generated from MILES)
* _LinearInequalities_Inner.txt_ (Generated from MILES)\
**_Source Code (including README) for inequalities reduction and to search impossible differential & related-key differential characteristics is provided in respective folders._** 
## MILP model to minimize number of active S-boxes
* _MILP_Outer.py_ is used to minimize number of active S-boxes in PIPO. It uses _LinearInequalities_Outer.txt_ to write linear inequalities of the S-box.
* There are two arugment for _MILP_Outer.py_. First argument defines number of rounds and second argument define the cutoff bound of active S-box. The second argument is made changable(instead of fix upper/lower bound) because it is obsevered that GUROBI gives quick solution for for some values which are not directly related to the upper/lower bound of active S-box. 
* The minimum number of active S-boxes for 7 rounds is searched using following command:\
```MILP_Outer.py 7 10```
* The output (_Outer_Result_7.txt_) is in the following format:\
```[[0, 0], [1, 7], [2, 3], [2, 7], [3, 0], [3, 4], [3, 5], [3, 7], [4, 0], [4, 6], [4, 7], [5, 4], [6, 7]]```\
[a,b] => In the round number a, S-box b is active.
* This output is the input for next part (_MILP_Inner.py_) at line no. 210.

## MILP model to optimize probability of differential characteristics
* The output of _MILP_Outer.py_ becomes input for _MILP_inner.py_ at line no. 210. MILP_inner.py uses _LinearInequalities_Inner.txt_ to write linear inequalities of the S-box.
* There is one arugment for _MILP_Inner.py_. This define the nuumber of rounds.
* High probablitiy differential characteristics for 7-round PIPO-64/128  is searhed using following command:\
```MILP_Inner.py 7```
* The output (_Inner_Result_7.txt_) is in the following format:
```
[[0, 0], [1, 7], [2, 3], [2, 7], [3, 0], [3, 4], [3, 5], [3, 7], [4, 0], [4, 6], [4, 7], [5, 4], [6, 7]] 65.0
z0_0_0 z1_7_0 z2_3_3 z2_7_5 z3_0_3 z3_4_0 z3_5_3 z3_7_3 z4_0_0 z4_6_5 z4_7_5 z5_4_6 z6_7_0 x0_8 x0_16 x0_32 x0_40 x0_56 y0_8 x1_15 y1_7 y1_23 x2_19 y2_19 y2_43 y2_51 y2_59 x2_7 y2_7 y2_39 y2_47 y2_55 x3_40 x3_48 y3_8 y3_32 x3_44 x3_52 y3_20 y3_28 y3_60 x3_37 x3_61 y3_29 y3_53 x3_7 x3_23 y3_7 y3_15 y3_55 x4_16 x4_24 x4_48 y4_16 x4_14 x4_38 x4_54 x4_62 y4_38 x4_7 x4_15 x4_31 y4_47 x5_20 x5_36 x5_44 y5_28 x6_31 y6_15 y6_23 y6_31 y6_55 x7_14 x7_19 x7_26 x7_48
```

* This output can be converted into the differential characteristics using _print_diff_characteristic.py_

## Print differential characteristics

* Differential characteristics can be printed using _print_diff_characteristic.py_
* There are two argument for _print_diff_characteristic.py_. First argument is _Inner_Result_7.txt_ and second argument is the characteristic number in _Inner_Result_7.txt_.
* The differential characteristic for 7-round PIPO-64/128 is printed using following command:\
```print_diff_characteristic.py Inner_Result_7.txt 1```
* The output is in the following format:
```
Differential Probability for 7 rounds of PIPO-64/128 is 2^{-65.0}
The input difference of plaintext is: 
0000  0001  0000  0000  0000  0001  0000  0001  0000  0000  0000  0001  0000  0001  0000  0000  :: Hex => 0100  0101  0001  0100   :: 0x0100010100010100 :: Probability => 2^{-0}
The Output difference of the round 1 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1000  0000  0000  0000  :: Hex => 0000  0000  0000  8000   :: 0x0000000000008000 :: Probability => 2^{-4}
The Output difference of the round 2 is: 
0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  0000  1000  0000  0000  1000  0000  :: Hex => 0000  0000  0008  0080   :: 0x0000000000080080 :: Probability => 2^{-4}
The Output difference of the round 3 is: 
0010  0000  0001  0001  0001  0001  0010  0000  0000  0000  1000  0000  0000  0000  1000  0000  :: Hex => 2011  1120  0080  0080   :: 0x2011112000800080 :: Probability => 2^{-11}
The Output difference of the round 4 is: 
0100  0000  0100  0001  0000  0000  0100  0000  1000  0001  0000  0001  1100  0000  1000  0000  :: Hex => 4041  0040  8101  c080   :: 0x404100408101c080 :: Probability => 2^{-19}
The Output difference of the round 5 is: 
0000  0000  0000  0000  0001  0000  0001  0000  0000  0000  0001  0000  0000  0000  0000  0000  :: Hex => 0000  1010  0010  0000   :: 0x0000101000100000 :: Probability => 2^{-16}
The Output difference of the round 6 is: 
0000  0000  0000  0000  0000  0000  0000  0000  1000  0000  0000  0000  0000  0000  0000  0000  :: Hex => 0000  0000  8000  0000   :: 0x0000000080000000 :: Probability => 2^{-7}
The Output difference of the round 7 is: 
0000  0000  0000  0001  0000  0000  0000  0000  0000  0100  0000  1000  0100  0000  0000  0000  :: Hex => 0001  0000  0408  4000   :: 0x0001000004084000 :: Probability => 2^{-4}
```
## Acknowledgement 
1. https://github.com/zhuby12/MILP-basedModel
