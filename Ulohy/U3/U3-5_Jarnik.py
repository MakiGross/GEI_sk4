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


def Jarnik(G):
    #input data structures
    n = len(G)
    P = {v:-1 for v in G} # predecessors
    D = {v:float('inf') for v in G} # weights
    Pq = PriorityQueue() 

    #Starting node:
    Pq.put((0,next(iter(G))))
    D[next(iter(G))] = 0
    result = []

    #Until Pq is empty
    while not Pq.empty():

        # remove node with lowest 
        du,u = Pq.get()
        if du > D[u]:
            continue
        D[u] = float("-inf")
        # iterate through neigbours
        for v, wuv in G[u].items():
            # edge relaxation
            if D[v] > wuv:
                D[v] = wuv
                P[v] = u
                Pq.put((D[v], v))
    for u in P:
        if P[u] != -1:
            result.append([P[u],u,G[P[u]][u]])

    return result

def countTotalWeight(edges):
    return sum([e[2] for e in edges])

# calling the function
spanTree = Jarnik(G)
print(spanTree)
print(countTotalWeight(spanTree))

