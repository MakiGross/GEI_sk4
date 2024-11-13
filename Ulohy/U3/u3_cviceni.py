from math import *;
from queue import *;
#Graph G definiton

#Graph G definiton

G = {
   1:[2, 3, 5],
   2:[1, 3, 4, 7, 8],
   3:[1, 2, 6, 7] ,
   4:[2, 9],
   5:[1, 6],
   6:[3, 5, 7, 9],
   7:[2, 3, 6, 8],
   8:[2, 6, 7, 9],
   9:[4, 6, 8]
}

#Coordinates definition for graphic representation


# BFS
def BFS(G,u):
    n = len(G)      # count of nodes
    P = [-1]*(n+1)  #list of predecessors (doesn't have predecessors yet = -1)
    S = [0]*(n+1)   #if visited (status) 0-not visited 1-open 2-closed =now every is 0
    Q = []          # query - now empty

    # starting node change status
    S[u] = 1     # state of index u is now 1 - open
    Q.append(u)  # added first node to the quevue

    while Q:    	   #until Q is empty:
        u = Q.pop(0)   # we are getting the first element in quevue


        for v in G[u]:       # visit all the neighbours v
            if S[v] == 0:    # If the neighbor is unvisited...
                S[v] = 1     # ...mark as "open"
                P[v] = u     # ..set the predecessor
                Q.append(v)  # ...enqueue the neighbor  

        S[u] = 2       # the first node can be now closed

    return P

P = BFS(G, 2)
print('Predecessors by BFS:')
print(P)


def rec(u, v, G):
    path = []  # path that will be reconstructed

    while   v!=u and v!=-1 :  # path shortening
        path.append(v)
        v = P[v]
    path.append(v) 

    if v== u:
        print('path does not exist')
    else: 
        print('all good')

    return path

path = rec(10, 5, P)
print('Path by BFS:')
print(path)
#_____________________________________________________________

def DFS(G,u):
    n = len(G)      # count of nodes
    P = [-1]*(n+1)  #list of predecessors (doesn't have predecessors yet = -1)
    S = [0]*(n+1)   #if visited (status) 0-not visited 1-open 2-closed =now every is 0
    St = []          # stack - now empty

    # starting node change status
    S[u] = 1     # state of index u is now 1 - open
    St.append(u)  # added first node to the quevue

    while St:    	   #until Q is empty:
        u = St.pop()   # we are getting the first element in quevue
        S[u] = 1

        for v in reversed(G[u]):       # visit all the neighbours v
            if S[v] == 0:    # If the neighbor is unvisited...
                S[v] = 1     # ...mark as "open"
                P[v] = u     # ..set the predecessor
                St.append(v)  # ...enqueue the neighbor  

        S[u] = 2       # the first node can be now closed

    return P

P = DFS(G, 2)
print('predecessors by DFS:')
print(P)


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

path = rec(9, 5, P)
print('Path by DFS:')
print(path)




## Djikstra algorithm

def djikstra(G, u, v):
    n = len(G)
    P  = [-1]*(n+1) # predecessors
    D = [inf]*(n+1) # weights
    Pq = PriorityQueue() # priority queue

    #Starting node:
    Pq.put((0,u))
    D[u] = 0

    #Until Pq is empty
    while not Pq.empty():

        # remove node with lowest 
        du, u = Pq.get()
        # iterate through neigbours
        for v, wuv in G[u].items():
            # edge relaxation
            if D[v] > D[u] + wuv:
                D[v] = D[u] + wuv
                P[v] = u
                Pq.put((D[v], v))

    return P, D[v]

start = 1
end = 5
# calling the function
P, dmin = djikstra(G, start, end)
# recontruction path
path = rec(1,5,P)

print('Djikstra algorithm path')
print(path, dmin)


    
