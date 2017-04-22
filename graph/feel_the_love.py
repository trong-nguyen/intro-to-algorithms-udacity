#
# Take a weighted graph representing a social network where the weight
# between two nodes is the "love" between them.  In this "feel the
# love of a path" problem, we want to find the best path from node `i`
# and node `j` where the score for a path is the maximum love of an
# edge on this path. If there is no path from `i` to `j` return
# `None`.  The returned path doesn't need to be simple, ie it can
# contain cycles or repeated vertices.
#
# Devise and implement an algorithm for this problem.
#
def bfs(G, i, j):
    explored = {}
    nodes = [i]
    reach = {i: 'root'}
    while nodes:
        w = nodes.pop()
        explored[w] = True
        for u in G[w]:
            if u in explored:
                continue
            reach[u] = w
            nodes.insert(0, u)
            if u == j:
                return reach
    return None

def bfs_track(G, i):
    explored = {}
    nodes = [i]
    max_love = (0., ('root',i))
    while nodes:
        w = nodes.pop()
        explored[w] = True
        for u in G[w]:
            if u in explored:
                continue
            max_love = max(max_love, (G[w][u], (w,u)))
            nodes.insert(0, u)
    return max_love

def retrieve_path(reach, i, j):
    assert reach, 'invalid reach {}'.format(reach)
    assert i in reach and j in reach, '{} and {} not in path'.format(i, j)
    path = [j]
    prior = j
    while prior != i:
        prior = reach[prior]
        path.insert(0, prior)
    return path

def feel_the_love(G, i, j):
    # return a path (a list of nodes) between `i` and `j`,
    # with `i` as the first node and `j` as the last node,
    # or None if no path exists

    # BFS between i and j
    direct_reach = bfs(G, i, j)
    if not direct_reach:
        return None

    # BFS from i for the entire graph and get the max love
    max_love_value, (u, v) = bfs_track(G, i)

    # build the path from i to max and max to j
    path = []
    for segment in [(i,u), (v,j)]:
        s1, s2 = segment
        if s1 == s2:
            # collapsed ends
            path += [s1]
        else:
            reach = bfs(G, s1, s2)
            path += retrieve_path(reach, s1, s2)
    return path


#########
#
# Test

def score_of_path(G, path):
    max_love = -float('inf')
    for n1, n2 in zip(path[:-1], path[1:]):
        love = G[n1][n2]
        if love > max_love:
            max_love = love
    return max_love

def test():
    G = {'a':{'c':1},
         'b':{'c':1},
         'c':{'a':1, 'b':1, 'e':1, 'd':1},
         'e':{'c':1, 'd':2},
         'd':{'e':2, 'c':1},
         'f':{}}
    path = feel_the_love(G, 'a', 'b')
    assert score_of_path(G, path) == 2

    path = feel_the_love(G, 'a', 'f')
    assert path == None

    G = {'a': {'b': 9.0199999999999996, 'e': 0.01, 'd': 0.32000000000000001, 'g': 5.7800000000000002, 'f': 6.9299999999999997, 'i': 7.6799999999999997, 'h': 5.7199999999999998, 'k': 0.26000000000000001}, 'c': {'b': 4.7699999999999996, 'e': 3.2599999999999998, 'd': 8.3800000000000008, 'i': 4.6500000000000004, 'h': 8.8599999999999994, 'k': 1.6599999999999999}, 'b': {'a': 9.0199999999999996, 'c': 4.7699999999999996, 'e': 4.1100000000000003, 'g': 8.2599999999999998, 'f': 2.23, 'i': 0.33000000000000002, 'h': 8.4399999999999995, 'k': 5.3499999999999996, 'j': 2.1299999999999999}, 'e': {'a': 0.01, 'c': 3.2599999999999998, 'b': 4.1100000000000003, 'd': 7.7400000000000002, 'f': 7.7000000000000002, 'j': 8.1600000000000001}, 'd': {'a': 0.32000000000000001, 'h': 1.01, 'c': 8.3800000000000008, 'e': 7.7400000000000002, 'f': 1.45}, 'g': {'a': 5.7800000000000002, 'h': 4.9900000000000002, 'b': 8.2599999999999998, 'i': 1.21}, 'f': {'a': 6.9299999999999997, 'b': 2.23, 'e': 7.7000000000000002, 'd': 1.45, 'i': 2.3799999999999999, 'h': 1.26, 'j': 2.0299999999999998}, 'i': {'a': 7.6799999999999997, 'c': 4.6500000000000004, 'b': 0.33000000000000002, 'g': 1.21, 'f': 2.3799999999999999, 'h': 3.8500000000000001, 'k': 6.0999999999999996}, 'h': {'a': 5.7199999999999998, 'c': 8.8599999999999994, 'b': 8.4399999999999995, 'd': 1.01, 'g': 4.9900000000000002, 'f': 1.26, 'i': 3.8500000000000001, 'k': 7.7699999999999996, 'j': 8.6899999999999995}, 'k': {'a': 0.26000000000000001, 'c': 1.6599999999999999, 'b': 5.3499999999999996, 'i': 6.0999999999999996, 'h': 7.7699999999999996, 'j': 1.22}, 'j': {'h': 8.6899999999999995, 'k': 1.22, 'b': 2.1299999999999999, 'e': 8.1600000000000001, 'f': 2.0299999999999998}}
    path = feel_the_love(G, 'a', 'h')
    assert abs(score_of_path(G, path) - 9.0199999999999996) < 1.e-6