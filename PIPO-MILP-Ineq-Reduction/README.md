# PIPO-MILP-Ineq-Reduction
Source code for QM based algorithm to get reduced set of linear inequalities corresponding to the DDT of ciphers with 8-bit S-boxes
## Source Code 
### There is one file in this source code.
* _Linear_Inequalities_Reduction.py_

## Reduction of Linear Inequalities 
_Linear_Inequalities_Reduction.py_ contains the source code to 
* Compute DDT of S-box
* To generate linear inequalities using essential prime implicants of QM algorithm
* To introduce new set of linear inequalities by adding selective inequalities
* To reduce the number of linear ineuqalities by constructing MILP problem whcih is solved using GUROBI/CPLEX solver

## Parameters 
1 - name of cipher (WARP, GIFT, TWINE, ASCON, FIDES-5, FIDES-6, SC2000-5, SC2000-6, APN-6, AES, SKINNY, PIPO)\
2 - **sbox**: Inequalities corresponding to DDT without considering probablity of transition (based on possible/impossible transitions). These will be used for active S-box minimization  \
    **sbox_{prob_value}**:  Inequalities corresponding to partial DDT considering the possible transitions with value {prob_value}. This will output the inequalities corresponding to pb-DDT.\
    **prob** (Not covered in PIPO paper): Inequalities corresponding to DDT considering probablity of each transition.  This will output the inequalities corresponding to f-TT. This parameter may work pratically for 4/5-bit ciphers. For large size of S-box this is not time efficient. Therefore, in the paper Espresso based MILES is used to generate these inequalities. \
3 - GUROBI/CPLEX

## Examples
```python Linear_Inequalities_Reduction.py PIPO sbox GUROBI```\
```python Linear_Inequalities_Reduction.py AES sbox_2 CPLEX```\
```python Linear_Inequalities_Reduction.py WARP sbox GUROBI```\
```python Linear_Inequalities_Reduction.py WARP prob CPLEX```\
The .lp and .sol files are created corresponding to MILP problem and solution.\
The minimized set of inequalities will be written to a .txt file in the current folder.

## Acknowledgement
1. https://github.com/tpircher-zz/quine-mccluskey
2. https://pypi.org/project/quine-mccluskey/
