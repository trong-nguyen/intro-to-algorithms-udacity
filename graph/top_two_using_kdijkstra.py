#
# write a function, `top_two` that takes in a graph and a starting
# node and returns two paths, the first and second shortest paths,
# for all the other nodes in the graph.  You can assume that the 
# graph is connected.
#
import heapq

# path that acts like list but allow quick lookup
class OrderedPath(object):
    def __init__(self, a, s=None):
        self.container = list(a)
        self.lookup = set(a) if not s else s.copy()

    def __eq__(self, another):
        if isinstance(another, list):
            return self.container == another
        elif isinstance(another, OrderedPath):
            return self.container == another.container
        
        raise 'Invalid comparison of {} and {}'.format(self, another)

    def __add__(self, l):
        added = OrderedPath(self.container, self.lookup)
        added.container.extend(l)
        added.lookup.union(l)
        return added

    def __contains__(self, i):
        return i in self.lookup

    def __getitem__(self, idx):
        return self.container[idx]

    def __repr__(self):
        return str(self.container)

# This is actually dijkstra using heap
def dijkstra_heap(graph, start, end, k):
    shortest_path = []
    opath = OrderedPath([start]) 
    # print opath.container, opath.lookup

    # opath = [start]
    heap = [(0, opath)]
    while heap and len(shortest_path) < k:
        cost, path = smallest = heapq.heappop(heap)
        tail = path[-1]
        # found a path that connects start and end
        if tail == end:
            shortest_path.append(smallest)
            # no need to branch from this, since it would come back to end and hence creates loops
            continue

        for nb, weight in graph[tail].items():
            # this prevents going back to one of the included node in path, i.e. prevents loops
            if nb in path:
                continue
            heapq.heappush(heap, (cost + weight, path + [nb]))
            # print start, end, nb, path, weight, nb in path
    return shortest_path

def top_two(graph, start):
    shortest = {}
    for node in graph:
        if node == start:
            continue

        shortest[node] = dijkstra_heap(graph, start, node, 2)

    return shortest

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
