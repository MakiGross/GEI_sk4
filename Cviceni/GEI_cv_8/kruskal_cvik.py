from math import *;
from queue import *;

## Kruskal
#Graph definition
V = [1, 2, 3, 4, 5, 6, 7, 8, 9]

E = [
    [1, 2, 8], 
    [1, 3, 4], 
    [1, 5, 2], 
    [2, 1, 8], 
    [2, 3, 5], 
    [2, 4, 2], 
    [2, 7, 6], 
    [2, 8, 7], 
    [3, 1, 4],  
    [3, 2, 5], 
    [3, 6, 3], 
    [3, 7, 4], 
    [4, 2, 2], 
    [4, 9, 3], 
    [5, 1, 2], 
    [5, 6, 5], 
    [6, 3, 3], 
    [6, 5, 5], 
    [6, 7, 5], 
    [6, 8, 7], 
    [6, 9, 10], 
    [7, 2, 6], 
    [7, 3, 4], 
    [7, 6, 5], 
    [7, 8, 3], 
    [8, 2, 7], 
    [8, 6, 7], 
    [8, 7, 3], 
    [8, 9, 1], 
    [9, 4, 3], 
    [9, 6, 10], 
    [9, 8, 1]
    ]

#Node coordinates X, Y
C = {
    1 : [95, 322],
    2 : [272, 331],
    3 : [173, 298],
    4 : [361, 299],
    5 : [82, 242],
    6 : [163, 211],
    7 : [244, 234],
    8 : [333, 225],
    9 : [412, 196]
}


# function find parent
def find(u,P):
    # find parent for u
    while P[u] != u:
        u = P[u]
    return u

# function Union
def union(u, v, P):
    root_u = find(u,P)
    root_v = find(v,P)
    if root_u != root_v:
        P[root_v] = root_u


def makeSet(u, P):
    # init trees
    P[u] = u

def min_span_Tree(U, V):
    T = []  # tree
    wt = 0  # line weight
    n = len(V)  # count of points
    P = [-1]*(n+10)  # predecessors

    for v in V:
        print(v)
        makeSet(v, P)

    # sort edges
    ES = sorted(E, key=lambda it:it[2])

    # process sorted edges
    for e in ES:
        u, v, w = e
        
        # relaxation of edge - union find
        if find(u,P) != find(v,P):
            union(u, V, P)
            T.append(e)
            wt = wt + w

    return T, wt

T,wt = min_span_Tree(E,V)
print(T)

