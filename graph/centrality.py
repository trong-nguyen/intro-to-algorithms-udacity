import requests

def get_data(url = 'http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQY69QQDAsSDEF0dGFjaGVkRmlsZRiSrQsM'):
	response = requests.get(url)
	assert response.ok, 'data source for centrality quiz not found'
	data = response.content.split('\n')
	data = [d.split('\t') for d in data]
	data = filter(lambda x: len(x) == 3, data)
	return data

# def get_top_actors(data):
data = get_data()
casting = {}
for actor, movie, year in data:
	movie_name = movie + year
	if actor not in casting:
		casting[actor] = set()
	casting[actor].add(movie_name)

most_popular = sorted([(len(v), k) for k,v in casting.iteritems()], reverse=True)
print 'The 20th most popular is {}'.format(most_popular[20-1])




