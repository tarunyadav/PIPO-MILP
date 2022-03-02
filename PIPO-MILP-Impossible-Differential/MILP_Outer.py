import gurobipy
import sys
import string
from  math import floor
def s_box_ineq():
    f = open("LinearInequalities_Outer.txt","r")
    data= f.readlines()
    no_of_input = int(data[0].rstrip().split()[2])
    f.close()
    ineq_list=[]
    for row in data[1:]:
        row_list=[0]*(no_of_input+1)
        row_arr = row.rstrip().split(" ")
        row_list=[0]*(no_of_input+1)
        for i in range(0,len(row_arr)):
                if(row_arr[i]=='+'):
                    row_list[i]= 1
                elif (row_arr[i]=='-'):
                    row_list[i]= -1
                elif (row_arr[i]=='0'):
                    row_list[i]= 0
        row_list[no_of_input] = int(row_arr[no_of_input])
        ineq_list = ineq_list + row_list
    return ineq_list

conv = s_box_ineq()

P64 = (0, 1, 2, 3, 4, 5, 6, 7, 15, 8, 9, 10, 11, 12, 13, 14, 
20, 21, 22, 23, 16, 17, 18, 19, 27, 28, 29, 30, 31, 24, 25, 26,
38, 39, 32, 33, 34, 35, 36, 37, 45, 46, 47, 40, 41, 42, 43, 44,
49, 50, 51, 52, 53, 54, 55, 48, 58, 59, 60, 61, 62, 63, 56, 57)

block_size=64
s_box_size = 8
conv_entry_size= (s_box_size*2) + 1
ROUND = int(sys.argv[1])
#act = (1, 2, 3, 5, 7, 10, 13, 16, 18, 20, 22, 24, 26)
#act = (1, 2, 4, 6, 9, 11, 13, 16, 18, 20,  20, 20, 20, 20)
act = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
act[ROUND-1] = int(sys.argv[2])  # Try with 1
BanListlen = 0
fix = True
fix_diff = [0x0000000000000001,0x0000000000000001]
fix_pos = [0,ROUND]


fix_diff_bin = [bin(diff)[2:].zfill(64) for diff in fix_diff];
fix_bit = [];
for diff_1 in fix_diff_bin:
    fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])


def PrintOuter(BanList):
    opOuter = open("Outer_"+str(ROUND)+"_Impossible.lp",'w+')
    opOuter.write("Minimize\n")
    buf = ''
    for i in range(0,64):
        if (i!=63):
            buf = buf + 'x0_' + str(i) + ' + '
        else:
            buf = buf + 'x0_' + str(i)
    opOuter.write(buf)
    opOuter.write('\n')
    opOuter.write("Subject to\n")
    #######################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            fix_s_box_next = [(i%s_box_size) for i in fix_bit[b]]
            fix_s_box_prev = [(P64.index(i)%s_box_size) for i in fix_bit[b]]
            for j in range(0,s_box_size):
                    if (fix_pos[b]!=0):
                        if(j in fix_s_box_prev):
                            buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 0\n"
                    if (fix_pos[b]!=ROUND):
                        if(j in fix_s_box_next):
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opOuter.write(buf)
    ########################
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,block_size):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opOuter.write(buf)
    #################
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,s_box_size):
            buf = ''
            for k in range(0,s_box_size):
                buf = buf +  "x" + str(i) + "_" + str(s_box_size*k+j)
                if k != (s_box_size-1):
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
            for k in range(0,s_box_size):
                buf = buf + "x" + str(i) + "_" + str(s_box_size*k+j) + " - a" + str(i) + "_" + str(j) + " <= 0\n"
            for k in range(0,int(len(conv)/conv_entry_size)):
                for l in range(0,conv_entry_size):
                    if conv[conv_entry_size*k+l] > 0:
                        if l <= (s_box_size-1):
                            buf = buf + " + " + str(conv[conv_entry_size*k+l]) + " x" + str(i) + "_" + str((s_box_size*(s_box_size-1-l)) + j)
                        if (s_box_size) <= l and l <= ((2*s_box_size)-1):
                            buf = buf + " + " + str(conv[conv_entry_size*k+l]) + " x" + str(i+1) + "_" + str(P64[s_box_size*(((2*s_box_size)-1-l))+ j])
                        if l == (2*s_box_size):
                            buf = buf + " >= -" + str(conv[conv_entry_size*k+l]) + "\n"
                    if conv[conv_entry_size*k+l] < 0:
                        if l <= (s_box_size-1):
                            buf = buf + " - " + str(-conv[conv_entry_size*k+l]) + " x" + str(i) + "_" + str((s_box_size*(s_box_size-1-l)) + j)
                        if (s_box_size) <= l and l <= ((2*s_box_size)-1):
                            buf = buf + " - " + str(-conv[conv_entry_size*k+l]) + " x" + str(i+1) + "_" + str(P64[s_box_size*(((2*s_box_size)-1-l))+ j])
                        if l == (2*s_box_size):
                            buf = buf + " >= " + str(-conv[conv_entry_size*k+l]) + "\n"
                    if conv[conv_entry_size*k+l] == 0:
                        if l == (2*s_box_size):
                            buf = buf + " >= " + str(conv[conv_entry_size*k+l]) + "\n"

            opOuter.write(buf)
                 
    buf = ''
    for i in range(0,block_size):
        buf = buf + "x0_" + str(i)
        if i != block_size-1:
            buf = buf + " + "
        if i == block_size-1:
            buf = buf + " >= 1\n"
    opOuter.write(buf)

    buf = ''
    for i in BanList:
        for j in range(0,len(i)):
            buf = buf + "a" + str(i[j][0]) + "_" + str(i[j][1])
            if j != len(i)-1:
                buf = buf + " + "
            else:
                buf = buf + " <= " + str(len(i)-1) + '\n'
    opOuter.write(buf)
    buf = ''
    for i in range(0,ROUND):
        for j in range(0,s_box_size):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND-1 or j != (s_box_size-1):
                buf = buf + " + "
            else:
                buf = buf + " >= "
    if act[ROUND-1] > BanListlen:
        buf = buf + str(act[ROUND-1]) + "\n"
    else:
        buf = buf + str(BanListlen) + "\n"
    opOuter.write(buf)

    opOuter.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,s_box_size):
            buf = buf + "a" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    for i in range(0,ROUND+1):
        buf = ''
        for j in range(0,block_size):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    opOuter.close()
    



def strtoint(s):
    reg = 0
    s1 = ''
    s2 = ''
    res = 0
    result = []
    for i in range(0,len(s)):
        if s[i] == '_':
            reg = 1
        if s[i] >= '0' and s[i]<= '9':
            if reg == 0:
                s1 = s1 + s[i]
            if reg == 1:
                s2 = s2 + s[i]
        
    result.append(int(s1))
    result.append(int(s2))
    return result

BanList = []
bl = []
blstring = []
resreg = 64
filename = "64_Result_" + str(ROUND) + "_Impossible.txt"
opResult = open(filename,'w+')

BanList=[]
iter_count_0 = 1
iter_count_1 = 0
ImpossibleOuter = open("Outer_"+str(ROUND)+"_Impossible_Template.lp",'r')
OuterLines = ImpossibleOuter.readlines()
ImpossibleOuter.close()
#######To get Template#######
# PrintOuter(BanList)
# sys.exit()
while True:
    
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            fix_s_box_next = [(i%s_box_size) for i in fix_bit[b]]
            fix_s_box_prev = [(P64.index(i)%s_box_size) for i in fix_bit[b]]
            for j in range(0,s_box_size):
                    if (fix_pos[b]!=0):
                        if(j in fix_s_box_prev):
                            buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]-1) + "_" + str(j) + " = 0\n"
                    if (fix_pos[b]!=ROUND):
                        if(j in fix_s_box_next):
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                        else:
                            buf = buf + "a" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"

    if (fix==True):
        for b in range(0,len(fix_bit)):
            for j in range(0,block_size):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"

    OuterLines[3:147] = [e+"\n"  for e in buf.split("\n")][:-1]
    ImpossibleOuterWrite = open("Outer_"+str(ROUND)+"_Impossible.lp",'w')
    ImpossibleOuterWrite.writelines(OuterLines)
    ImpossibleOuterWrite.close()
    o = gurobipy.read("Outer_"+str(ROUND)+"_Impossible.lp")
    o.optimize()
    iter_count_1 = iter_count_1 + 1
    if(o.getAttr("SolCount")!=0):
            print("No. of Solultions: " + str(o.getAttr("SolCount"))+"\n")
            print ("Iteratino No. - " + str(iter_count_0) + "_"+ str(iter_count_1) + "\n")

            fix_diff[1] = fix_diff[1] << 1
            if (iter_count_1==64):
                iter_count_0 = iter_count_0 + 1
                fix_diff[0] = fix_diff[0] << 1
                fix_diff[1] = 0x0000000000000001
                iter_count_1 = 0
            fix_diff_bin = [bin(diff)[2:].zfill(64) for diff in fix_diff];
            fix_bit = [];
            for diff_1 in fix_diff_bin:
                fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])
            continue
    else:
         
        print(fix_diff)
        print(fix_diff_bin)
        sys.exit()
