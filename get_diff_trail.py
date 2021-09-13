#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 18:40:37 2020

@author: tarunyadav
"""

import sys
filename = sys.argv[1]
blocksize= int(sys.argv[3]);
f1 = open(filename,"r");
data = f1.readlines()
data_copy = [a for a in data];
for a in data_copy:
    if ("*" in a):
        data.remove(a)
#print(data)
f1.close()
diff_sbox_line = data[2*int(sys.argv[2]) - 2]
diff_differential_line = data[2*int(sys.argv[2]) - 1]

diff_prob = diff_sbox_line.split("]]")[1].strip()
diff_differential_line_arr = diff_differential_line.split()

def print_binary_data(data,prob):
    for i in range(0,len(data),4):
        print(data[i:i+4],end='  ');
    print(":: Hex => ",end='');
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='  ')
    print(" :: ",end='0x')
    for i in range(0,len(data),16):
        print(hex(int(data[i:i+16],2))[2:].zfill(4),end='')
    print(" :: Probability => 2^{-"+str(prob)+"}")
    print("");

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
round_bit_arr  = []
round_bit_arr_y = []
prob_arr = []
for var in diff_differential_line_arr:
    if (var[0] == 'x'):
        round_bit_arr += [strtoint(var)]
    elif (var[0] == 'y'):
        round_bit_arr_y += [strtoint(var)]
    elif (var[0] == 'z'):
        new_var = var.split("_");
        prob_arr += [strtoint("_".join([new_var[0],new_var[2]]))]
no_of_rounds = max([_[0] for _ in round_bit_arr])


print("Differential Probability for " + str(no_of_rounds) + " rounds of PIPO_"+str(blocksize)+" is 2^{-" + str(diff_prob) + "}")
for r in range(0,no_of_rounds+1):
    print("The input difference of the round "+ str(r)+" is: ");
    diff_bits = list("0"*blocksize);

    active_bits = [a[1] for a in round_bit_arr if a[0]==r]
    for bit in active_bits:
        diff_bits[len(diff_bits)-1-bit] = "1";
    probability = 0;
    if (r>0):
        round_prob  = [a[1] for a in prob_arr if a[0]==r-1]
        for prob in round_prob:
            if (prob==6):
                probability += 7;
            elif (prob==5):
                probability += 6;
            elif (prob==4):
                probability += 5.415037;
            elif (prob==3):
                probability += 5;
            elif (prob==2):
                probability += 4.678072;
            elif (prob==1):
                probability += 4.415037;
            elif (prob==0):
                probability += 4;
    print_binary_data("".join(diff_bits),probability);
