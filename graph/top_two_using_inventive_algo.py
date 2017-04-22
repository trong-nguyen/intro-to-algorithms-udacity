#
# write a function, `top_two` that takes in a graph and a starting
# node and returns two paths, the first and second shortest paths,
# for all the other nodes in the graph.  You can assume that the 
# graph is connected.
#

import json
# from find_a_favor import dijkstra_heap, retrieve_shortest_path
import copy

# from heap import *
from operator import itemgetter
import math

# modified to be able to store ids and values in heap.

# Heap shortcuts
def left(i): return i*2+1
def right(i): return i*2+2
def parent(i): return (i-1)/2
def root(i): return i==0
def leaf(L, i): return right(i) >= len(L) and left(i) >= len(L)
def one_child(L, i): return right(i) == len(L)
def val_(pair): return pair[0]

def swap(heap, old, new, location):
    location[heap[old]] = new
    location[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])

# Call this routine if the heap rooted at i satisfies the heap property
# *except* perhaps i to its children immediate children
#
#
# location is a dictionary mapping an object to its location
# in the heap
def down_heapify(heap, i, location):
    # If i is a leaf, heap property holds
    while True:
        l = left(i)
        r = right(i)

        # see if we don't have any children
        if l >= len(heap): 
            break

        v = heap[i][0]
        lv = heap[l][0]

        # If i has one child...                 
        if r == len(heap):
            # check heap property
            if v > lv:
                # If it fails, swap, fixing i and its child (a leaf)
                swap(heap, i, l, location)
            break

        rv = heap[r][0]
        # If i has two children...
        # check heap property
        if min(lv, rv) >= v: 
            break
        # If it fails, see which child is the smaller
        # and swap i's value into that child
        # Afterwards, recurse into that child, which might violate
        if lv < rv:
            # Swap into left child
            swap(heap, i, l, location)
            i = l
        else:
            # swap into right child
            swap(heap, i, r, location)
            i = r

# Call this routine if whole heap satisfies the heap property
# *except* perhaps i to its parent
def up_heapify(heap, i, location):
    # If i is root, all is well
    while i > 0: 
        # check heap property
        p = (i - 1) / 2
        if heap[i][0] < heap[p][0]:
            swap(heap, i, p, location)
            i = p
        else:
            break

# put a pair in the heap
def insert_heap(heap, v, location):
    heap.append(v)
    location[v] = len(heap) - 1
    up_heapify(heap, len(heap) - 1, location)

# build_heap
def build_heap(heap):
    location = dict([(n, i) for i, n in enumerate(heap)])
    for i in range(len(heap)-1, -1, -1):
        down_heapify(heap, i, location)
    return location

# remove min
def heappopmin(heap, location):
    # small = heap[0]
    val = heap[0]
    new_top = heap.pop()
    del location[val]
    if len(heap) == 0:
        return val
    location[new_top] = 0
    heap[0] = new_top
    down_heapify(heap, 0, location)
    return val

def decrease_val(heap, location, old_val, new_val):
    i = location[old_val]
    heap[i] = new_val
    # is this the best way?
    del location[old_val]
    location[new_val] = i
    up_heapify(heap, i, location)


def _test_location(heap, location):
    for n, i in location.items():
        assert heap[i] == n

def _test_heap():
    h = [(1, 'a'), (4, 'b'), (6, 'c'), (8, 'd'), 
         (9, 'e'), (1, 'f'), (4, 'g'), (5, 'h'),
         (7, 'i'), (8, 'j')]
    location = build_heap(h)
    _test_location(h, location)
    old_min = (-float('inf'), None)
    while len(h) > 0:
        new_min = remove_min_heap(h, location)
        _test_location(h, location)
        assert val_(old_min) <= val_(new_min)
        old_min = new_min    

def _test_add_and_modify():
    h = [(1, 'a'), (4, 'b'), (6, 'c'), (8, 'd'), 
         (9, 'e'), (1, 'f'), (4, 'g'), (5, 'h'),
         (7, 'i'), (8, 'j')]
    location = build_heap(h)
    insert_heap(h, (-1, 'k'), location)
    assert (-1, 'k') == remove_min_heap(h, location)
    decrease_val(h, location, (6, 'c'), (-1, 'c'))
    assert (-1, 'c') == remove_min_heap(h, location)
    _test_location(h, location)

def get_parent(d):
    try:
        return d[-1]
    except:
        print d
        raise

def retrieve_shortest_path(dist, destination, origin):
    node = destination
    path = [node]
    while node != origin and node != None:
        node = get_parent(dist[node])
        path.insert(0, node)

    return path

def maximize_probability_of_favor(G, v1, v2):
    # logarithm is monotonic: x ~ log(x) hence 
    # maximize(x1*x2*...) = maximize(logx1+logx2+..)
    # and = minimize(-logx1-logx2...)
    logG = {
        k: {
            kk:-math.log(vv) for kk,vv in v.items()
        }
        for k,v in G.iteritems()
    }

    # your code here
    # call either the heap or list version of dijkstra
    # and return the path from `v1` to `v2` 
    # along with the probability that v1 will do a favor 
    # for v2
    m = 1.*sum([len(v) for v in G.values()])
    n = 1.*len(G)
    mlogn = m*math.log(n)
    n2 = n*n
    text = 'dijkstras with m={}, n={}, mlogn={}, n**2={}'.format(m, n, mlogn, n2)

    if mlogn < n2:
        print 'Using heap', text 
        final_dist = dijkstra_heap(logG, v1)
    else:
        print 'Using list', text
        final_dist = dijkstra_list(logG, v1)

    path = retrieve_shortest_path(final_dist, v2, v1)
    print path

    edges = [logG[n1][n2] for n1, n2 in zip(path[:-1], path[1:])]
    log_prob = sum(edges)
    prob = math.e ** (-log_prob)
    return path, prob

#
# version of dijkstra implemented using a heap
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_heap(G, a):
    # Distance to the input node is zero, and it has
    # no parent
    first_entry = (0, a, None)
    heap = [first_entry]
    # location keeps track of items in the heap
    # so that we can update their value later
    location = {first_entry:0}
    dist_so_far = {a:first_entry} 
    final_dist = {}
    while len(dist_so_far) > 0:
        dist, node, parent = heappopmin(heap, location)
        # lock it down!
        final_dist[node] = (dist, parent)
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, x, node)
            if x not in dist_so_far:
                # add to the heap
                insert_heap(heap, new_entry, location)
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                # update heap
                decrease_val(heap, location, dist_so_far[x], new_entry)
                dist_so_far[x] = new_entry
    return final_dist

#
# version of dijkstra implemented using a list
#
# returns a dictionary mapping a node to the distance
# to that node and the parent
#
# Do not modify this code
#
def dijkstra_list(G, a):
    dist_so_far = {a:(0, None)} #keep track of the parent node
    final_dist = {}
    while len(final_dist) < len(G):
        node, entry = min(dist_so_far.items(), key=itemgetter(1))
        # lock it down!
        final_dist[node] = entry
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist, node)
            if x not in dist_so_far:
                dist_so_far[x] = new_entry
            elif new_entry < dist_so_far[x]:
                dist_so_far[x] = new_entry
    return final_dist

def get_dist_value(d):
    return d[0]

def select(v, v0, graph, dist, top, shortest_path):
    cpath = copy.deepcopy(top[v0])
    # assert not(cpath is top[v0]), 'Wrong'
    for u in graph[v]:
        # if u == v0:
        #     continue
        if v in shortest_path[u]:
            continue
        # print shortest_path[u]

        s_uv = graph[u][v]
        s_v0v = graph[v0][v]
        s_u = get_dist_value(dist[u])
        path_value = 1.0*s_u + s_uv
        relative_path_value = path_value - s_v0v

        # compare this path_value to those of top of the previous node v0
        cpath += [[relative_path_value, path_value] + [list(shortest_path[u])]]
        cpath = sorted(cpath)
        # if len(cpath) > 3:
        #     cpath.pop() #maintain

        print 'from {} to {}, via {}'.format(v0, v, u), cpath
    for p in cpath:
        p[-1] += [v]
    return cpath

def all_shortest_path(graph, origin, dist):
    spath = {}
    queue = [origin]
    while queue:
        v = queue.pop()
        for u in graph[v]:
            if u in spath:
                continue
            spath[u] = retrieve_shortest_path(dist, origin=origin, destination=u)
            queue.insert(0, u)
            # print u, spath[u]
    return spath





def top_two(graph, start):
    ''' run a dijkstra to find shortest distance to all nodes from origin
    maintain a second_shortest list
    second_shortest = SS(nb_i) = shortest distance from a to b that travel through nb_i
    where nb_i is the neighbor of one of the nodes that form the shortest path
    for all nodes vi on the shortest path
        for all neighbors of vi
            compute the distance of the ab path that travels through nb_i
            put this in the list

    second shortest distance = min of this list interms of distance
    third shortest distance = second min of this list
    #
    # compute Ci value, the distance
    '''


    # the result should be a dictionary, containing a mapping between
    # every node in the graph, except the start node, to a list.  The
    # list should contain two elements.  Each element should contain a
    # cost to get to that node and the path followed.  See the `test`
    # function for an example
    #

    shortest_dist = dijkstra_heap(graph, start)
    shortest_path = all_shortest_path(graph, origin=start, dist=shortest_dist)

    top = {start: []}
    queue = [start]
    while queue:
        v0 = queue.pop()
        for v in graph[v0]:
            if v in top:
                continue
            top[v] = select(v, v0, graph, shortest_dist, top, shortest_path)
            queue.insert(0, v)
            print v0, v, top

    def conform(p):
        return [p[1], p[-1], p[0]]

    for k, v in top.iteritems():
        top[k] = [conform(vi) for vi in v]

    return top

def test():
    graph = {'a':{'b':3, 'c':4, 'd':8},
             'b':{'a':3, 'c':1, 'd':2},
             'c':{'a':4, 'b':1, 'd':2},
             'd':{'a':8, 'b':2, 'c':2}}
    result = top_two(graph, 'a') # this is a dictionary
    print json.dumps(result, indent=4)
    print result
    b = result['b'] # this is a list
    b_first = b[0] # this is a list
    assert b_first[0] == 3 # the cost to get to 'b'
    assert b_first[1] == ['a', 'b'] # the path to 'b'
    b_second = b[1] # this is a list
    assert b_second[0] == 5 # the cost to get to 'b'
    assert b_second[1] == ['a', 'c', 'b']


test()
