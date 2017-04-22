# generate the combinations
# select a strategy to select
# loop over combinations and count successful rate
# is_successful for a combination: selector's id is in selected labels

from itertools import permutations

def select(selector_id, case):
	# return {
	# 	0: [0, 1],
	# 	1: [2, 3],
	# 	2: [0, 2],
	# 	3: [1, 3]
	# }[selector_id]

	# open my id and the one that is in my id box if not my id
	what_i_want = selector_id
	what_i_get = case[what_i_want]
	labels = [selector_id]
	n = len(case)

	# keep following until running out of turns (half of case size)
	while what_i_get != what_i_want and len(labels) < len(case)/2:
		labels.append(what_i_get)
		what_i_get = case[what_i_get]
	return labels

def is_successful(selector_id, selected_labels):
	return selector_id in selected_labels

def evaluate_strategy(n, verbose=False):
	possibilities = list(permutations(range(n)))
	count = []
	for p in possibilities:
		unsuccessful = False
		if verbose: print p
		for selector_id in range(n):
			labels = select(selector_id, p)
			contents = [p[i] for i in labels]
			unsuccessful = not is_successful(selector_id, contents)
			if verbose:
				print '\t prisoner {} got {} when opening labels {}: {}'.format(selector_id, contents, labels, not unsuccessful)
			if unsuccessful:
				break

		if not unsuccessful:
			count.append(p)

	print 'Succesful rate when n={}: {:0.2f}'.format(n, float(len(count)) / len(possibilities))
		# print count
	return count

for n in range(2,12,2):
	evaluate_strategy(n, verbose=False)
# import json
# print json.dumps(res)



