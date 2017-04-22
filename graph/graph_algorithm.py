# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]

def compute_adjacencies(graph):
    adj = {}
    for i, j in graph:
        if i not in adj:
            adj[i] = []
        if j not in adj:
            adj[j] = []
        adj[i].append(j)
        adj[j].append(i)
    return adj

def terminated(i, adj):
    return adj[i]

def next_node(i, adj):
    j = adj[i].pop()
    adj[j].remove(i) # remove node i from adj
    return j
    
def find_eulerian_tour(graph):
    adjacencies = compute_adjacencies(graph)
    i = graph[0][0]
    path = [i]
    while adjacencies[i]:
        j = next_node(i, adjacencies)
        path.append(j)
        i = j
    return path

# print find_eulerian_tour([(1, 2), (2, 3), (3, 1)])

##################################################################
# Traversal...
# Call this routine on nodes being visited for the first time
def mark_component(G, node, marked, marker=1):
    marked[node] = marker
    total_marked = 1
    for neighbor in G[node]:
        if neighbor not in marked:
            total_marked += mark_component(G, neighbor, marked, marker)
    return total_marked

def check_connection(G, v1, v2):
    # partition G into regions with markers
    marked = {}
    marker = 0
    for v in G.keys():
        if v not in marked:
            mark_component(G, v, marked, marker)
            marker += 1
            print marked
    # cost for marked map: O(n)
    # cost for lookup v1, v2: O(1)
    return marked[v1] == marked[v2]
    
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def test_1():
    edges = [('a', 'g'), ('a', 'd'), ('g', 'c'), ('g', 'd'), 
             ('b', 'f'), ('f', 'e'), ('e', 'h')]
    G = {}
    for v1, v2 in edges:
        make_link(G, v1, v2)
    assert check_connection(G, "a", "c") == True
    assert check_connection(G, 'a', 'b') == False
    
# test_1()

def centrality_max(G, v):
    # your code here
    marked = {}
    distance_from_v = {v:0}
    list = [v]
    while list:
        w = list.pop(0)
        for nb in G[w]:
            if nb in marked:
                continue
            marked[nb] = True
            list.append(nb)
            distance_from_v[nb] = distance_from_v[w] + 1
    return max(distance_from_v.values())

#################
# Testing code
#
def make_link(G, node1, node2):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = 1
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = 1
    return G

def test():
    chain = ((1,2), (2,3), (3,4), (4,5), (5,6))
    G = {}
    for n1, n2 in chain:
        make_link(G, n1, n2)

    assert centrality_max(G, 1) == 5
    assert centrality_max(G, 3) == 3
    tree = ((1, 2), (1, 3),
            (2, 4), (2, 5),
            (3, 6), (3, 7),
            (4, 8), (4, 9),
            (6, 10), (6, 11))
    G = {}
    for n1, n2 in tree:
        make_link(G, n1, n2)
    assert centrality_max(G, 1) == 3
    assert centrality_max(G, 11) == 6

test()

