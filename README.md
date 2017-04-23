# ALGORITHMS IMPLEMENTED FOLLOWING MICHAEL LITTMAN'S INTRO TO ALGORITHM ON UDACITY
School: Udacity  
Class: CS215
Lecturer: Michael Littman  

Mostly on Graph Theory

<!-- MarkdownTOC -->

- Dijkstra algorithm - Find shortest path with weights
- Bipartite
- Feel the love - Find walk with maximum weight between nodes i and j, allowing duplicated nodes or edges
- Find best flights
- Shortest distance for binary tree
- Shortest distance for generic tree
- K-shortest path problem with Yen's Algorithm
- K-shortest path problem with Dijkstra algorithm
- Awesome problems:
- The 100 prisoners, 100 boxes and their fates
- Other techniques

<!-- /MarkdownTOC -->

## Dijkstra algorithm - Find shortest path with weights

- Make graph / connectivity map
- Traverse BFS
- Radiate from source node, traverse BFS
- Check all neighbor nodes
- Keep track of current distances to the source node
- Select the node with smallest distance to proceed to next round
- Accumulate rule could be altered to allow flexibility, see `graph/least_obscure_path.py` problem

More about Dijkstra's algorithm [here](https://www.quora.com/Is-Dijkstras-Algorithm-a-greedy-algorithm-or-a-dynamic-programming-algorithm). Tip: it is a greedy algorithm.

## Bipartite

> Find possible bipartite groups in a connected graph. Should return 2 bipartite sets or None if not found.

Self - algorithm. Time complexity at most of O(m), using BFS, flipping from value (A) to another (B) on traversing.

Assign center node one value A, their neighbors value B, then their neighbors of neighbors value A again.
In the process if neighbor of a node has a value, and that value is the same as the central node (which means there are connections between one team) we stop and return None, no bipartite set found.

## Feel the love - Find walk with maximum weight between nodes i and j, allowing duplicated nodes or edges
See discussions [here](https://discussions.udacity.com/search?q=feel%20the%20love%20category%3A570)

See code in [file](graph/feel_the_love.py)

This algorithm is an example of thinking-out-of-the-box. Do not trap your thinking in traversing around the graph which allows cycles and duplicates, it is a rabbit hole to follow.

The answer is simple:
- Check whether i and j are connected.
- Check all edges reachable from i (or j) and keep track of the maximum love / weight, call this the u-v edge.
- Build the path, really, the actual form of the path doesnot matter at all. So frankly we would build a path such as: `path = path(i to u) + path(v to j)`.

I believe (without proof) that either BFS or DFS can be used, as the form of the path is not important, as long as the path connects i and j and the edge with maximum love: uv.

Complexity analysis:
- Connectivity check: ϴ(n+m)
- Find edge with max love: ϴ(n+m)
- Build path: ϴ(n+m) from i to u and ϴ(n+m) from v to j

Total: **ϴ(n+m)**. Cool!

Possible application: Game programming, find the path to get the most valuable chest. It does not matter how long you travel or how silly your path is (back and forth, around, cyclic)

## Find best flights
> Given lots of flights with corresponding costs, arrival/departure times, origins and destinations. Find a combination of flights that get your from point A to point B subjected to a number of constraints: cost / flight time efficient, minimum transit time, no overnight flights, etc.

```python
flights = [(523, 'Broome', 'Derby', '07:17', '08:57', 60),
       (549, 'Broome', 'Perth', '17:16', '19:18', 100),
       (604, 'Carnarvon', 'Perth', '14:50', '17:16', 200),
       (612, 'Carnarvon', 'Perth', '19:54', '22:38', 50),
       (107, 'Derby', 'Broome', '08:44', '10:36', 160),
       (108, 'Derby', 'Broome', '21:18', '23:04', 30),
       (622, 'Derby', 'Fitzroy Crossing', '13:59', '15:04', 60),
       (112, 'Derby', 'Fitzroy Crossing', '19:24', '20:15', 60),
       (113, 'Derby', 'Geraldton', '07:00', '08:10', 20),
       (638, 'Fitzroy Crossing', 'Derby', '09:18', '10:08', 50),
       (654, 'Fitzroy Crossing', 'Halls Creek', '07:55', '09:48', 180),
       (143, 'Fitzroy Crossing', 'Halls Creek', '09:45', '11:39', 20),
       (661, 'Fitzroy Crossing', 'Halls Creek', '20:35', '22:19', 200),
       (663, 'Geraldton', 'Carnarvon', '08:30', '10:24', 30),
    ]
```

**Solution**
See problem [here](https://discussions.udacity.com/search?q=find%20best%20flight%20category%3A570)

See code in [file](graph/find_best_flights.py)

- Based on Dijkstras algorithm
- Divide the contraints into qualitative and quantitative:
	* Qualitative: no over flight time which means connecting flight must be in order with respect to timeline, e.g. if we have `flight = leg a -> leg b -> leg c` then leg a arrival time must be < leg b departure time + commuting time allowance (1 hour for ex.)
	* Quantitative: such as cost and flight time with definite constraint, for ex. of type *minimal*
- The steps are:
	* Build the graph based on the qualitative constraints: flights as nodes, not the destinations. Node A (flight A) can only be connected to node B if Constraints(node A, node B) satisfies the qualitative terms. Such as `nodeB['departure'] >= nodeA['arrival'] + commutingTime`

	* Traversing the built graph based on Dijkstra algorithm with target function takes multiple constraints to produce a single value as Dijkstras weight. 
		- `f(cost, duration) = cost * inf + duration` where `inf` is orders larger than duration
- Think of the problem as a multivariate version of Dijkstras shorted weighted path algorithm. Where each constraint added introduces an additional dimension to the tree.
- Note that we might end up with more than one tree, i.e. we have more than one region, or all the nodes are not connected due to the qualitative / tree building requirements.

Complexity: **ϴ((n+m)^d)** where d is the number of qualitative constraints

## Shortest distance for binary tree

See code [here](graph/distance_oracle_1.py)

Think of the problem as the shortest distance problem in graph theory with binary tree as the underlying structure. 

The takeaway: we should make good use of the knowledge about binary tree to enhance traversals and search. 

For example: in a binary tree, the shortest path (in terms of hops) between any x, y nodes is the path between x to z and z to y, where z is the common node on the up-traversing paths between x and y to root.

## Shortest distance for generic tree

See code [here](graph/distance_oracle_2.py)

The tactic here is that we could convert this problem to binary tree shortest distance. Since we are only concerned about the shortest distances between nodes, not the actual path that we used to compute the distances, we could make use of the solution that we developed for binary trees after tactically transforming a generic tree to a binary tree structure with virtual binary connectivities. 

Now if tree A is a generic tree, with distances da(i,j), after the transformation we would have a binary tree B, with distances db(i,j) = da_shortest(i,j) where da is a direct connection and da_shortest is a shortest path connection. The ultimate purpose is to reduce the many connectivities in a generic tree to lesser connectivities in a binary one.

Algorithm:
- Convert generic tree A to binary tree B
	* Recursively split trees at the middle point
	* Finding mid-depth nodes:
		- Starting from random node v
		- Find the node x with max depth from v, using breadth-first-search (BFS)
		- Find node y with max depth from x, using BFS
		- Find the middle depth point between x and y
	* Split tree into sub trees branching from the mid depth nodes, splitting techniques use branch removing technique: copy all nodes from branch i-th of mid-depth nodes.
- Create labels for tree B
	* Similar to binary tree shortest path
	* Starting from root, assign distances from parent p-child c in tree B by the shortest distance between node p and node c in tree A, using Dijkstras algorithm, take into account distances possibly having weights.
	* To increase efficiency, Dijkstras search is modified to use a dynamic table lookup. Susequent search can look into the table to check searched shortest distances between any (i,j) pair and update the table with its own search results.

Algorithms used:
- Greedy method (Dijkstras)
- Divide and conquer (tree splitting)
- Dynamic programming (modified Dijkstras, tree splitting)
- Memoization (modified Dijkstras)

Complexity:
- Tree conversion: logn splitting steps, for each step we need 2(n+m) BFS search: ϴ(logn(n+m))
- Label creation: at most we need to run logn full Dijkstras (mlogn) search: ϴ(m(logn)^2)

Total: **ϴ(m(logn)^2)**

## K-shortest path problem with Yen's Algorithm

Using [Yen's algorithm](https://en.wikipedia.org/wiki/Yen%27s_algorithm) we can progressively find the top k-shortest paths. The algorithm relies on the shortest path (using any shortest path method, such as Dijkstra's) as contraints.

See code [here](graph/top_two_using_yen_algo.py).

Algorithm:
- Step 1: Find the shortest path
- Step 2: find the next shortest path (A_k) which deviates from the top path (A_k+1). The second shortest A2 could be found from the shortest A1 from step 1.
	* For all edges on the shortest path:
		- Virtually remove the edge
		- Find the shortest path from the first verted of the removed edge to the target node of the graph with the edge removed.
		- Compute the deviating path (spur_path) cost: `cost(root_path + spur_path)`
	* Compare the cost of all deviating paths, select the one with the lowest cost, it is the A_k shortest path

Cost: **ϴ(l\*(m + nlogn))=ϴ(n(m + nlogn))** where k is number of edges of the shortest path. O(l) = (logn, n)

## K-shortest path problem with Dijkstra algorithm

See code [here](graph/top_two_using_kdijkstra.py).

It turns out that Dijkstra shourtest path algorithm could be modified to solve k-shortest problems in the following manner:

Algorithm:
- Hold a race from start node where the branches are kept expanding. The first k path that reaches the end node first are the k shortest paths.
- Basically it follows Dijkstra where we expand the branch following the path of current lowest cost. While in the original version only the shortest path is saved, in the modifed version all paths are saved and continously fed with added edges following the branch with lowest cost.

**The catch**: while it has similar time complexity to the simpler shortest path version, it is much more expensive in terms of space complexity **ϴ(m!)** (need proof).

## Awesome problems:

## The 100 prisoners, 100 boxes and their fates
See [here](http://puzzling.stackexchange.com/questions/16/100-prisoners-names-in-boxes)


> The names of 100 prisoners are placed in 100 wooden boxes, one name to a box, and the boxes are lined up on a table in a room.

> One by one, the prisoners are led into the room; each may look in at most 50 boxes, but must leave the room exactly as he found it and is permitted no further communication with the others.

> The prisoners have a chance to plot their strategy in advance, and they are going to need it, because unless every single prisoner finds his own name all will subsequently be executed.

>> Find a strategy for them which has probability of success (all prisoners' survival) exceeding 30%.

>> Comment: If each prisoner examines a random set of 50 boxes, their probability of survival is an unenviable 1/2^(100)≈0.0000000000000000000000000000008. They could do worse—if they all look in the same 50 boxes, their chances drop to zero. 30% seems ridiculously out of reach—but yes, you heard the problem correctly.


Algorithm:
```python
assign(prisoners, ids) # 1 to 100 for example

def open(boxes, label):
	content = boxes[label]
	if content != his_id:
		label = content
		open(boxes, label)

for each prisoner:
	# keep open the box with labels obtained from the content in the previous open
	initial_label = his_id
	open(boxes, initial_label)
	# until he ran out of options # n/2
```

| n | Success rate |
| ---- | ----------------- |
| 2 |               0.50 |
| 4 |               0.42 |
| 6 |               0.38 |
| 8 |               0.37 |
| 10 |              0.35 
| 100 |               0.3118 |
| n |               1/n + 1/(n-1) + ... + 1/(n/2+1) = 1 - (1 + 1/2 + 1/3 + ... + 1/n)  |


In essence, the algorithm that receive input from both:
- global (myId)
- individual feedback (result if I choose labels based on myId) can give very high rate of success **0.42** in case `n=4`
- even without any sort of global communication (prisoners can learn from each other' results)

This problem is highly interesting if consider parallelism:
- Each thread is only concerned with its ids and its local data `data[id]`
- We can parallelize the algorithm in a very efficient manner, since there is little (actually none) information exchanged between threads.

## Other techniques

- Learn more about the Python's overridable.
```python
__repr__: # used by caller's __str__() method, to really distingush object from others, unambigous

__str__: # to make it readable, could be ambiguous, optional to implement

__contains__: # 'in' operator

__getitem__: # '[]' operator

__add__: # '+' operator
```

- Don't use list or dict, or any mutable objects as default parameters. Just don't, proof here [Watch out for default parameters](http://reinout.vanrees.org/weblog/2012/04/18/default-parameters.html)! Since all calls to the function with default parameter will share the same default object, in this case, list or dict. So altering the objects will be seen by subsequent calls to the function.

Use `None` instead.

```python
def f_with_default(default_dict={}, default_list=[]):
	from random import random
	print 'default_dict is {}'.format(default_dict)
	print 'default_list is {}'.format(default_list)

	num = random()
	default_dict[num] = num
	default_list.append(num)

print '1st call, defaults are initialized and empty'
f_with_default()

print '\n2nd call, defaults now refer to the one initialized with and mutated by 1st call'
f_with_default()
```
- when dealing with extremely large or exceedingly small numbers, remember logarithm tools
`log(a*b*c) = log(a+b+c)`
- when designing algorithms, be fixated or opinionated about options, minimize configurations. Leave details for sub data structures to deal with.

For example: considering the above Dijkstras algorithm, you would like to write a routine which employs exactly:

- (1) add (+) accumulation rules and 
- (2) minimize distance / shortest distance.

For specific applications:
- Implement a datastructure that wraps `distance` structure contained in graph
- If we need accumulation rules to be division / multiplication: just overriding `__add__(self, x)` operator
- If we need largest distances instead: transform the graph with opposite sign: plus (+) to minus (-)