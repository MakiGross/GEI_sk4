from math import *;
from queue import *;

# graph definition
G = {
    1 : {2:8, 3:4, 5:2},
    2 : {1:8, 3:5, 4:2, 7:6, 8:7},
    3 : {1:4, 2:5, 6:3, 7:4},
    4 : {2:2, 9:3},
    5 : {1:2, 6:5},
    6 : {3:3, 5:5, 7:5, 8:7, 9:10},
    7 : {2:6, 3:4, 6:5, 8:3},
    8 : {2:7, 6:7, 7:3, 9:1},
    9 : {4:3, 6:10, 8:1}
}


def dijkstra(G, u, v):
    #input data structures
    n = len(G)
    P = [-1]*(n+1) # predecessors
    D = [inf]*(n+1) # weights
    Pq = PriorityQueue() 

    #Starting node:
    Pq.put((0,u))
    D[u] = 0

    #Until Pq is empty
    while not Pq.empty():

        # remove node with lowest 
        du,u = Pq.get()
        # iterate through neigbours
        for v, wuv in G[u].items():
            # edge relaxation
            if D[v] > D[u] + wuv:
                D[v] = D[u] + wuv
                P[v] = u
                Pq.put((D[v], v))

    return P, D[v]

# Path recreation
def rec(u, v, G):
    path = []  # path that will be reconstructed

    while   v!=u and v!=-1 :  # path shortening
        path.append(v)
        v = P[v]
    path.append(v) 

    if v != u:
        print('path does not exist')
    else: 
        print('all good')
    return path

start = 1
end = 9
# calling the function
P, dmin = dijkstra(G, start, end)
# recontruction path
path = rec(start,end,P)

print('Djikstra algorithm path')
print(path, dmin)

