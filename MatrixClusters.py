import numpy as np
import re
import operator

def printInputMtx():
    print("====== KW Distance matrix =======")
    for i in range(nk):
        print("\t"+kStr[i], end='')
    print("")
    for i in range(nk):
        print(kStr[i], end='')
        for j in range(nk):
            print("\t", A[i][j], end='')
        print("")

def printInputNormMtx():
    print("====== KW Distance matrix (Normalized) =======")
    for i in range(nk):
        print("\t"+kStr[i], end='')
    print("")
    for i in range(nk):
        print(kStr[i], end='')
        for j in range(nk):
            if i!=j:
                print("\t", round(B[i][j],2), end='')
            else:
                print("\t-", end='')
        print("")

def printCorrMtx():
    print("====== Correlation matrix (C) =======")
    for i in range(ns):
        print("\tS",i, end='')
    print("")
    for i in range(ns):
        print("S",i, end='')
        for j in range(ns):
            print("\t", round(C[i][j],2), end='')
        print("")

def printNormMtx():
    print("====== Normalized Correlation matrix (S) =======")
    for i in range(ns):
        print("\t\tS",i, end='')
    print("")
    for i in range(ns):
        print("S",i, end='')
        for j in range(ns):
            print("\t\t", round(N[i][j],4), end='')
        print("")

A = [] # Input Matrix
B = [] # Normalized Input
C = [] # Correlation Matrix
N = [] # Normalized C Matrix

stem = []
kStr = [i for i in input("Enter Keywords (Default=Bird Cat Dog Kitty Puppy Tiger): ").split()]
nk = len(kStr)
ns = 0
    
if(nk == 0):
    kStr = ["Bird","Cat","Dog","Kitty","Puppy","Tiger"]
    nk = 6
    ns = 4
    stem = [3,1,0,1,0,2]
    A = np.array([  [0,2,5,7,float("inf"),3],
                    [2,0,3,5,6,3],
                    [5,3,0,12,3,2],
                    [7,5,12,0,float("inf"),14],
                    [float("inf"),6,3,float("inf"),0,7],
                    [3,3,2,14,7,0]])
else:
    nk = int(nk)

    for i in range(nk):
        stem.append(int(input("Stem of "+kStr[i]+"? (Number 0,1,2,3... only): ")))
    ns = len(stem)

    A = np.zeros((nk, nk))
    for i in range(nk):
        for j in range(nk):
            A[i][j] = float(input("Enter Distance("+kStr[i]+",K"+kStr[j]+"): "))


printInputMtx()
# Normalize I/P
B = np.zeros((nk, nk))
for i in range(nk):
        for j in range(nk):
            if A[i][j] != 0:
                B[i][j] = 1.0/A[i][j]
printInputNormMtx()

# Correlation
C = np.zeros((ns,ns))
for i in range(nk):
    for j in range(i,nk):
        if stem[i]!=stem[j]:
            C[stem[i]][stem[j]] += B[i][j]
            C[stem[j]][stem[i]] += B[i][j]
printCorrMtx()

# Normalize C
N = np.zeros((ns,ns))
stem_sorted = np.sort(stem)
unique_elements, counts_elements = np.unique(stem_sorted, return_counts=True)
for i in range(ns):
    for j in range(i,ns):
        if i!=j:
            val = C[i][j] / counts_elements[i] / counts_elements[j]
            N[i][j] = val
            N[j][i] = val

printNormMtx()
q = np.zeros(nk)
maxC = np.zeros(ns)
maxC_i = []
for i in range(nk):
    q[i] = float(input("Enter Query weight for "+kStr[i]+": "))
for i in range(ns):
    maxC[i] = N[i][0]
    maxC_i.append([])
    for j in range(ns):
        if i != j:
            if N[i][j] > maxC[i]:
                maxC[i] = N[i][j]
                maxC_i[i] = []
                maxC_i[i].append(j)
            elif N[i][j] == maxC[i]:
                maxC_i[i].append(j)
    print(maxC_i[i])
        
newStr = ""
for i in range(nk):
    if q[i] != 0:
        if q[i] > 0:
            newStr += " + "
        newStr += str(q[i]) + "(S" + str(stem[i])
        for j in range(len(maxC_i[stem[i]])):
            
            newStr += " + "+ str(round(maxC[maxC_i[stem[i]][j]],2)) + "S" + str(maxC_i[stem[i]][j])
        newStr += ")"

print(newStr)