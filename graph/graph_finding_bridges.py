# Pre-order Tarjan algorithm

from yaml import dump as nice_dump

# Bridge Edges v4
#
# Find the bridge edges in a graph given the
# algorithm in lecture.
# Complete the intermediate steps
#  - create_rooted_spanning_tree
#  - post_order
#  - number_of_descendants
#  - lowest_post_order
#  - highest_post_order
#
# And then combine them together in
# `bridge_edges`

# So far, we've represented graphs 
# as a dictionary where G[n1][n2] == 1
# meant there was an edge between n1 and n2
# 
# In order to represent a spanning tree
# we need to create two classes of edges
# we'll refer to them as "green" and "red"
# for the green and red edges as specified in lecture
#
# So, for example, the graph given in lecture
# G = {'a': {'c': 1, 'b': 1}, 
#      'b': {'a': 1, 'd': 1}, 
#      'c': {'a': 1, 'd': 1}, 
#      'd': {'c': 1, 'b': 1, 'e': 1}, 
#      'e': {'d': 1, 'g': 1, 'f': 1}, 
#      'f': {'e': 1, 'g': 1},
#      'g': {'e': 1, 'f': 1} 
#      }
# would be written as a spanning tree
# S = {'a': {'c': 'green', 'b': 'green'}, 
#      'b': {'a': 'green', 'd': 'red'}, 
#      'c': {'a': 'green', 'd': 'green'}, 
#      'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
#      'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
#      'f': {'e': 'green', 'g': 'red'},
#      'g': {'e': 'green', 'f': 'red'} 
#      }
#       
def create_rooted_spanning_tree(G, root):
    GCopied = {k:{kk:'green' for kk, vv in v.items()} for k, v in G.items()}
    v = root
    list = [v]
    explored = {v:True}
    reds = []
    while list:
        w = list.pop(0)
        for nb in GCopied[w]:
            if nb != w:
                if nb in explored:
                    reds.append((w, nb))
                else:
                    explored[nb] = True
                    del GCopied[nb][w]
                    list.append(nb)
    S = {k:{kk:'green' for kk, vv in v.items()} for k, v in G.items()}
    for a, b in reds:
        S[a][b] = 'red'
        S[b][a] = 'red'
    return S

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result
# feel free to edit the test to
# match the solution your program produces
def test_create_rooted_spanning_tree():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    S = create_rooted_spanning_tree(G, "a")
    print nice_dump(S)
    assert S == {'a': {'c': 'green', 'b': 'green'}, 
                 'b': {'a': 'green', 'd': 'red'}, 
                 'c': {'a': 'green', 'd': 'green'}, 
                 'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
                 'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
                 'f': {'e': 'green', 'g': 'red'},
                 'g': {'e': 'green', 'f': 'red'} 
                 }

###########
# test_create_rooted_spanning_tree()

def post_order(S, root):
    def mark_component(S, v, marked, ind, order):
        # the sorted is for enforcing alphabet order
        for nb in sorted(S[v].keys()):
            if S[v][nb] == 'red' or nb in marked:
                continue
            marked[nb] = True
            mark_component(S, nb, marked, ind, order)

        order[v] = ind.pop(0) + 1



    # return mapping between nodes of S and the post-order value
    # of that node
    marked = {root: True}
    ind = list(range(len(S)))
    order = {}
    mark_component(S, root, marked, ind, order)
    return order

    # return {k:len([nb for nb in v if v[nb] == 'green'])+1 for k, v in }

# This is just one possible solution
# There are other ways to create a 
# spanning tree, and the grader will
# accept any valid result.
# feel free to edit the test to
# match the solution your program produces
def test_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    assert po == {'a':7, 'b':1, 'c':6, 'd':5, 'e':4, 'f':2, 'g':3}

# test_post_order()
##############

def number_of_descendants(S, root):
    # return mapping between nodes of S and the number of descendants
    # of that node
    def traverse(S, v, marked, descendants):
        descendants[v] = 1
        for nb in S[v]:
            if S[v][nb] == 'red' or nb in marked:
                continue
            marked[nb] = True
            descendants[v] += traverse(S, nb, marked, descendants)
        return descendants[v]

    marked = {root: True}
    descendants = {}
    traverse(S, root, marked, descendants)
    return descendants

def test_number_of_descendants():
    S =  {'a': {'c': 'green', 'b': 'green'}, 
          'b': {'a': 'green', 'd': 'red'}, 
          'c': {'a': 'green', 'd': 'green'}, 
          'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
          'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
          'f': {'e': 'green', 'g': 'red'},
          'g': {'e': 'green', 'f': 'red'} 
          }
    nd = number_of_descendants(S, 'a')
    assert nd == {'a':7, 'b':1, 'c':5, 'd':4, 'e':3, 'f':1, 'g':1}

# test_number_of_descendants()
###############
def eval_post_order(S, root, po, eval_type):
    # return a mapping of the nodes in S
    # to the lowest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    def traverse(S, v, po, marked, lpo):
        lpo[v] = po[v]
        for nb in sorted(S[v].keys()):
            if S[v][nb] == 'red':
                lpo[v] = eval_type(lpo[v], po[nb])
                continue
            if nb in marked:
                continue
            marked[nb] = True
            lpo[v] = eval_type(lpo[v], traverse(S, nb, po, marked, lpo))
        return lpo[v]

    marked = {root: True}
    lpo = {}
    traverse(S, root, po, marked, lpo)
    return lpo

def lowest_post_order(S, root, po):
    return eval_post_order(S, root, po, min)


def test_lowest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    l = lowest_post_order(S, 'a', po)
    print nice_dump(l)
    assert l == {'a':1, 'b':1, 'c':1, 'd':1, 'e':2, 'f':2, 'g':2}

# test_lowest_post_order()
################

def highest_post_order(S, root, po):
    # return a mapping of the nodes in S
    # to the highest post order value
    # below that node
    # (and you're allowed to follow 1 red edge)
    return eval_post_order(S, root, po, max)

def test_highest_post_order():
    S = {'a': {'c': 'green', 'b': 'green'}, 
         'b': {'a': 'green', 'd': 'red'}, 
         'c': {'a': 'green', 'd': 'green'}, 
         'd': {'c': 'green', 'b': 'red', 'e': 'green'}, 
         'e': {'d': 'green', 'g': 'green', 'f': 'green'}, 
         'f': {'e': 'green', 'g': 'red'},
         'g': {'e': 'green', 'f': 'red'} 
         }
    po = post_order(S, 'a')
    h = highest_post_order(S, 'a', po)
    print nice_dump(h)
    assert h == {'a':7, 'b':5, 'c':6, 'd':5, 'e':4, 'f':3, 'g':3}
    
# test_highest_post_order()
#################

def bridge_edges(G, root):
    # use the four functions above
    # and then determine which edges in G are bridge edges
    # return them as a list of tuples ie: [(n1, n2), (n4, n5)]
    S = create_rooted_spanning_tree(G, root)
    po = post_order(S, root)
    des = number_of_descendants(S, root)
    lo = lowest_post_order(S, root, po)
    ho = highest_post_order(S, root, po)

    bridges = []
    explored = {root: True}
    open_list = [root]
    while open_list:
        w = open_list.pop()
        for nb in S[w]:
            if S[w][nb] == 'red' or nb in explored:
                continue
            explored[nb] = True
            open_list.append(nb)
            if ho[nb] <= po[nb] and lo[nb] > po[nb] - des[nb]:
                bridges.append((w, nb))
    return bridges



def test_bridge_edges():
    G = {'a': {'c': 1, 'b': 1}, 
         'b': {'a': 1, 'd': 1}, 
         'c': {'a': 1, 'd': 1}, 
         'd': {'c': 1, 'b': 1, 'e': 1}, 
         'e': {'d': 1, 'g': 1, 'f': 1}, 
         'f': {'e': 1, 'g': 1},
         'g': {'e': 1, 'f': 1} 
         }
    bridges = bridge_edges(G, 'a')
    print nice_dump(bridges)
    assert bridges == [('d', 'e')]

# test_bridge_edges()