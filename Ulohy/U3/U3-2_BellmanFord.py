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

def BellmanFord(Graph, start):
    dist = {vertex: float('inf') for vertex in Graph}  # initialize distances
    dist[start] = 0  # dist on start is 0
    state = {vertex: False for vertex in Graph}  
    state[start] = True
    pred = {vertex: float(-1) for vertex in Graph} # predecessors 
    que = Queue()
    que.put(start)

    while not que.empty():
        v = que.get()  
        for w, weight in Graph[v].items():
            if dist[w] > dist[v] + weight:
                dist[w] = dist[v] + weight
                if state[w] == False:
                    que.put(w)
                state[w] == True
                pred[w] = v
        state[v] = False
    return dist, pred

# Path recreation
def rec(u, v, P):
    path = []  # path that will be reconstructed

    while   v!=u and v!=-1 :  # path shortening
        path.append(v)
        v = P[v]
    path.append(v) 

    if v != u:
        print('path does not exist')
    else: 
        print(path)
    return path

start = 1
end = 9
dist, pred = BellmanFord(G,1)
path = rec(start, end, pred)