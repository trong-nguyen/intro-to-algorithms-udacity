#
# Design and implement an algorithm that can preprocess a
# graph and then answer the question "is x connected to y in the
# graph" for any x and y in constant time Theta(1).
#

#
# `process_graph` will be called only once on each graph.  If you want,
# you can store whatever information you need for `is_connected` in
# global variables
#
global_values = {}

def assign_value(lead_node, G, G_values):
    # BFS
    stack = [lead_node]
    while stack:
        w = stack.pop()
        for u in G[w]:
            if u in G_values:
                continue
            G_values[u] = G_values[w]
            stack.insert(0, u)



def process_graph(G):
    global_values.clear() # reset
    # for each node, assign its value to its neighbor
    # if two nodes have the same value, they are connected
    # we follow lead node and do BFS to all its connected neighbor
    # then we select another lead node which is not searched yet
    value = 0
    for v in G:
        if v in global_values:
            continue
        global_values[v] = value
        assign_value(v, G, global_values)
        value += 1


#
# When being graded, `is_connected` will be called
# many times so this routine needs to be quick
#
def is_connected(i, j):
    assert global_values != {}, "global values should be initialized first"
    assert i in global_values and j in global_values, "{} and {} not in global values".format(i, j)
    return global_values[i] == global_values[j]

#######
# Testing
#
def test():
    G = {'a':{'b':1},
         'b':{'a':1},
         'c':{'d':1},
         'd':{'c':1},
         'e':{}}
    process_graph(G)
    assert is_connected('a', 'b') == True
    assert is_connected('a', 'c') == False

    G = {'a':{'b':1, 'c':1},
         'b':{'a':1},
         'c':{'d':1, 'a':1},
         'd':{'c':1},
         'e':{}}
    process_graph(G)
    assert is_connected('a', 'b') == True
    assert is_connected('a', 'c') == True
    assert is_connected('a', 'e') == False

test()
