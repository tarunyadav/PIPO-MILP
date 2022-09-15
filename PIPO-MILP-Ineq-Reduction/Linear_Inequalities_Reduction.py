"""
#Parameters 
1 - name of the cipher (WARP, GIFT, TWINE, ASCON, FIDES-5, FIDES-6, SC2000-5, SC2000-6, APN-6, AES, SKINNY, PIPO)
2 - sbox: Inequalities corresponding to DDT without considering probablity of transition (based on possible/impossible transitions). These will be used for active S-box minimization  
    sbox_{prob_value}:  Inequalities corresponding to partial DDT considering the possible transitions with value {prob_value}. This will output the inequalities corresponding to pb-DDT.
     prob (Not covered in PIPO paper): Inequalities corresponding to DDT considering probablity of each transition.  This will output the inequalities corresponding to f-TT. This parameter may work pratically for 4/5-bit ciphers. For large size of S-box this is not time efficient. Therefore, in the paper Espresso based MILES is used to generate these inequalities.      
3 - GUROBI/CPLEX

#output
The .lp and .sol files are created corresponding to MILP problem and solution.
Linear inequalites will be written to .txt file in the current folder.

#Examples
python Linear_Inequalities_Reduction.py PIPO sbox GUROBI
python Linear_Inequalities_Reduction.py AES sbox_2 CPLEX
python Linear_Inequalities_Reduction.py WARP sbox GUROBI
python Linear_Inequalities_Reduction.py WARP prob CPLEX
"""
import sys
import time
import math
import numpy as np
from quine_mccluskey.qm import QuineMcCluskey
import gurobipy
from gurobipy import GRB
from docplex.mp.model import Model

try:
  import google.colab
  IN_COLAB = True
except:
  IN_COLAB = False

if (IN_COLAB==True):
  # Setup the Gurobi environment with the WLS license
  e = gurobipy.Env(empty=True)
  e.setParam('WLSACCESSID', '')
  e.setParam('WLSSECRET', '')
  e.setParam('LICENSEID', )
  e.start()

file_name = "_"+sys.argv[1]+"_"+sys.argv[2]+"_"+sys.argv[3]


def MILP_Solve(ineq_list,impossible_diff_arr):
        if (sys.argv[3] == "GUROBI"):
            start_3 = time.process_time()
            if (IN_COLAB==True):
              print("environment set")
              m = gurobipy.Model(env=e)
            else:
              m = gurobipy.Model()
            for i in range(0,len(ineq_list)):
                m.addVar(vtype=GRB.BINARY,name="z%s" % str(i))
    
            m.update()
            variables = m.getVars()
            
            for i in range(0,len(impossible_diff_arr)):
                if(i%1000==0):
                    print(str(i)+" impossible points covered (MILP model construction).")
                ineq_solve_count = (np.multiply(np.array(impossible_diff_arr[i]),np.array(ineq_list))).sum(1)
                less_than_zero = np.where(ineq_solve_count<0)[0]
                m.addConstr(sum([variables[x] for x in less_than_zero]) >=1)
            m.setObjective(sum(m.getVars()),GRB.MINIMIZE)
            m.update()
            end_3 = time.process_time()
            print(">>Time>> TTime Taken to write lp model: " + str(end_3 - start_3))
            m.write("Problem"+ file_name +".lp")
            m.optimize()
            m.write("Solution"+ file_name +".sol")
            m.setParam(GRB.Param.SolutionNumber, 1)
            sol_arr = np.array(m.X)
            final_sol = np.where(sol_arr == 1)[0].tolist()
        
        elif (sys.argv[3] == "CPLEX"):
            start_3 = time.process_time()
            m = Model()
            m.binary_var
            for i in range(0,len(ineq_list)):
                m.binary_var(name="z%s" % str(i))

            variables = [i for i in m.iter_binary_vars()]
            for i in range(0,len(impossible_diff_arr)):
                if(i%1000==0):
                    print(str(i)+" points covered")
                ineq_solve_count = (np.multiply(np.array(impossible_diff_arr[i]),np.array(ineq_list))).sum(1)
                less_than_zero = np.where(ineq_solve_count<0)[0]
                m.add_constraint(sum([variables[x] for x in less_than_zero]) >=1)
            m.set_objective("min",sum(variables))
            end_3 = time.process_time()
            print(">>Time>> TTime Taken to write lp model: " + str(end_3 - start_3))
            m.export("Problem"+ file_name +".lp")
            sol = m.solve(log_output=True)
            sol.export("Solution"+ file_name +".sol")
            print(sol.get_objective_value())
            sol_arr = np.array(sol.get_values(variables)) 
            final_sol = np.where(sol_arr == 1)[0].tolist()

        

        f = open("ineq"+ file_name +".txt","w")
        ineq_list = ineq_list.astype(int)
        for ineqlitity in final_sol:
            inequality_rotated = ineq_list[ineqlitity].tolist()[1:] + [ineq_list[ineqlitity].tolist()[0]] 
            f.write(str(inequality_rotated).replace("[","").replace("]",",\n"))    
        f.close()
        ineq_list_mod = []
        print(final_sol)
        for x in final_sol:
            ineq_list_mod.append(ineq_list[x])
        return ineq_list
    
    
def print_DDT(table):
    for row in range(len(table)):
        for col in range(len(table[row])):
            print(table[row][col],end='');
            if col == len(table[row])-1: 
                print("\n");

if (sys.argv[1] == "WARP"):
  s_box = ((0xc,0xa, 0xd,0x3, 0xe,0xb, 0xf, 0x7, 0x8, 0x9, 0x1, 0x5, 0x0, 0x2, 0x4, 0x6),);     # WARP
elif (sys.argv[1] == "GIFT"):
  s_box = ((0x1,0xa, 0x4,0xc, 0x6,0xf, 0x3, 0x9, 0x2, 0xd, 0xb, 0x7, 0x5, 0x0, 0x8, 0xe),);       # GIFT       
elif (sys.argv[1] == "TWINE"):
  s_box = ((0xc,0x0, 0xf,0xa, 0x2,0xb, 0x9, 0x5, 0x8, 0x3, 0xd, 0x7, 0x1, 0xe, 0x6, 0x4),);       # TWINE         
elif (sys.argv[1] == "ASCON"):
  s_box = ((0x4,0xb,0x1f,0x14,0x1a,0x15,0x9,0x2,0x1b,0x5,0x8,0x12,0x1d,0x3,0x6,0x1c,), (0x1e,0x13,0x7,0xe,0x0,0xd,0x11,0x18,0x10,0xc,0x1,0x19,0x16,0xa,0xf,0x17));       # ASCON  
elif (sys.argv[1] == "FIDES-5"):
  s_box = ((1,0,25,26,17,29,21,27,20,5,4,23,14,18,2,28),(15,8,6,3,13,7,24,16,30,9,31,10,22,12,11,19)); #FIDES-5
elif (sys.argv[1] == "FIDES-6"):
  s_box = ( (54,0,48,13,15,18,35,53,63,25,45,52,3,20,33,41),(8,10,57,37,59,36,34,2,26,50,58,24,60,19,14,42),(46,61,5,49,31,11,28,4,12,30,55,22,9,6,32,23),(27,39,21,17,16,29,62,1,40,47,51,56,7,43,38,44));#FIDES-6
elif (sys.argv[1] == "SC2000-5"):
  s_box = ((20,26,7,31,19,12,10,15,22,30,13,14, 4,24, 9,18),(27,11, 1,21, 6,16, 2,28,23, 5, 8, 3, 0,17,29,25)); #SC2000-5
elif (sys.argv[1] == "SC2000-6"):
  s_box = ((47,59,25,42,15,23,28,39,26,38,36,19,60,24,29,56),(37,63,20,61,55, 2,30,44, 9,10, 6,22,53,48,51,11),(62,52,35,18,14,46, 0,54,17,40,27, 4,31, 8, 5,12),(3,16,41,34,33, 7,45,49,50,58, 1,21,43,57,32,13)); #SC2000-6
elif (sys.argv[1] == "APN-6"):
  s_box = ((0,54,48,13,15,18,53,35,25,63,45,52,3,20,41,33),(59,36,2,34,10,8,57,37,60,19,42,14,50,26,58,24),(39,27,21,17,16,29,1,62,47,40,51,56,7,43,44,38),(31,11,4,28,61,46,5,49,9,6,23,32,30,12,55,22)); #APN-6
elif (sys.argv[1] == "AES"):
  s_box = ((0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76),(0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0),(0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15),(0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75),(0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84),(0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF),(0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8),(0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2),(0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73),(0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB),(0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79),(0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08),(0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A),(0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E),(0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF),(0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16))  #AES
elif (sys.argv[1] == "SKINNY"):
    s_box = ((0x65, 0x4c, 0x6a, 0x42, 0x4b, 0x63, 0x43, 0x6b, 0x55, 0x75, 0x5a, 0x7a, 0x53, 0x73, 0x5b, 0x7b), 
(0x35, 0x8c, 0x3a, 0x81, 0x89, 0x33, 0x80, 0x3b, 0x95, 0x25, 0x98, 0x2a, 0x90, 0x23, 0x99, 0x2b),
(0xe5, 0xcc, 0xe8, 0xc1, 0xc9, 0xe0, 0xc0, 0xe9, 0xd5, 0xf5, 0xd8, 0xf8, 0xd0, 0xf0, 0xd9, 0xf9),
(0xa5, 0x1c, 0xa8, 0x12, 0x1b, 0xa0, 0x13, 0xa9, 0x05, 0xb5, 0x0a, 0xb8, 0x03, 0xb0, 0x0b, 0xb9),
(0x32, 0x88, 0x3c, 0x85, 0x8d, 0x34, 0x84, 0x3d, 0x91, 0x22, 0x9c, 0x2c, 0x94, 0x24, 0x9d, 0x2d),
(0x62, 0x4a, 0x6c, 0x45, 0x4d, 0x64, 0x44, 0x6d, 0x52, 0x72, 0x5c, 0x7c, 0x54, 0x74, 0x5d, 0x7d ),
(0xa1, 0x1a, 0xac, 0x15, 0x1d, 0xa4, 0x14, 0xad, 0x02, 0xb1, 0x0c, 0xbc, 0x04, 0xb4, 0x0d, 0xbd ),
(0xe1, 0xc8, 0xec, 0xc5, 0xcd, 0xe4, 0xc4, 0xed, 0xd1, 0xf1, 0xdc, 0xfc, 0xd4, 0xf4, 0xdd, 0xfd ),
(0x36, 0x8e, 0x38, 0x82, 0x8b, 0x30, 0x83, 0x39, 0x96, 0x26, 0x9a, 0x28, 0x93, 0x20, 0x9b, 0x29 ),
(0x66, 0x4e, 0x68, 0x41, 0x49, 0x60, 0x40, 0x69, 0x56, 0x76, 0x58, 0x78, 0x50, 0x70, 0x59, 0x79 ),
(0xa6, 0x1e, 0xaa, 0x11, 0x19, 0xa3, 0x10, 0xab, 0x06, 0xb6, 0x08, 0xba, 0x00, 0xb3, 0x09, 0xbb ),
(0xe6, 0xce, 0xea, 0xc2, 0xcb, 0xe3, 0xc3, 0xeb, 0xd6, 0xf6, 0xda, 0xfa, 0xd3, 0xf3, 0xdb, 0xfb ),
(0x31, 0x8a, 0x3e, 0x86, 0x8f, 0x37, 0x87, 0x3f, 0x92, 0x21, 0x9e, 0x2e, 0x97, 0x27, 0x9f, 0x2f ),
(0x61, 0x48, 0x6e, 0x46, 0x4f, 0x67, 0x47, 0x6f, 0x51, 0x71, 0x5e, 0x7e, 0x57, 0x77, 0x5f, 0x7f ),
(0xa2, 0x18, 0xae, 0x16, 0x1f, 0xa7, 0x17, 0xaf, 0x01, 0xb2, 0x0e, 0xbe, 0x07, 0xb7, 0x0f, 0xbf ),
(0xe2, 0xca, 0xee, 0xc6, 0xcf, 0xe7, 0xc7, 0xef, 0xd2, 0xf2, 0xde, 0xfe, 0xd7, 0xf7, 0xdf, 0xff))#SKINNY
elif (sys.argv[1] == "PIPO"):
  s_box = ((0x5E, 0xF9, 0xFC, 0x00, 0x3F, 0x85, 0xBA, 0x5B, 0x18, 0x37, 0xB2, 0xC6, 0x71, 0xC3, 0x74, 0x9D), (0xA7, 0x94, 0x0D, 0xE1, 0xCA, 0x68, 0x53, 0x2E, 0x49, 0x62, 0xEB, 0x97, 0xA4, 0x0E, 0x2D, 0xD0), (0x16, 0x25, 0xAC, 0x48, 0x63, 0xD1, 0xEA, 0x8F, 0xF7, 0x40, 0x45, 0xB1, 0x9E, 0x34, 0x1B, 0xF2), (0xB9, 0x86, 0x03, 0x7F, 0xD8, 0x7A, 0xDD, 0x3C, 0xE0, 0xCB, 0x52, 0x26, 0x15, 0xAF, 0x8C, 0x69), (0xC2, 0x75, 0x70, 0x1C, 0x33, 0x99, 0xB6, 0xC7, 0x04, 0x3B, 0xBE, 0x5A, 0xFD, 0x5F, 0xF8, 0x81), (0x93, 0xA0, 0x29, 0x4D, 0x66, 0xD4, 0xEF, 0x0A, 0xE5, 0xCE, 0x57, 0xA3, 0x90, 0x2A, 0x09, 0x6C), (0x22, 0x11, 0x88, 0xE4, 0xCF, 0x6D, 0x56, 0xAB, 0x7B, 0xDC, 0xD9, 0xBD, 0x82, 0x38, 0x07, 0x7E), (0xB5, 0x9A, 0x1F, 0xF3, 0x44, 0xF6, 0x41, 0x30, 0x4C, 0x67, 0xEE, 0x12, 0x21, 0x8B, 0xA8, 0xD5), (0x55, 0x6E, 0xE7, 0x0B, 0x28, 0x92, 0xA1, 0xCC, 0x2B, 0x08, 0x91, 0xED, 0xD6, 0x64, 0x4F, 0xA2), (0xBC, 0x83, 0x06, 0xFA, 0x5D, 0xFF, 0x58, 0x39, 0x72, 0xC5, 0xC0, 0xB4, 0x9B, 0x31, 0x1E, 0x77), (0x01, 0x3E, 0xBB, 0xDF, 0x78, 0xDA, 0x7D, 0x84, 0x50, 0x6B, 0xE2, 0x8E, 0xAD, 0x17, 0x24, 0xC9), (0xAE, 0x8D, 0x14, 0xE8, 0xD3, 0x61, 0x4A, 0x27, 0x47, 0xF0, 0xF5, 0x19, 0x36, 0x9C, 0xB3, 0x42), (0x1D, 0x32, 0xB7, 0x43, 0xF4, 0x46, 0xF1, 0x98, 0xEC, 0xD7, 0x4E, 0xAA, 0x89, 0x23, 0x10, 0x65), (0x8A, 0xA9, 0x20, 0x54, 0x6F, 0xCD, 0xE6, 0x13, 0xDB, 0x7C, 0x79, 0x05, 0x3A, 0x80, 0xBF, 0xDE), (0xE9, 0xD2, 0x4B, 0x2F, 0x0C, 0xA6, 0x95, 0x60, 0x0F, 0x2C, 0xA5, 0x51, 0x6A, 0xC8, 0xE3, 0x96), (0xB0, 0x9F, 0x1A, 0x76, 0xC1, 0x73, 0xC4, 0x35, 0xFE, 0x59, 0x5C, 0xB8, 0x87, 0x3D, 0x02, 0xFB)) #PIPO    
DDT_SIZE = (len(s_box)*len(s_box[0]))
input_size = int(math.log(DDT_SIZE,2))
DDT = np.zeros( (DDT_SIZE,DDT_SIZE) )
DDT = DDT.astype(int)
sbox_val = []


for p2 in range(DDT_SIZE):
    row = p2 >> 4
    col = p2 & 15
    sbox_val.append(s_box[row][col]);

for p1 in range(DDT_SIZE):
	for p2 in range(DDT_SIZE):
		XOR_IN = np.bitwise_xor(p1,p2);
		XOR_OUT = np.bitwise_xor(sbox_val[p1],sbox_val[p2]);
		DDT[XOR_IN][XOR_OUT] += 1


diff_arr = []
diff_arr_qm = []
diff_arr_with_1 = []
impossible_diff_arr=[]
impossible_diff_arr_qm=[]
impossible_diff_arr_new=[]
if ("sbox" in sys.argv[2]):
    check = False
    prob_point = 0
    if ("_" in sys.argv[2]):
       prob_point = int(sys.argv[2].split("_")[1])
       check = True
    for row in range(len(DDT)):
            row_hex = bin(row)[2:].zfill(input_size);
            row_arr = [int(i) for i in row_hex];
            for col in range(len(DDT[row])):
                col_hex = bin(col)[2:].zfill(input_size);
                col_arr = [int(i) for i in col_hex];
                #if(DDT[row][col]!=0):
                    
                if ((DDT[row][col]==prob_point)==check):
                    diff_arr += [row_arr+col_arr];
                    diff_arr_with_1 += [[1]+row_arr+col_arr];
                    diff_arr_qm += [row_hex+col_hex];
                else:
                    impossible_diff_arr += [[1]+row_arr+col_arr];
                    impossible_diff_arr_qm += [row_hex+col_hex];
                    impossible_diff_arr_new += [row_arr+col_arr];
                

unique_entries = np.unique(DDT)
unique_entries_count = len(np.unique(DDT))
print(unique_entries)
if (sys.argv[2] == "prob"):               
    diff_arr = []
    diff_arr_with_1 = []
    impossible_diff_arr=[]
    impossible_diff_arr_qm=[]
    impossible_diff_arr_new=[]
    for row in range(len(DDT)):
            row_bin = bin(row)[2:].zfill(input_size);
            row_arr = [int(i) for i in row_bin];
            for col in range(len(DDT[row])):
                col_bin = bin(col)[2:].zfill(input_size);
                col_arr = [int(i) for i in col_bin];
                if(DDT[row][col]!=0):
                    DDT_bin = "".join(['0']*(unique_entries_count-2))
                    for num in range(1,len(unique_entries)-1):
                        if (DDT[row][col] == unique_entries[num]):
                            DDT_bin = DDT_bin[0:len(DDT_bin) - np.where(unique_entries==unique_entries[num])[0][0]] +  '1' + DDT_bin[len(DDT_bin) - np.where(unique_entries==unique_entries[num])[0][0] +1:] 
                        

                    int_DDT_bin = int(DDT_bin,2);
                    DDT_arr = [int(i) for i in DDT_bin];
                    diff_arr += [row_arr+col_arr+DDT_arr];
                    diff_arr_with_1 += [[1]+row_arr+col_arr+DDT_arr];
                    for k in range(0,pow(2,unique_entries_count-2)):
                        if (k!=int_DDT_bin):
                            im_bin = bin(k)[2:].zfill(unique_entries_count-2);
                            im_arr = [int(i) for i in im_bin];
                            impossible_diff_arr += [[1] + row_arr+col_arr+im_arr];
                            impossible_diff_arr_qm += [row_bin+col_bin+im_bin]
                else:
                    for k in range(0,pow(2,unique_entries_count-2)):
                            im_bin = bin(k)[2:].zfill(unique_entries_count-2);
                            im_arr = [int(i) for i in im_bin];
                            impossible_diff_arr += [[1]+row_arr+col_arr+im_arr];
                            impossible_diff_arr_qm += [row_bin+col_bin+im_bin];

ineq_list = []
print(">>> No. of possible points: " + str(len(diff_arr_with_1)))
print(">>> No. of impossible points: " + str(len(impossible_diff_arr)))


start_1 = time.process_time()
print(">>> QM Started")
qm = QuineMcCluskey()
qm.n_bits = 2*input_size
if (sys.argv[2] == "prob"):    
    qm.n_bits = 2*input_size + unique_entries_count -2
qm.profile_cmp = 0   
qm.profile_xor = 0    
qm.profile_xnor = 0  
terms = set(impossible_diff_arr_qm) |  set([])
  
prime_implicants = qm._QuineMcCluskey__get_prime_implicants(terms)
print(len(prime_implicants))
essential_implicants = qm._QuineMcCluskey__get_essential_implicants(prime_implicants,set([]))
print(len(essential_implicants))
   
prime_implicants_list = list(prime_implicants)
print(">>> No. of Prime Implicants: "+ str(len(prime_implicants_list)))
essential_implicants_list = list(essential_implicants)
print(">>> No. of Essential Prime Implicants: "+ str(len(essential_implicants_list)))
print(">>> Using Essential Prime Implicants...")
implicants_list  = essential_implicants_list

ineq_map = {"0":1,"1":-1,"-":0}
for i in range(0,len(implicants_list)):
    ineq_list.append([implicants_list[i].count("1")-1] + [ineq_map[x] for x in implicants_list[i]])
print(">>> No. of Inequalities: "+ str(len(ineq_list)))
print(">>> QM Ended")
end_1 = time.process_time()
print(">>Time>> TTime Taken to get essential prime implicants inequalities: " + str(end_1 - start_1))

print(len(ineq_list))

start_2 = time.process_time()
ineq_list_orig = ineq_list.copy()

for i in range(0,len(np.array(impossible_diff_arr))):
    if(i%1000==0):
        print(str(i)+" impossible points covered (Addition of new inequalities).")
    ineq_solve_count = (np.multiply(np.array(impossible_diff_arr[i]),np.array(ineq_list_orig))).sum(1)
    less_than_zero = np.where(ineq_solve_count<0)[0]
    ineq_list.append(np.array([ineq_list_orig[x] for x in less_than_zero]).sum(axis=0))
ineq_list.append(np.array(ineq_list_orig).sum(axis=0))    
end_2 = time.process_time()
print(">>Time>> Time Taken to write new inequalities: " + str(end_2 - start_2))
 
print("Number of Inequalities: " + str(len(ineq_list)))
ineq_list = MILP_Solve(np.array(ineq_list),np.array(impossible_diff_arr))
