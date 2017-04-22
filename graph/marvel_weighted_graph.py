#
# In lecture, we took the bipartite Marvel graph,
# where edges went between characters and the comics
# books they appeared in, and created a weighted graph
# with edges between characters where the weight was the
# number of comic books in which they both appeared.
#
# In this assignment, determine the weights between
# comic book characters by giving the probability
# that a randomly chosen comic book containing one of
# the characters will also contain the other
#




def add_empty_dict(d, k):
  if k not in d:
    d[k] = {}
  return d


def create_weighted_graph(bipartiteG, characters):
    # 1. create character-character map Ci - Ck for each Mj in marvel
    # 1.1. add score, 1 if not found to each Ci - Ck pair for each Mj
    # 2. create character - movie map
    # 2.2 normalize Ci - Ck map by len(Ci) + len(Ck) from movie map

    WG = {}
    for movie, casting in bipartiteG.iteritems():
        cast = casting.keys()
        for i, ci in enumerate(cast):
            add_empty_dict(WG, ci)
            for ck in cast[i+1:]:
                WG[ci][ck] = WG[ci].get(ck, 0) + 1
                add_empty_dict(WG, ck)
                WG[ck][ci] = WG[ck].get(ci, 0) + 1

            # 2.
            add_empty_dict(bipartiteG, movie)
            bipartiteG[movie][ci] = 1

    # 2.2
    LG = {}
    for chars in bipartiteG.values():
        for character in chars:
            LG[character] = LG.get(character, 0) + 1
    for ci, other_characters in WG.iteritems():
        for ck in other_characters:
            # summed films by each character minus the mutual films
            # ex: played 2 each, same movie once -> 2+2-1 = 3
            # ex: played 1 each, same once -> 1+1-1 = 1
            WG[ci][ck] /= 1.*(LG[ci]+LG[ck]-WG[ci][ck]) 

    return WG

######
#
# Test

def test():
    bipartiteG = {'charA':{'comicB':1, 'comicC':1},
                  'charB':{'comicB':1, 'comicD':1},
                  'charC':{'comicD':1},
                  'comicB':{'charA':1, 'charB':1},
                  'comicC':{'charA':1},
                  'comicD': {'charC':1, 'charB':1}}
    G = create_weighted_graph(bipartiteG, ['charA', 'charB', 'charC'])
    # three comics contain charA or charB
    # charA and charB are together in one of them

    # print json.dumps(G, indent=4)
    assert G['charA']['charB'] == 1.0 / 3
    assert G['charA'].get('charA') == None
    assert G['charA'].get('charC') == None

# from marvel import marvel, characters

import requests, cPickle, json, os

marvel_url = 'http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQYi8cfDAsSDEF0dGFjaGVkRmlsZRjRqSEM'
chars_url = 'http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQYi8cfDAsSDEF0dGFjaGVkRmlsZRi5sSEM'

def get_pickle(url, name):
  if os.path.exists(name):
      return cPickle.load(open(name, 'r'))

  r = requests.get(url)
  assert r.ok, 'Cannot load data from {}'.format(url)
  data = cPickle.loads(r.content)
  cPickle.dump(data, open(name, 'w'))
  return data

marvel = get_pickle(marvel_url, name='marvel')
characters = get_pickle(chars_url, name='characters')

def assert_eps(u, v, eps=1e-6):
    assert abs(u-v) < eps

def test2():
    G = create_weighted_graph(marvel, characters)
    assert_eps(G['HULK/DR. ROBERT BRUC']['DEMOLITION MAN/DENNI'], 0.0344827586207)
    assert_eps(G['HULK/DR. ROBERT BRUC']['VINDICATOR II DOPPEL'], 0.0740740740741)