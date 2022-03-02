import gurobipy
import sys
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
key_size = 128
conv_entry_size= (s_box_size*2) + 1
ROUND = int(sys.argv[1])
#act = (1, 2, 3, 5, 7, 10, 13, 16, 18, 20, 22, 24, 26)
#act = (1, 2, 4, 6, 9, 11, 13, 16, 18, 20,  20, 20, 20, 20)
act = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
act[ROUND-1] = int(sys.argv[2])  # Try with 1
BanListlen = 0
#############################
fix = False           # Make it True if want to fix a difference (need to set fix_diff and fix_pos too)
repeatTrail = False  # Make it True to serch trails with same input and output difference
#fix_bit = [[20,22,52,54]]
#fix_diff = [0x0000000000000402,0x0000000002020000,0x0000000002020000]
#fix_pos = [1,3,11]
#fix_diff = [0x8880888088888000]
fix_diff  = [0x0000000000001000]
fix_pos = [0]
fix_diff_bin = [bin(diff)[2:].zfill(64) for diff in fix_diff];
fix_bit = [];
for diff_1 in fix_diff_bin:
    fix_bit.append([len(diff_1)-1-i for i in range(0,len(diff_1)) if diff_1[i]=="1" ])
##################################

def PrintOuter(BanList):
    opOuter = open("Outer_"+str(ROUND)+".lp",'w+')
    opOuter.write("Minimize\n")
    buf = ''
    for i in range(0,ROUND):
        for j in range(0,s_box_size):
            buf = buf + "a" + str(i) + "_" + str(j)
            if i != ROUND-1 or j != (s_box_size-1):
                buf = buf + " + "
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
    ##################
    if (repeatTrail==True):
        buf = ''
        for i in range(0,block_size):
            buf = buf + "x0_" +str(i) + " - x" + str(ROUND) +"_" + str(i)+" = 0 \n"
        opOuter.write(buf)
    ##################
    buf = ''
    for i in range(0,ROUND):
        buf = ''      
        for p in range(0,64):
            q=p
            if (i%2!=0):
               q  = q + 64
            buf = buf + "x" + str(i) + "_" + str(p) + " + k" + str(q) + " - u" + str(i) + "_" + str(p) + " >= 0" + "\n"
            buf = buf + "x" + str(i) + "_" + str(p) + " - k" + str(q) + " + u" + str(i) + "_" + str(p) + " >= 0" + "\n"
            buf = buf + "- 1 x" + str(i) + "_" + str(p) + " + k" + str(q) + " + u" + str(i) + "_" + str(p) + " >= 0" + "\n"
            buf = buf + "x" + str(i) + "_" + str(p) + " + k" + str(q) + " + u" + str(i) + "_" + str(p) + " <= 2" + "\n"
        opOuter.write(buf)
        buf = ''
        for j in range(0,s_box_size):
            buf = ''
            for k in range(0,s_box_size):
                buf = buf +  "u" + str(i) + "_" + str(s_box_size*k+j)
                if k != (s_box_size-1):
                    buf = buf + " + "
            buf = buf + " - a" + str(i) + "_" + str(j) + " >= 0\n"
            for k in range(0,s_box_size):
                buf = buf + "u" + str(i) + "_" + str(s_box_size*k+j) + " - a" + str(i) + "_" + str(j) + " <= 0\n"

            for k in range(0,int(len(conv)/conv_entry_size)):
                for l in range(0,conv_entry_size):
                    if conv[conv_entry_size*k+l] > 0:
                        if l <= (s_box_size-1):
                            buf = buf + " + " + str(conv[conv_entry_size*k+l]) + " u" + str(i) + "_" + str((s_box_size*(s_box_size-1-l)) + j)
                        if (s_box_size) <= l and l <= ((2*s_box_size)-1):
                            buf = buf + " + " + str(conv[conv_entry_size*k+l]) + " x" + str(i+1) + "_" + str(P64[s_box_size*(((2*s_box_size)-1-l))+ j])
                        if l == (2*s_box_size):
                            buf = buf + " >= -" + str(conv[conv_entry_size*k+l]) + "\n"
                    if conv[conv_entry_size*k+l] < 0:
                        if l <= (s_box_size-1):
                            buf = buf + " - " + str(-conv[conv_entry_size*k+l]) + " u" + str(i) + "_" + str((s_box_size*(s_box_size-1-l)) + j)
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
    for i in range(0,key_size):
        buf = buf + "k" + str(i)
        if i != key_size-1:
            buf = buf + " + "
        if i == key_size-1:
            buf = buf + " >= 1\n"
    opOuter.write(buf)
    #buf = ''
    #buf = buf + "a0_0 + a0_1 + a0_2 + a0_3 + a0_4 + a0_5 + a0_6 + a0_7 = 1\n"
    #buf = buf + "a1_0 + a1_1 + a1_2 + a1_3 + a1_4 + a1_5 + a1_6 + a1_7 = 1\n"
    #buf = buf + "a2_0 + a2_1 + a2_2 + a2_3 + a2_4 + a2_5 + a2_6 + a2_7 = 2\n"
    #buf = buf + "a3_0 + a3_1 + a3_2 + a3_3 + a3_4 + a3_5 + a3_6 + a3_7 = 4\n"
    #buf = buf + "a4_0 + a4_1 + a4_2 + a4_3 + a4_4 + a4_5 + a4_6 + a4_7 = 3\n"
    #buf = buf + "a5_0 + a5_1 + a5_2 + a5_3 + a5_4 + a5_5 + a5_6 + a5_7 = 1\n"
    #buf = buf + "a6_0 + a6_1 + a6_2 + a6_3 + a6_4 + a6_5 + a6_6 + a6_7 = 1\n"
    #opOuter.write(buf)

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
    for i in range(0,ROUND):
        buf = ''
        for j in range(0,block_size):
            buf = buf + "u" + str(i) + "_" + str(j) + "\n"
        opOuter.write(buf)
    buf = ''
    for i in range(0,key_size):
        buf = buf + "k" + str(i) + "\n"
    opOuter.write(buf)
    opOuter.close()
    



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
resreg = 64
filename = "Outer_Result_" + str(ROUND) + ".txt"
opResult = open(filename,'w+')


#BanList = [[[0, 1], [1, 2], [2, 0], [2, 3], [3, 0], [3, 1], [3, 4], [3, 6], [4, 2], [4, 5], [4, 7], [5, 2], [6, 5]],[[0, 7], [1, 6], [2, 2], [2, 6], [3, 0], [3, 2], [3, 3], [3, 7], [4, 1], [4, 2], [4, 3], [5, 7], [6, 2]],[[0, 3], [1, 0], [2, 5], [2, 7], [3, 0], [3, 1], [3, 3], [3, 6], [4, 1], [4, 2], [4, 7], [5, 2], [6, 3]],[[0, 2], [1, 7], [2, 4], [2, 6], [3, 0], [3, 2], [3, 5], [3, 6], [4, 0], [4, 1], [4, 7], [5, 1], [6, 6]],[[0, 1], [1, 0], [2, 0], [2, 4], [3, 1], [3, 2], [3, 4], [3, 5], [4, 3], [4, 4], [4, 5], [5, 1], [6, 4]]]  # It is used to ban already identified solution and find a new solution
while True:
    PrintOuter(BanList)
    o = gurobipy.read("Outer_"+str(ROUND)+".lp")
    o.optimize()
    obj = o.getObjective()
    #print(obj)
    try:
        if obj.getValue() < act[ROUND-1]+64:
            bl = []
            blstring = []
            for v in o.getVars():
                if v.x == 1 and v.VarName[0] == 'a':
                    blstring.append(v.VarName)
            for b in blstring:
                bl.append(strtoint(b))
            BanList.append(bl)
            BanListlen = len(bl)
            print(bl)
            opResult.write(str(bl)+"\n")
            buf = ''
            for v in o.getVars():
                if v.x == 1:
                    buf = buf + v.VarName + " "
            buf = buf + "\n"
            opResult.write(buf)
            opResult.flush()
            opResult.flush()

        else:
            break
    except:
        continue;

