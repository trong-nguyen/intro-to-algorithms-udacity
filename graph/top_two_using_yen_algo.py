#
# write a function, `top_two` that takes in a graph and a starting
# node and returns two paths, the first and second shortest paths,
# for all the other nodes in the graph.  You can assume that the 
# graph is connected.
#
import heapq

from dijkstra import dijkstra as core_dijkstra
from dijkstra import OrientedDistUnit as dunit

# modified to be able to store ids and values in heap.

def all_shortest_path(graph, origin, dist):
    spath = {}
    queue = [origin]
    while queue:
        v = queue.pop()
        for u in graph[v]:
            if u in spath:
                continue
            spath[u] = dunit.shortest_path(dist, origin=origin, destination=u)
            queue.insert(0, u)
            # print u, spath[u]
    return spath

def dijkstra(G, removed_edge=None, *args, **kwarg):
    if not removed_edge:
        return core_dijkstra(G, dunit=dunit, *args, **kwarg)

    # wrapper
    v1, v2 = removed_edge
    tmp = G[v1][v2]
    del G[v1][v2]
    del G[v2][v1] # undirected
    result = core_dijkstra(G, dunit=dunit, *args, **kwarg)
    G[v1][v2] = G[v2][v1] = tmp
    return result

def make_edges(vertices):
    return list(zip(vertices[:-1], vertices[1:]))

def compute_path_cost(path, graph):
    edges = make_edges(path)
    return sum([graph[a][b] for a, b in edges])

def yen_shortest(graph, dist, shortest_path, origin, destination, second_shortest_lookup=None):
    def update_lookup(table, start, end, value):
        print 'Updating [{}-{}] route, value{}'.format(start, end, value)
        table[start] = table.get(start, {})
        table[start][end] = value
        table[end] = table.get(end, {})
        table[end][start] = value #undirected

    def lookup_has(v1, v2, table):
        return table and v1 in table and v2 in table[v1]

    def retrieve_lookup(table, v1, v2):
        print 'Reusing [{}-{}] route'.format(v1, v2)
        return table[v1][v2] # v1, v2 order doesnot matter since we updated both



    '''
    1st step:
        find A1, already found in dist

    2nd step: build container B which contains all the deviated path from A1
        for edge in shortest_path
            temporarily remove edge
            find shortest from left vertex to destination
            compute cost for this path
            assemble (cost, path) and store it in a container
    '''

    B_container = []
    sp = shortest_path[destination]
    for idx, (v1, v2) in enumerate(make_edges(sp)):
        root_path = sp[:idx+1]
        root_cost = compute_path_cost(root_path, graph)

        if second_shortest_lookup is not None and lookup_has(v1, destination, second_shortest_lookup):
            spur_cost, spur_path = retrieve_lookup(second_shortest_lookup, v1, destination)
        else:
            removed_edge = (v1, v2)
            v1_dist, _ = dijkstra(graph, removed_edge, origin=v1, target=destination)
            spur_path = dunit.shortest_path(v1_dist, origin=v1, destination=destination)
            spur_cost = dunit.weight(v1_dist[destination]) if spur_path else float('inf')
            
            # update if required
            if second_shortest_lookup is not None:
                value = (spur_cost, spur_path)
                update_lookup(second_shortest_lookup, v1, destination, value)
        
        if not spur_path:
            continue

        # assemble
        heapq.heappush(B_container, (root_cost + spur_cost, root_path + spur_path[1:]))

    if not B_container:
        return None

    return heapq.heappop(B_container)

def core_top_two(graph, start, end, shortest_dist, fslookup, sslookup=None):
    # your code here
    #
    # the result should be a dictionary, containing a mapping between
    # every node in the graph, except the start node, to a list.  The
    # list should contain two elements.  Each element should contain a
    # cost to get to that node and the path followed.  See the `test`
    # function for an example
    #
    shortest_path = fslookup[end]

    shortest = (compute_path_cost(shortest_path, graph), shortest_path)
    second_shortest = yen_shortest(graph, shortest_dist, shortest_path=fslookup, origin=start, destination=end, second_shortest_lookup=sslookup)

    return [shortest, second_shortest] if second_shortest else [shortest]

def top_two(graph, start):
    sslookup = {}
    top = {}

    dist, _ = dijkstra(graph, origin=start)
    fslookup = all_shortest_path(graph, start, dist)

    for end in graph:
        if end == start:
            continue

        top[end] = core_top_two(graph, start, end, dist, fslookup, sslookup)
    return top

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    graph = {'a':{'b':3, 'c':4, 'd':8},
             'b':{'a':3, 'c':1, 'd':2},
             'c':{'a':4, 'b':1, 'd':2},
             'd':{'a':8, 'b':2, 'c':2}}

    # result = {'b': top_two(graph, 'a', 'b')}
    # print result


    result = top_two(graph, 'a') # this is a dictionary
    print result

    b = result['b'] # this is a list
    b_first = b[0] # this is a list
    assert b_first[0] == 3 # the cost to get to 'b'
    assert b_first[1] == ['a', 'b'] # the path to 'b'
    b_second = b[1] # this is a list
    assert b_second[0] == 5 # the cost to get to 'b'
    assert b_second[1] == ['a', 'c', 'b']

    edges = [
        ('a', 'b', 3),
        ('a', 'c', 4),
        ('a', 'd', 8),
        ('b', 'd', 2),
        ('c', 'd', 2),
        ('c', 'f', 3),
        ('b', 'e', 5),
        ('d', 'e', 3),
        ('e', 'f', 6)
    ]
    graph = {}
    for n1, n2, w in edges:
        make_link(graph, n1, n2, w)

    print top_two(graph, 'a')
test()
