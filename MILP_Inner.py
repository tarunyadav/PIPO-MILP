import gurobipy
import sys
def s_box_ineq():
    f = open("DDT_all_min_prob.txt","r")
    data= f.readlines()
    no_of_input = int(data[0].rstrip().split()[1])
    f.close()
    ineq_list=[]
    for row in data[4:-1]:
        row_arr = row.rstrip().split(" ")[0]
        row_list=[0]*(no_of_input+1)
        const = 0
        for i in range(0,len(row_arr)):
                if(row_arr[i]=='0'):
                    row_list[i]=1
                elif (row_arr[i]=='1'):
                    row_list[i]=-1
                    const = const + 1
 
        row_list[23] = const - 1
        ineq_list = ineq_list + row_list
    return ineq_list

convpbl = s_box_ineq()
P64 = (0, 1, 2, 3, 4, 5, 6, 7, 15, 8, 9, 10, 11, 12, 13, 14, 
20, 21, 22, 23, 16, 17, 18, 19, 27, 28, 29, 30, 31, 24, 25, 26,
38, 39, 32, 33, 34, 35, 36, 37, 45, 46, 47, 40, 41, 42, 43, 44,
49, 50, 51, 52, 53, 54, 55, 48, 58, 59, 60, 61, 62, 63, 56, 57)

block_size=64
s_box_size = 8
convpbl_entry_size= (s_box_size*2) + 8
ROUND = int(sys.argv[1])
BanListlen = 0
repeatTrail = False
fix = False
#fix_diff  = [0x0000000000001000]
fix_diff  = [0x0014000010000400]
fix_pos = [0]
fix_diff_bin = [bin(diff)[2:].zfill(64) for diff in fix_diff];
fix_bit = [];
for diff_1 in fix_diff_bin:
    fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])



def PrintInner(SolveList):
    opInner = open("Inner_"+str(ROUND)+".lp","w+")
    opInner.write("Minimize\n")
    buf = ''
    sl = []
    for i in range(0,len(SolveList)):
        buf = buf + "4 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0 + 4.415037 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1 + 4.678072 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2 + 5 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_3 + 5.415037 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_4 + 6 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_5 + 7 z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_6"
        if i != len(SolveList)-1:
            buf = buf + " + "
        else:
            buf = buf + "\n"
    opInner.write(buf)
    opInner.write("Subject to\n")
    ##################
    if (fix==True):
        for b in range(0,len(fix_bit)):
            buf = ''
            for j in range(0,block_size):
                if(j in fix_bit[b]):
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 1\n"
                else:
                    buf = buf + "x" + str(fix_pos[b]) + "_" + str(j) + " = 0\n"
            opInner.write(buf)
    #################
    ##################
    if (repeatTrail==True):
        buf = ''
        for i in range(0,block_size):
            buf = buf + "x0_" +str(i) + " - x" + str(ROUND) +"_" + str(i)+" = 0 \n"
        opInner.write(buf)
    ##################
    buf = ''
    for i in range(0,len(SolveList)):
        buf = ''
        
            
        for k in range(0,8):
            buf = buf + "8 x" + str(SolveList[i][0]) + "_" + str(8*k + SolveList[i][1])
            if k != 7:
                buf = buf + " + "
        for k in range(0,8):
            buf = buf + " - y" + str(SolveList[i][0]) + "_" + str(8*k + SolveList[i][1])
        buf = buf + " >= 0\n"

        for k in range(0,8):
            buf = buf + "8 y" + str(SolveList[i][0]) + "_" + str(8*k + SolveList[i][1])
            if k != 7:
                buf = buf + " + "
        for k in range(0,8):
            buf = buf + " - x" + str(SolveList[i][0]) + "_" + str(8*k + SolveList[i][1])
        buf = buf + " >= 0\n"
        opInner.write(buf)
    
        buf = ''
        for k in range(0,int(len(convpbl)/convpbl_entry_size)):
            for l in range(0,convpbl_entry_size):
                if convpbl[convpbl_entry_size*k+l] > 0:
                    if l <=(s_box_size-1):
                        buf = buf + " + " + str(convpbl[convpbl_entry_size*k+l]) + " x" + str(SolveList[i][0]) + "_" + str((s_box_size*(s_box_size-1-l)) + SolveList[i][1])
                    if (s_box_size) <= l and l <= ((2*s_box_size)-1):
                        buf = buf + " + " + str(convpbl[convpbl_entry_size*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(s_box_size*(((2*s_box_size)-1-l)) + SolveList[i][1])
                    if (2*s_box_size) <=l and l <= ((2*s_box_size)+6):
                        buf = buf + " + " + str(convpbl[convpbl_entry_size*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-(2*s_box_size))
                    if l == ((2*s_box_size)+7):    
                        buf = buf + " >= -" + str(convpbl[convpbl_entry_size*k+l]) + "\n"
                        
                if convpbl[convpbl_entry_size*k+l] < 0:
                    if l <=(s_box_size-1):
                        buf = buf + " - " + str(-convpbl[convpbl_entry_size*k+l]) + " x" + str(SolveList[i][0]) + "_" + str((s_box_size*(s_box_size-1-l)) + SolveList[i][1])
                    if (s_box_size) <= l and l <= ((2*s_box_size)-1):
                        buf = buf + " - " + str(-convpbl[convpbl_entry_size*k+l]) + " y" + str(SolveList[i][0]) + "_" + str(s_box_size*(((2*s_box_size)-1-l)) + SolveList[i][1])
                    if (2*s_box_size) <=l and l <= ((2*s_box_size)+6):
                        buf = buf + " - " + str(-convpbl[convpbl_entry_size*k+l]) + " z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_" + str(l-(2*s_box_size))
                    if l == ((2*s_box_size)+7):    
                        buf = buf + " >= " + str(-convpbl[convpbl_entry_size*k+l]) + "\n"
                if convpbl[convpbl_entry_size*k+l] == 0:
                    if l == ((2*s_box_size)+7):
                        buf = buf + " >= " + str(convpbl[convpbl_entry_size*k+l]) + "\n"

        opInner.write(buf)
    
    buf = ''
    sl = []
    for i in range(0,ROUND):
        buf = ''
        sl = []
        sl.append(i)
        for j in range(0,8):
            sl.append(j)

            if sl not in SolveList:
                for k in range(0,8):
                    buf = buf + "x" + str(i) + "_" + str(8*k+j) + " = 0\n"
                    buf = buf + "y" + str(i) + "_" + str(8*k+j) + " = 0\n"
            sl.pop()

        if i != ROUND:
            for j in range(0,64):
                buf = buf + "x" + str(i+1) + "_" + str(P64[j]) + " - y" + str(i) + "_" + str(j) + " = 0\n"
        opInner.write(buf)

    buf = ''
    for i in SolveList:
        if i[0] == 0:
            buf = buf + "x0_" + str((8*0)+i[1]) + " + x0_" + str((8*1)+i[1]) + " + x0_" + str((8*2)+i[1]) + " + x0_" + str((8*3)+i[1]) + " + x0_" +str((8*4)+i[1]) + " + x0_" + str((8*5)+i[1]) + " + x0_" + str((8*6)+i[1]) + " + x0_" + str((8*7)+i[1])
            buf = buf + " >= 1\n"
    opInner.write(buf)

    buf = ''
    opInner.write("Binary\n")
    buf = ''
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,64):
            buf = buf + "x" + str(i) + "_" + str(j) + "\n"
        for j in range(0,64):
            buf = buf + "y" + str(i) + "_" + str(j) + "\n"
        opInner.write(buf)
    buf = ''
    for j in range(0,64):
        buf = buf + "x" + str(ROUND) + "_" + str(j) + "\n"
    opInner.write(buf)
    buf = ''
    for i in range(0,len(SolveList)):
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_0\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_1\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_2\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_3\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_4\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_5\n"
        buf = buf + "z" + str(SolveList[i][0]) + "_" + str(SolveList[i][1]) + "_6\n"
        opInner.write(buf)
        buf = ''
    opInner.close()


def strtoint(s):
    reg = 0
    s1 = ''
    s2 = ''
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
resreg = 128
filename = "Inner_Result_" + str(ROUND) + ".txt"
opResult = open(filename,'w+')

#############FIX Active S-Box##################
bl = [[0, 0], [1, 7], [2, 3], [2, 7], [3, 0], [3, 4], [3, 5], [3, 7], [4, 0], [4, 6], [4, 7], [5, 4], [6, 7]] #Solution corresponding to this particular set of S-boxes; Format: [a,b] In round a, S-box no. b is active
BanList.append(bl)
BanListlen = len(bl)
PrintInner(bl)
while True:
    i = gurobipy.read("Inner_"+str(ROUND)+".lp")
    i.optimize()
    buf = ''
    buf = buf + str(bl) + " " + str(i.getObjective().getValue()) + "\n"
    if i.getObjective().getValue() < resreg:
        resreg = i.getObjective().getValue()
        ot = open("mini_"+str(ROUND)+".txt","w+")
        ot.write(str(resreg))
        ot.close()
    for v in i.getVars():
        if v.x == 1:
            buf = buf + v.VarName + " "
    buf = buf + "\n"
    opResult.write(buf)
    opResult.flush()

