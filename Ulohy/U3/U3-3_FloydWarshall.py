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


def FloydWarshall(Graph):
    #output matrix 
    dist = {v: {w:float("inf") for w in Graph} for v in Graph}
    # matrix of 'predecessors'
    pred = {v: {w: -1 for w in Graph} for v in Graph}
    # output matrix made from graph
    for v in Graph:
        dist[v][v] = 0
        for w, weight in Graph[v].items():
            dist[v][w] = weight


    for k in Graph:
        # matrix for every k
        dist2 = {v: {w:float("inf") for w in Graph} for v in Graph}
        for i in Graph:
            for j in Graph:

                if dist[i][k] + dist[k][j] < dist[i][j]:
                    pred[i][j] = k
                
                dist2[i][j] = min(dist[i][j],  # if the vertex is not on the path, stays inf
                                 dist[i][k] + dist[k][j]  # if the vertex is on the path the distance is added
                                 )
        dist = dist2        

    return dist, pred      


def PrintPathHelper(start, end, PredMatrix):
    k = PredMatrix[start][end]
    if k == -1:
        print(end)
    else:
        PrintPathHelper(start, k, PredMatrix)
        PrintPathHelper(k, end, PredMatrix)

def PrintPath(start, end, PredMatrix):
    print(start)
    PrintPathHelper(start, end, PredMatrix)


dist, pred = FloydWarshall(G)
PrintPath(1,9,pred)

