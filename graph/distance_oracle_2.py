#  
# This is the same problem as "Distance Oracle I" except that instead of
# only having to deal with binary trees, the assignment asks you to
# create labels for all tree graphs.
#
# In the shortest-path oracle described in Andrew Goldberg's
# interview, each node has a label, which is a list of some other
# nodes in the network and their distance to these nodes.  These lists
# have the property that
#
#  (1) for any pair of nodes (x,y) in the network, their lists will
#  have at least one node z in common
#
#  (2) the shortest path from x to y will go through z.
# 
# Given a graph G that is a tree, preprocess the graph to
# create such labels for each node.  Note that the size of the list in
# each label should not be larger than log n for a graph of size n.
#

#
# create_labels takes in a tree and returns a dictionary, mapping each
# node to its label
#
# a label is a dictionary mapping another node and the distance to
# that node
#
from operator import add

def min_dist(dist):
    return min([(v,k) for k, v in dist.iteritems()])[1]

# Dijkstra algorithm
# Advance features:
# - Custom accumulate rule (max of 2, product of 2, sum of 2
# - Dynamic lookup / reusable results from prior search
def dijkstra(G, v, target=None, accumulate_rule=add, dynamic_lookup={}, verbose=False):
    if target:
        success_string = '{}-{} pair found in lookup'.format(v, target)
        if v in dynamic_lookup and target in dynamic_lookup[v]:
            if verbose: print success_string
            return dynamic_lookup[v], dynamic_lookup[v][target]
        elif target in dynamic_lookup and v in dynamic_lookup[target]:
            if verbose: print success_string
            return dynamic_lookup[target], dynamic_lookup[target][v]

    if v in dynamic_lookup:
        final_dist = dynamic_lookup[v]

        # shortest distance search has been found for all nodes
        if len(final_dist) == len(G):
            return final_dist

        dist_so_far = None
        for w in final_dist:
            for u in G[w]:
                if u not in final_dist:
                    dist_so_far = {u: final_dist[w] + G[w][u]}
                    break
            if dist_so_far:
                break
        assert dist_so_far, 'Something wrong with dynamic_lookup logic, no dist found outside of final_dist'
    else:
        final_dist = dynamic_lookup[v] = {}
        dist_so_far = {v:0.}

    while len(final_dist) < len(G):
        try:
            w = min_dist(dist_so_far)
        except:
            import json
            print 'final len {}, G len {}'.format(len(final_dist), len(G))
            print 'G', json.dumps(G, indent=2)
            print 'final_dist', json.dumps(final_dist, indent=2)
            print 'dist_so_far', json.dumps(dist_so_far, indent=2)
            raise

        final_dist[w] = dist_so_far[w]
        if target == w:
            return final_dist, final_dist[target]
        del dist_so_far[w]
        for u in G[w]:
            if u in final_dist:
                continue
            s = accumulate_rule(final_dist[w], G[w][u]) # dist from w to this neighbor
            if u not in dist_so_far:
                dist_so_far[u] = s
            else:
                dist_so_far[u] = min(dist_so_far[u], s)

    return final_dist, None

def bfs_depth(G, v):
    stack = [v]
    depth = {v: 0}
    explored = {v: True}
    while stack:
        v = stack.pop()
        for u in G[v]:
            if u in explored:
                continue
            depth[u] = depth[v] + 1
            explored[u] = True
            stack.insert(0, u)
    return depth


def find_tree_root(G):
    def mid_key(d):
        return G.keys()[len(G) / 2]
    def max_value_key(d):
        assert d, 'cannot find max value key of empty dict'
        return max([v,k] for k,v in d.iteritems())[1]
    # find middle point between two furthest nodes (hops)
    # start from random node v, find furthest node x
    # start from node x, find furthest node y
    # root = middle(x, y)
    assert G
    v = mid_key(G)
    depth_from_v = bfs_depth(G, v)
    x = max_value_key(depth_from_v)
    depth_from_x = bfs_depth(G, x)
    y = max_value_key(depth_from_x)
    y_value = depth_from_x[y]
    mid_value = y_value / 2

    for k,v in depth_from_x.iteritems():
        if v == mid_value:
            root = k
            break

    return root, depth_from_x

# from dijkstra import dijkstra

def create_subtree(G, root, parent):
    # create subtree branching from root, except parent branch
    stack = [root]
    subtree = {}
    while stack:
        v = stack.pop()
        if v == root:
            subtree[v] = {x:y for x,y in G[v].iteritems() if x != parent}
        else:
            subtree[v] = G[v]

        for u in G[v]:
            if u in subtree or u == parent:
                continue
            stack.insert(0, u)
    return subtree



def transform_to_kary_tree(G, binG):
    def extract_tree(G, g):
        # extract nodes and values in G only if existed in g
        tree = {}
        for k, v in g.iteritems():
            nb = G[k]
            tree[k] = {nbk: nbv for nbk, nbv in nb.iteritems() if nbk in g}
        return tree

    if len(G) == 1:
        return G.keys()[0]


    mid, depth = find_tree_root(G)
    mid_depth = depth[mid]

    subtrees = [create_subtree(G, child_root, mid) for child_root in G[mid]]

    for tree in subtrees:
        if not tree:
            continue

        handle = transform_to_kary_tree(tree, binG)

        binG[mid] = binG.get(mid, {})
        binG[mid][handle] = {}
        binG[handle] = binG.get(handle, {})
        binG[handle].update({mid: {}})
        
    root = mid
    return root


def create_labels(tree):
    shortest_dist_lookup = {}
    k_ary_tree = {}
    root = transform_to_kary_tree(tree, k_ary_tree)
    labels = {root:{root:0}}
    stack = [root]
    while stack:
        parent = stack.pop()
        # pre-emptive calculation
        dijkstra(tree, parent, target=None, dynamic_lookup=shortest_dist_lookup)
        for child in k_ary_tree[parent]:
            if child in labels:
                continue
            labels[child] = {}
            for ancestor in labels[parent]:
                # apply shortest dist on the original tree, not the transformed one
                _, dist = dijkstra(tree, child, target=ancestor, dynamic_lookup=shortest_dist_lookup)
                labels[child][ancestor] = dist
                labels[child][child] = 0
            stack.insert(0, child)
    return labels

#######
# Testing
#


def get_distances(G, labels):
    # labels = {a:{b: distance from a to b,
    #              c: distance from a to c}}
    # create a mapping of all distances for
    # all nodes
    distances = {}
    for start in G:
        # get all the labels for my starting node
        label_node = labels[start]
        s_distances = {}
        for destination in G:
            shortest = float('inf')
            # get all the labels for the destination node
            label_dest = labels[destination]
            # and then merge them together, saving the
            # shortest distance
            for intermediate_node, dist in label_node.iteritems():
                # see if intermediate_node is our destination
                # if it is we can stop - we know that is
                # the shortest path
                if intermediate_node == destination:
                    shortest = dist
                    break
                other_dist = label_dest.get(intermediate_node)
                if other_dist is None:
                    continue
                if other_dist + dist < shortest:
                    shortest = other_dist + dist
            s_distances[destination] = shortest
        distances[start] = s_distances
    return distances

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G

def test():
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2


import math

def max_labels(labels):
    return max(len(labels[u]) for u in labels)

def labels_needed(G):
    return 1 + int(math.ceil(math.log(len(G))/math.log(2)))

def test_ked4r():
    # binary tree
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][4] == 2    
    assert distances[4][1] == 2
    assert distances[1][4] == 2
    assert distances[2][1] == 1
    assert distances[1][2] == 1   
    assert distances[1][1] == 0
    assert distances[2][2] == 0
    assert distances[9][9] == 0
    assert distances[2][3] == 2
    assert distances[12][13] == 2
    assert distances[13][8] == 6
    assert distances[11][12] == 6
    assert distances[1][12] == 3
    print 'test1 passes'

    # chain graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7),
             (7, 8), (8, 9), (9, 10), (10, 11), (11, 12), (12, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][2] == 1
    assert distances[1][3] == 2
    assert distances[1][13] == 12
    assert distances[6][1] == 5
    assert distances[6][13] == 7
    assert distances[8][3] == 5
    assert distances[10][4] == 6
    print 'test2 passes'

    # "star-chain" graph
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 7), 
             (7, 8), (8, 9), (1, 10), (10, 11), (11, 12), (12, 13)]    
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)
    labels = create_labels(tree)
    assert labels_needed(tree) >= max_labels(labels)
    distances = get_distances(tree, labels)
    assert distances[1][1] == 0
    assert distances[5][5] == 0
    assert distances[1][2] == 1
    assert distances[1][3] == 2    
    assert distances[1][4] == 3
    assert distances[1][5] == 4
    assert distances[5][6] == 5
    assert distances[5][7] == 6
    assert distances[5][8] == 7
    assert distances[5][9] == 8
    print 'test3 passes'

from collections import deque

def distance(tree, w, u):
    if w==u: return 0

    distances = {w: 0}
    frontier = deque([w])
    while frontier:
        n = frontier.popleft()
        for s in tree[n]:
            if s not in distances: 
                distances[s] = distances[n] + tree[n][s]
                frontier.append(s)
            if s==u:
                return distances[u]

    return None

from math import log, ceil
from random import randint

def test_kulakovsky():
    N = 100
    n0 = 20
    n1 = 100

    for _ in range(N):
        tree = {}
        for w in range(1, n0):
            make_link(tree, w, w+1, randint(1, 1))

        for w in range(n0+1, n1+1):
            make_link(tree, randint(1, w-1), w, randint(1, 1))

        labels = create_labels(tree)
        distances = get_distances(tree, labels)

        assert max([len(labels[n]) for n in tree]) <= int(ceil(log(len(tree)+1, 2)))

        for _ in range(N):
            w = randint(1, n1)
            u = randint(1, n1)
            assert distance(tree, w, u) == distances[w][u]

    print 'random_test() passed'

def test_weighted():
    edges = [('a', 'b', 5), ('a', 'c', 9), ('b', 'h', 7), ('b', 'g', 6),
             ('h', 'm', 8), ('c', 'd', 2), ('d', 'e', 4), ('d', 'f', 3)]
    w_tree = {}
    for n1, n2, wt in edges:
        make_link(w_tree, n1, n2, wt)
    w_labels = create_labels(w_tree)
    w_distances = get_distances(w_tree, w_labels)
    assert w_distances['a'] == {'a': 0, 'c': 9, 'b': 5, 'e': 15, 'd': 11, 'g': 11, 'f': 14, 'h': 12, 'm': 20}
    assert w_distances['b'] == {'a': 5, 'c': 14, 'b': 0, 'e': 20, 'd': 16, 'g': 6, 'f': 19, 'h': 7, 'm': 15}
    assert w_distances['c'] == {'a': 9, 'c': 0, 'b': 14, 'e': 6, 'd': 2, 'g': 20, 'f': 5, 'h': 21, 'm': 29}
    assert w_distances['d'] == {'a': 11, 'c': 2, 'b': 16, 'e': 4, 'd': 0, 'g': 22, 'f': 3, 'h': 23, 'm': 31}
    assert w_distances['e'] == {'a': 15, 'c': 6, 'b': 20, 'e': 0, 'd': 4, 'g': 26, 'f': 7, 'h': 27, 'm': 35}
    assert w_distances['f'] == {'a': 14, 'c': 5, 'b': 19, 'e': 7, 'd': 3, 'g': 25, 'f': 0, 'h': 26, 'm': 34} 
    assert w_distances['g'] == {'a': 11, 'c': 20, 'b': 6, 'e': 26, 'd': 22, 'g': 0, 'f': 25, 'h': 13, 'm': 21}
    assert w_distances['h'] == {'a': 12, 'c': 21, 'b': 7, 'e': 27, 'd': 23, 'g': 13, 'f': 26, 'h': 0, 'm': 8}
    assert w_distances['m'] == {'a': 20, 'c': 29, 'b': 15, 'e': 35, 'd': 31, 'g': 21, 'f': 34, 'h': 8, 'm': 0}
    print 'weighted_test passed'
    return

def test_units():
    import json
    # edges = [(1, 2), (3, 2), (3, 4), (4, 5), (5, 6), (6, 7)]
    # edges = [(1, 2), (3, 2), (2, 4), (4, 5), (5, 6), (5, 7)]
    edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7),
             (4, 8), (4, 9), (5, 10), (5, 11), (6, 12), (6, 13)]
    tree = {}
    for n1, n2 in edges:
        make_link(tree, n1, n2)


    bintree = {}
    root = transform_to_kary_tree(tree, bintree)
    print 'root is', root

    labels = create_labels(tree)
    print json.dumps(labels, indent=2)

test_units()
test()
test_weighted()
# test_kulakovsky()
test_ked4r()
