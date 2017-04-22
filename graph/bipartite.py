#
# Write a function, `bipartite` that
# takes as input a graph, `G` and tries
# to divide G into two sets where 
# there are no edges between elements of the
# the same set - only between elements in
# different sets.
# If two sets exists, return one of them
# or `None` otherwise
# Assume G is connected
#

def bipartite(G):
    # your code here
    # return a set
    explored = {}
    origin = G.keys()[0]
    team = {origin: 'captain'}
    stack = [origin]
    one_team = {'captain': [origin], 'iron': []}
    while stack:
        v = stack.pop(0)
        print v, team[v], G[v].keys()
        nb_team = 'iron' if team[v] == 'captain' else 'captain'
        explored[v] = True
        for nb in G[v]:
            if nb in explored:
                continue
            print '\tassign', nb, nb_team
            if nb not in team:
                team[nb] = nb_team
                one_team[nb_team].append(nb)
                stack.append(nb)
            else:
                if team[nb] != nb_team:
                    return None
    return set(one_team['captain'])



########
#
# Test

def make_link(G, node1, node2, weight=1):
    if node1 not in G:
        G[node1] = {}
    (G[node1])[node2] = weight
    if node2 not in G:
        G[node2] = {}
    (G[node2])[node1] = weight
    return G


def test():
    edges = [(1, 2), (2, 3), (1, 4), (2, 5),
             (3, 8), (5, 6)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert (g1 == set([1, 3, 5]) or
            g1 == set([2, 4, 6, 8]))
    edges = [(1, 2), (1, 3), (2, 3)]
    G = {}
    for n1, n2 in edges:
        make_link(G, n1, n2)
    g1 = bipartite(G)
    assert g1 == None

test()
