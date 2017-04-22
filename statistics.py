import requests

def most_popular_names(url='http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQY-qsODAsSDEF0dGFjaGVkRmlsZRiskBIM'):
	#change the data source when necessary
	r = requests.get(url)
	assert r.ok, 'Data source not found, try another'

	data = r.content.split()
	names = [d.split(',') for d in data]
	female_names = [ (int(d[2]), d[0]) for d in names if d[1] == 'F']

	female_names = sorted(female_names)

	print 'The second most popular name is', female_names[-2]

from random import randint

def find_median(l):
	def partition(l, vk):
		left = []
		right = []
		for i in l:
			if i > vk:
				left.append(i)
			elif i < vk:
				right.append(i)
		return left, right

	def top_vk(l, rank):
		rk = randint(0, len(l)-1) # randint return in range [0:n] n INCLUSIVE
		vk = l[rk]
		left, right = partition(l, vk)
		# print left, vk, right

		# remedy for duplicates value causing both left and right empty
		k = len(left)
		if k == rank:
			return vk
		elif k > rank:
			if not left:
				return vk
			return top_vk(left, rank)
		else:
			if not right:
				return vk
			return top_vk(right, rank - k - 1)

	m = len(l)/2
	return top_vk(l, m)

# a = [randint(0,1) for i in range(5)]
# print find_median(a)
# print a

def minimize_absolute(L):
    return find_median(L)

from operator import itemgetter
from collections import Counter
def mode(L):
    counts = Counter(L)
    return max([(v,k) for k,v in counts.items()])[1]

print mode(list(range(100)))