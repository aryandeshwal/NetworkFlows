from Network import Network
from algorithms import fifo_preflow, shortest_augmenting_path, capacity_scaling
import time
import numpy as np
import networkx as nx
np.random.seed(42)


def exists_st_path(fs, s, t):
    '''
        Input
        -----
        fs : forward star representation of a network
        
        Output
        ------
        Boolean value(True or False) representing whether 
        there exists s-t path or not
    '''
    adjList = {}
    for edge in fs:
        tail = edge[0]
        head = edge[1]
        if tail in adjList:
            adjList[tail].append(head)
        else:
            adjList[tail] = []
            adjList[tail].append(head)
    # Run BFS and check whether the path exists
    visited = [False for i in range(t+1)] 
    pred = [-1 for i in range(t+1)] 
    visited[s] = True 
    Queue = [s] 
    while len(Queue) > 0: 
        top = Queue.pop(0) 
        if top in adjList:
            for i in range(len(adjList[top])):
                head = adjList[top][i]
                if (visited[head] == False): 
                    visited[head] = True
                    pred[head] = top
                    Queue.append(head) 
    if (pred[t] != -1 and pred[t] != 0): # there is a path and it is non-trivial
        return True
    else:
        return False


def gen_random_networks(n, m, U, num = 20):
    '''
        Input
        -----
        n : number of nodes in the network
        m : number of edges in the network
        U : maximum capacity of any arc in the network
        num : total number of networks to be generated (defaults to 20)
        
        Output
        ------
        'num' feasible non-trivial networks in forward-star representation
        feasible signify networks with s-t paths,
        non-trivial signifies networks where there is no direct s-t arc
    '''
    feasible_networks = []
    for i in range(num):
        fs_repr = []
        isNotFeasible = True
        while isNotFeasible:
            net = nx.gnm_random_graph(n, m, directed = True) # Use of networkx library method
            if (exists_st_path(net.edges, 0, n-1)):
                isNotFeasible = False
        for edge in net.edges:
            rc = np.random.randint(1, U) # generate random capacity of the edge between [1, U]
            fs_repr.append([edge[0] + 1, edge[1] + 1, rc]) # converting 1-based index for the algorithms
        #print(fs_repr)
        feasible_networks.append(fs_repr)
    return feasible_networks


# Generating data as a function of nodes
def get_nodes_data(num_nodes):
	preflow_time = []
	sap_time = []
	capscal_time = []
	for n in num_nodes:
	    network_set = gen_random_networks(n, 2*n, 20, num=50)
	    pftime = 0
	    stime = 0
	    ctime = 0
	    for fs in network_set:
	        fgraph = Network(fs, 1, n)
	        start_time = time.time()
	        v, x, ns, nns = fifo_preflow(fgraph)
	        pftime += (time.time() - start_time)
	        sgraph = Network(fs, 1, n)
	        sstart_time = time.time()
	        sv, sx = shortest_augmenting_path(sgraph)
	        stime += (time.time() - sstart_time)
	        cgraph = Network(fs, 1, n)
	        cstart_time = time.time()
	        cv, cx = capacity_scaling(cgraph)
	        ctime += (time.time() - cstart_time)
	    preflow_time.append(pftime/50)
	    sap_time.append(stime/50)
	    capscal_time.append(ctime/50)
	with open("no_data.txt", "a+") as f:
		print("preflow_time = ", end='', file =f)
		print(preflow_time, file = f)
		print("sap_time = ", end='', file =f)
		print(sap_time, file = f)
		print("capscal_time = ", end='', file =f)
		print(capscal_time, file = f)

num_nodes = [5, 8, 10, 12, 15, 20, 25, 50, 100, 150, 200, 400, 500]
#get_nodes_data(num_nodes)

# Generating data as a function of edges
def get_edge_data(n):
	preflow_time = []
	sap_time = []
	capscal_time = []
	for m in np.linspace(n, n*(n-1)//2, 10):
	    network_set = gen_random_networks(n, int(m), 100, num=50)
	    pftime = 0
	    stime = 0
	    ctime = 0
	    for fs in network_set:
	        fgraph = Network(fs, 1, n)
	        start_time = time.time()
	        v, x, ns, nns = fifo_preflow(fgraph)
	        pftime += (time.time() - start_time)
	        #print("Preflow maximum flow v: ", v)
	        sgraph = Network(fs, 1, n)
	        sstart_time = time.time()
	        sv, sx = shortest_augmenting_path(sgraph)
	        stime += (time.time() - sstart_time)
	        #print("SAP maximum flow v: ", sv)
	        cgraph = Network(fs, 1, n)
	        cstart_time = time.time()
	        cv, cx = capacity_scaling(cgraph)
	        ctime += (time.time() - cstart_time)
	        #print("Capacity Scaling maximum flow v: ", cv)
	    preflow_time.append(pftime/50)
	    sap_time.append(stime/50)
	    capscal_time.append(ctime/50)
	with open("no_data.txt", "a+") as f:
		print("preflow_edge_time", end = '=', file =f)
		print(preflow_time, file = f)
		print("sap_edge_time", end = '=', file =f)
		print(sap_time, file = f)
		print("cap_edge_time", end = '=', file =f)
		print(capscal_time, file = f)
#get_edge_data(n=20)


# Generating data as a function of maximum capacity
def get_cap_data():
	preflow_time = []
	sap_time = []
	capscal_time = []
	n = 400
	m = n*(n-1)//2
	for U in [10, 100, 1000, 10000, 100000, 1000000]:
	    network_set = gen_random_networks(n, int(m), U, num=50)
	    pftime = 0
	    stime = 0
	    ctime = 0
	    for fs in network_set:
	        i = np.random.randint(0, len(fs))
	        fs[i][2] = U
	        fgraph = Network(fs, 1, n)
	        start_time = time.time()
	        v, x, ns, nns = fifo_preflow(fgraph)
	        pftime += (time.time() - start_time)
	        sgraph = Network(fs, 1, n)
	        sstart_time = time.time()
	        sv, sx = shortest_augmenting_path(sgraph)
	        stime += (time.time() - sstart_time)
	        cgraph = Network(fs, 1, n)
	        cstart_time = time.time()
	        cv, cx = capacity_scaling(cgraph)
	        ctime += (time.time() - cstart_time)
	    preflow_time.append(pftime/50)
	    sap_time.append(stime/50)
	    capscal_time.append(ctime/50)
	with open("no_data.txt", "a+") as f:
		print("preflow_cap_time", end = '=', file =f)
		print(preflow_time, file = f)
		print("sap_cap_time", end = '=', file =f)
		print(sap_time, file = f)
		print("cap_cap_time", end = '=', file =f)
		print(capscal_time, file = f)
#get_cap_data()