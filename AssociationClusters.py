import numpy as np
import re
import operator

def printInputMtx():
    print("====== Doc-KW Frequency matrix (F) =======")
    for i in range(nd):
        print("\tD",i, end='')
    print("")
    for i in range(nk):
        print(kStr[i], end='')
        for j in range(nd):
            print("\t", A[i][j], end='')
        print("")

def printCorrMtx():
    print("====== Correlation matrix (C) =======")
    for i in range(nk):
        print("\t",kStr[i], end='')
    print("")
    for i in range(nk):
        print(kStr[i], end='')
        for j in range(nk):
            print("\t", C[i][j], end='')
        print("")

def printNormMtx():
    print("====== Normalized Correlation matrix (S) =======")
    for i in range(nk):
        print("\t\t",kStr[i], end='')
    print("")
    for i in range(nk):
        print(kStr[i], end='')
        for j in range(nk):
            print("\t\t", round(N[i][j],4), end='')
        print("")

A = [] # Input Matrix
C = [] # Correlation Matrix
N = [] # Normalized C Matrix

kStr = [i for i in input("Enter Keywords (Default='Dog Cat Tiger'): ").split()]
nk = len(kStr)
nd = input("Enter Document Number(Default=6): ")
if(kStr == "" or nd == ""):
    kStr = ["Dog","Cat","Tiger"]
    nk = 3
    nd = 6
    A = np.array([[3, 0, 2, 0, 1, 1], [4, 3, 7, 0, 0, 1], [2, 5, 2, 6,3, 1]])
else:
    nk = int(nk)
    nd = int(nd)
    A = np.zeros((nk, nd))
    for i in range(nk):
        for j in range(nd):
            A[i][j] = int(input("Enter Freq(K"+str(i)+",D"+str(j)+"): "))


printInputMtx()
C = A.dot(A.transpose())
printCorrMtx()
N = np.copy(C).astype(float)
for i in range(nk):
    for j in range(i,nk):
        s = C[i][j]/(C[i][i]+C[j][j]-C[i][j])
        N[i][j] = s # cross set value
        N[j][i] = s # cross set value

printNormMtx()
q = np.zeros(nk)

for i in range(nk):
    q[i] = float(input("Enter Query weight for "+kStr[i]+": "))
for i in range(nk):
    if q[i] != 0:
        max_val = N[i][0]
        max_i = 0
        newStr = ""
        for j in range(nk):
            if i != j:
                if N[i][j] > max_val:
                    max_val = N[i][j]
                    max_i = j
                    newStr = " + " + str(N[i][j]) + kStr[j]
                elif N[i][j] == max_val:
                    newStr += " + " + str(N[i][j]) + kStr[j]
        
        newStr = str(q[i]) + "(" + kStr[i] + newStr + ")"
        print(newStr)
