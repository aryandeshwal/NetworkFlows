import math
class Network:
    '''
        Class for defining a network with its parameters.
        Input - forward_star, s, t
        forward_star - stores the forward star representation of initial given network.
        res_adjList - stores the residual network in adjacency list at each stage of the algorithm
        inarc_adjList - stores the inarc list of the network
        nodes - no of nodes in the network
        edges - no of edges in the network
        adjMatrix - to keep track of edge capacities
    '''
    def __init__(self, forward_star, s, t):
        '''
            Initializes all the representations and parameters of the network
        '''
        self.source = s
        self.sink = t
        self.max_capacity = 0
        self.forward_star = forward_star
        self.res_adjList = {}  
        self.nodes = self._initialize_graph() # initialize adjlist and get a node count
        self.inarc_adjList = {}
        self.adjMatrix = [[[0, False] for i in range(self.nodes+1)] for j in range(self.nodes+1)]
        self._inarc_adjMatrix()
        self.edges = len(forward_star)
    def _initialize_graph(self):
        '''
            Creates the adjacency List from the given forward star representation
            returns - the number of nodes in the network
        '''
        N = 0 # variable to calculate no of nodes
        for i in range(len(self.forward_star)):
            tail, head, capacity = self.forward_star[i]
            if (capacity > self.max_capacity):
                self.max_capacity = capacity
            if (head > N): N = head
            if (tail > N): N = tail
            if tail in self.res_adjList:
                self.res_adjList[tail].append(list([head, capacity]))
            else:
                self.res_adjList[tail] = []
                self.res_adjList[tail].append(list([head, capacity]))
        return N
    def _inarc_adjMatrix(self):
        '''
            Creates the in-arc list and adjacency matrix from the given forward star representation
        '''        
        for i in range(len(self.forward_star)):
            tail, head, capacity = self.forward_star[i]
            self.adjMatrix[tail][head] = [capacity, True]
            if head in self.inarc_adjList:
                self.inarc_adjList[head].append(list([tail, capacity]))
            else:
                self.inarc_adjList[head] = []
                self.inarc_adjList[head].append(list([tail, capacity]))
    def exact_distance_label(self):
        '''
            Computes the exact distance labels by performing reverse BFS 
        '''
        d = [-1 for i in range(self.nodes + 1)]
        visited = [False for i in range(self.nodes + 1)] # list to keep track of marked nodes
        visited[self.sink] = True
        Queue = [self.sink]
        d[self.sink] = 0
        while len(Queue) > 0:
            top = Queue[0] # first element in the queue
            if top in self.inarc_adjList: # check if it has any inarcs at all
                for i in range(len(self.inarc_adjList[top])):
                    adjnode, capacity = self.inarc_adjList[top][i]
                    if (visited[adjnode] == False): # if adjacent node is not marked
                        visited[adjnode] = True
                        d[adjnode] = d[top] + 1
                        Queue.append(adjnode) # add it to the back of Queue
            Queue.remove(top) # Delete node already processed
        return d
    def push(self, i, j, delta):
        capacity = self.adjMatrix[i][j][0]
        self.res_adjList[i].remove([j, capacity])
        if (capacity - delta > 0):
            self.res_adjList[i].append([j, capacity-delta])
        if (j in self.res_adjList):
            if ([i, self.adjMatrix[j][i][0]] in self.res_adjList[j]): # if reverse edge is already there in the residual network
                self.res_adjList[j].remove([i, self.adjMatrix[j][i][0]])
        else:
            self.res_adjList[j] = []
        self.res_adjList[j].append([i, self.adjMatrix[j][i][0] + delta])
        self.adjMatrix[i][j][0] = self.adjMatrix[i][j][0] - delta # residual capacity
        self.adjMatrix[j][i][0] = self.adjMatrix[j][i][0] + delta
        
    def augment(self, pred):
        # Find delta (min capacity) of the path
        delta = math.inf
        i = self.sink
        while (i != self.source):
            capacity = self.adjMatrix[pred[i]][i][0]
            if (capacity < delta):
                delta = capacity
            i = pred[i]
        
        # Augment along the path with delta and update the residual network
        i = self.sink
        while (i != self.source):
            capacity = self.adjMatrix[pred[i]][i][0]
            self.res_adjList[pred[i]].remove([i, capacity])
            if (capacity - delta > 0):
                self.res_adjList[pred[i]].append([i, capacity - delta])
            if (i in self.res_adjList): 
                if ([pred[i], self.adjMatrix[i][pred[i]][0]] in self.res_adjList[i]): # if reverse edge is already there in the residual network
                    self.res_adjList[i].remove([pred[i], self.adjMatrix[i][pred[i]][0]])
            else:
                self.res_adjList[i] = []
            self.res_adjList[i].append([pred[i], self.adjMatrix[i][pred[i]][0] + delta])

            self.adjMatrix[pred[i]][i][0] = self.adjMatrix[pred[i]][i][0] - delta
            self.adjMatrix[i][pred[i]][0] = self.adjMatrix[i][pred[i]][0] + delta
            i = pred[i]
    def isPath(self, DELTA):
        visited = [False for i in range(self.nodes+1)] # list to keep track of marked nodes
        pred = [0 for i in range(self.nodes+1)] # initialization of pred vector
        # Mark Node s
        visited[self.source] = True 
        # Initialize next counter
        Queue = [self.source] # Queue to store nodes for expanding the graph in BFS way
                    # initialized with source node s
        while len(Queue) > 0: # while list is not empty
            fnode = Queue.pop(0) # first element in the queue
            if fnode in self.res_adjList: # check if it has any outarcs at all
                for i in range(len(self.res_adjList[fnode])):
                    head, capacity = self.res_adjList[fnode][i]
                    if (capacity >= DELTA and visited[head] == False): # if adjacent node is not marked
                        visited[head] = True
                        pred[head] = fnode
                        Queue.append(head) # add it to the back of Queue
        min_cap = math.inf
        if (pred[self.sink] != 0): # there is a path
            return (True, pred)
        else:
            return (False, pred)

