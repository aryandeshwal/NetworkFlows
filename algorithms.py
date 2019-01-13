import math
import numpy as np
def fifo_preflow(network):
    # Obtain the exact distance labels of the network
    n = network.nodes
    s = network.source
    t = network.sink
    d = network.exact_distance_label()
    no_satpushes = 0
    no_nonsatpushes = 0
    excess = [0 for i in range(n+1)]
    Queue = [] # FIFO queue to store active nodes
    # push all flow from source to adajcent edges
    for i in range(len(network.res_adjList[s])):
        head, capacity = network.res_adjList[s][i]
        excess[head] = capacity
        Queue.append(head)
    for i in range(len(Queue)):
        no_satpushes+=1
        network.push(s, Queue[i], network.adjMatrix[s][Queue[i]][0])
    if t in Queue:
        Queue.remove(t)# sink is not an active node
    d[s] = n

    while (len(Queue) > 0): # while there exists some active node
        top = Queue.pop(0) # push as much flow from current node until e[top] = 0 or top is relabelled
        while True:
            hasAdmissibleArc = False
            if (excess[top] == 0):
                break            

            if top in network.res_adjList:
                for i in range(len(network.res_adjList[top])):
                    head, capacity = network.res_adjList[top][i]
                    if (d[top] == d[head] + 1): # Admissible Arc
                        hasAdmissibleArc = True
                        delta = min(excess[top], capacity) 
                        if (delta == capacity):
                            no_satpushes += 1
                        else: 
                            no_nonsatpushes += 1
                        network.push(top, head, delta)
                        excess[top] -= delta
                        excess[head] += delta
                        if (head != t and head!= s and head not in Queue and excess[head] > 0):
                            Queue.append(head)
                        break
            else:
                print("Problem here 1!")
            if (hasAdmissibleArc == False): 
                break

        if (excess[top] > 0): # if node is still active, relabel and add to the Queue
            dmin = math.inf
            if top in network.res_adjList:
                for i in range(len(network.res_adjList[top])):
                    head, capacity = network.res_adjList[top][i]
                    if ((d[head] + 1) < dmin):
                        dmin = d[head] + 1
            else:
                print("Problem here 2!")
            d[top] = dmin
            Queue.append(top)

    max_flow = 0
    x_vector = []
    for i in range(len(network.forward_star)):
        tail, head, capacity = network.forward_star[i]
        flow_value = 0
        if (capacity >= network.adjMatrix[tail][head][0]):
            flow_value = capacity - network.adjMatrix[tail][head][0] # u_ij - r_ij
        x_vector.append(((tail, head), flow_value)) # edge (i,j) and final flow x(i,j) along the edge
        if (tail == s):
            max_flow =  max_flow + flow_value
        if (head == s): # have to consider incoming flow if the source has incoming edges
            max_flow = max_flow - flow_value
    return max_flow, x_vector, no_satpushes, no_nonsatpushes        


def shortest_augmenting_path(network):
    # Obtain the exact distance labels of the network
    n = network.nodes
    d = network.exact_distance_label()
    s = network.source
    t = network.sink
    i = s
    pred = [0 for i in range(n+1)]
    while d[s] < n:
        # if i has an admissible arc
        has_admissible_arc = False
        min_dj = math.inf
        if i in network.res_adjList:
            for j in range(len(network.res_adjList[i])):
                head, capacity = network.res_adjList[i][j]
                if (d[head] + 1 < min_dj):
                    min_dj = d[head] + 1
                if (d[i] == d[head]+1): # if admissible arc
                    has_admissible_arc = True
                    pred[head] = i 
                    i = head   # advance
                    if (i == t): 
                        network.augment(pred)
                        i = s
                    break
        if (has_admissible_arc == False):
            d[i] = min_dj
            if (i != s):
                i = pred[i]
    max_flow = 0
    x_vector = []
    for i in range(len(network.forward_star)):
        tail, head, capacity = network.forward_star[i]
        flow_value = 0
        if (capacity >= network.adjMatrix[tail][head][0]):
            flow_value = capacity - network.adjMatrix[tail][head][0] # u_ij - r_ij
        x_vector.append(((tail, head), flow_value)) # edge (i,j) and final flow x(i,j) along the edge
        if (tail == s):
            max_flow =  max_flow + flow_value
        if (head == s):
            max_flow = max_flow - flow_value

    return max_flow, x_vector    


def capacity_scaling(network):
    n = network.nodes
    d = network.exact_distance_label()
    s = network.source
    t = network.sink
    U = network.max_capacity            
    DELTA = int(2 ** (np.log(U)))
    while DELTA >= 1:
        hasDeltaPath, pred = network.isPath(DELTA)
        while hasDeltaPath:
            network.augment(pred)
            hasDeltaPath, pred = network.isPath(DELTA)
        DELTA = DELTA // 2
        

    max_flow = 0
    x_vector = []
    for i in range(len(network.forward_star)):
        tail, head, capacity = network.forward_star[i]
        flow_value = 0
        if (capacity >= network.adjMatrix[tail][head][0]):
            flow_value = capacity - network.adjMatrix[tail][head][0] # u_ij - r_ij
        x_vector.append(((tail, head), flow_value)) # edge (i,j) and final flow x(i,j) along the edge
        if (tail == s):
            max_flow =  max_flow + flow_value
        if (head == s):
            max_flow = max_flow - flow_value

    return max_flow, x_vector    

