import yaml
from heap import *

# Dijkstra algorithm
# Advance features:
# - Custom accumulate rule (max of 2, product of 2, sum of 2
# - Dynamic lookup / reusable results from prior search

# Basic Accessor, Retriever, of "distance" structure
class DistUnit(object):
	@classmethod
	def make(cls, weight, **kwarg):
		return weight

	@classmethod
	def weight(cls, unit):
		return unit

	@classmethod
	def add(cls, u1, u2):
		return u1 + u2

	@classmethod
	def smaller(cls, du1, du2):
		return du2 if cls.weight(du2) < cls.weight(du1) else du1

	@classmethod
	def pop_smallest(cls, distances):
		return heapq.heappop(distances)
		# return min([(cls.weight(v),k) for k, v in distances.iteritems()])[1]

# Class accessor with orientation
class OrientedDistUnit(DistUnit):
	@classmethod
	def make(cls, weight, node, parent, **kwarg):
		return (weight, node, parent)

	@classmethod
	def weight(cls, unit):
		return unit[0]

	@classmethod
	def parent(cls, unit):
		return unit[-1]

	@classmethod
	def shortest_path(cls, dist, destination, origin):
	    node = destination
	    path = [node]
	    while node != origin:
	        node = cls.parent(dist[node])
	        if node == None:
	        	return None
	        path.insert(0, node)

	    return path


def dijkstra(G, origin, target=None, dunit=DistUnit, dynamic_lookup=None, verbose=False):
	if dynamic_lookup != None:
		if target:
			success_string = '{}-{} pair found in lookup'.format(origin, target)
			if origin in dynamic_lookup and target in dynamic_lookup[origin]:
				if verbose: print success_string
				return dynamic_lookup[origin], dynamic_lookup[origin][target]
			elif target in dynamic_lookup and origin in dynamic_lookup[target]:
				if verbose: print success_string
				return dynamic_lookup[target], dynamic_lookup[target][origin]

		if origin in dynamic_lookup:
			final_dist = dynamic_lookup[origin]

			# shortest distance search has been found for all nodes
			if len(final_dist) == len(G):
				return final_dist

			dist_so_far = None
			for w in final_dist:
				for u in G[w]:
					if u not in final_dist:
						weight = dunit.add(dunit.weight(final_dist[w]), G[w][u])
						dist_so_far = {u: dunit.make(weight=weight, parent=w)}
						break
				if dist_so_far:
					break
			assert dist_so_far, 'Something wrong with dynamic_lookup logic, no dist found outside of final_dist'
		else:
			final_dist = dynamic_lookup[origin] = {}
			first_entry = dunit.make(0., node=origin, parent=None)
			dist_so_far = {origin: first_entry}
			heap = [first_entry]
			location = {first_entry:0}

	else:
		final_dist = {}
		first_entry = dunit.make(0., node=origin, parent=None)
		dist_so_far = {origin: first_entry}
		heap = [first_entry]
		location = {first_entry:0}


	while len(final_dist) < len(G):
		w = heappopmin(heap, location)[1]
		final_dist[w] = dist_so_far[w]
		if target == w:
			return final_dist, final_dist[target]
		del dist_so_far[w]
		for u in G[w]:
			if u in final_dist:
				continue

			s = dunit.add(dunit.weight(final_dist[w]), G[w][u])
			dist_data = dunit.make(weight=s, node=u, parent=w)
			if u not in dist_so_far:
				# add to the heap
				insert_heap(heap, dist_data, location)
				dist_so_far[u] = dist_data
			elif dunit.weight(dist_data) < dunit.weight(dist_so_far[u]):
				# update heap
				decrease_val(heap, location, dist_so_far[u], dist_data)
				dist_so_far[u] = dist_data



	return final_dist, None

def test_dijkstra():
	dunit = OrientedDistUnit


	graph = {
		'a':{'b': 6, 'c':4},
		'b':{'a': 6, 'c': 1, 'd': 5},
		'c':{'a': 4, 'b': 1, 'd': 7},
		'd':{'b': 5, 'c': 7, 'e': 7, 'f': 10},
		'e':{'d': 7, 'f': 2},
		'f':{'d': 10, 'e':2},
	}

	# print yaml.dump(graph)
	dl = {}
	shortest_from_a, _ = dijkstra(graph, 'a', dunit=dunit, dynamic_lookup=dl)
	dijkstra(graph, 'a', dynamic_lookup=dl)
	dijkstra(graph, 'a', target='e', dynamic_lookup=dl)
	dijkstra(graph, 'a', target='f', dynamic_lookup=dl)
	dijkstra(graph, 'f', target='a', dynamic_lookup=dl)

	print yaml.dump(shortest_from_a)

	assert dunit.weight(shortest_from_a['a']) == 0
	assert dunit.weight(shortest_from_a['b']) == 5
	assert dunit.weight(shortest_from_a['c']) == 4
	assert dunit.weight(shortest_from_a['d']) == 10
	assert dunit.weight(shortest_from_a['e']) == 17
	assert dunit.weight(shortest_from_a['f']) == 19

	print dunit.shortest_path(shortest_from_a, origin='a', destination='f')

# test_dijkstra()
