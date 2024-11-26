from math import *;
from queue import *;

# graph definition
G = {
    1 : {2:-1, 3:4, 5:2},
    2 : {1:8, 3:5, 4:2, 7:6, 8:7},
    3 : {1:4, 2:5, 6:3, 7:4},
    4 : {2:2, 9:3},
    5 : {1:2, 6:5},
    6 : {3:3, 5:5, 7:5, 8:7, 9:10},
    7 : {2:6, 3:4, 6:5, 8:3},
    8 : {2:7, 6:7, 7:3, 9:1},
    9 : {4:3, 6:10, 8:1}
}

def findRoot(UF, i):  
    pred = UF[i][0]
    if pred == -1:
        return i
    
    while UF[pred][0] != -1:
        UF[i][0] = UF[pred][0]  # decrease the depth of the tree
        i = pred
        pred = UF[pred][0]

    return pred    

def join(UF, i, j):  # (union find, two indexes)
    rootI = findRoot(UF,i)
    rootJ = findRoot(UF,j)

    if rootI==rootJ:
        return False
    
    if UF[rootI][1] > UF[rootJ][1]:
        UF[rootJ][0] = rootI
        UF[rootI][1] = UF[rootI][1] + UF[rootJ][1]   # joinnig smaller to bigger tree
    else:
        UF[rootI][0] = rootJ
        UF[rootJ][1] = UF[rootI][1] + UF[rootJ][1]     
    return True


def Kruskal(G):
    edges = []

    for v in G:
        for u,w in G[v].items():
            edges.append([u, v, w])

    edges.sort(key=lambda x:x[2])
 
    UF = {v: [-1, 1] for v in G}


    result = []

    for edge in edges:
        if join(UF,edge[0],edge[1]):
            result.append(edge)
            if len(result) == len(G)-1:
                break
    return result

def countTotalWeight(edges):
    return sum([e[2] for e in edges])

spanTree = Kruskal(G)
print(spanTree)
print(countTotalWeight(spanTree))


