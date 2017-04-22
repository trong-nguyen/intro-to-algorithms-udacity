# -*- coding: utf-8 -*-

import requests
from dijkstra import dijkstra

def get_newline_3tab_delimited_data(url):
  response = requests.get(url)
  assert response.ok, 'cannot get data from {}'.format(url)
  data = response.content
  data = data.decode('utf-8')
  data = data.split('\n')
  data = filter(bool, data)
  data = map(lambda d: d.split('\t'), data)
  return data

def make_actor_graph(casting, obscurity):
  # 1. make full_movie_name 
  casting = [(actor, movie + year) for actor, movie, year in casting]
  obscurity = {movie + year: score for movie, year, score in obscurity}

  # 2. make [actors] - [movies] connectivities
  ''' 
  actor_movies = {
    david: {
      bond: 0.3,
      avengers: 1.9,
    },
    cumberbatch: {
      starwars: 9.2,
      kong: 3.1
    }
  }
  movie_actors = {
    avengers: [hawk, robert, green],
    kong: [xiexie, middleton]
  }
  '''
  actor_movies = {}
  movie_actors = {}
  for actor, movie in casting:
    if actor not in actor_movies:
      actor_movies[actor] = {}
    actor_movies[actor][movie] = obscurity[movie]
    if movie not in movie_actors:
      movie_actors[movie] = []
    movie_actors[movie].append(actor)

  # 3. make actor actor connectivities with scores
  '''
  actor_movies = {
    david: {
      middleton: 0.3,
      junior: 1.9,
      downney: 3.2
    },
    cumberbatch: {
      david: 9.2,
      downey: 3.1
    }
  }

  '''
  actor_graph = {}
  for actor, mvs in actor_movies.items():
    actor_graph[actor] = {}
    for movie, score in mvs.items():
      score = float(score) # conversion
      for other_actor in movie_actors[movie]:
        if other_actor == actor:
          continue
        actor_graph[actor][other_actor] = score
        if other_actor not in actor_graph:
          actor_graph[other_actor] = {}
        actor_graph[other_actor][actor] = score # 2 way

  return actor_graph

def test_weighted_bacon_game():
  #
  # Another way of thinking of a path in the Kevin Bacon game 
  # is not about finding *short* paths, but by finding paths 
  # that don't use obscure movies.  We will give you a 
  # list of movies along with their obscureness score.  
  #
  # For this assignment, we'll approximate obscurity 
  # based on the multiplicative inverse of the amount of 
  # money the movie made.  Though, its not really important where
  # the obscurity score came from.
  #
  # Use the the imdb-1.tsv and imdb-weights.tsv files to find
  # the obscurity of the "least obscure"
  # path from a given actor to another.  
  # The obscurity of a path is the maximum obscurity of 
  # any of the movies used along the path.
  #
  # You will have to do the processing in your local environment
  # and then copy in your answer.
  #
  # Hint: A variation of Dijkstra can be used to solve this problem.
  #

  # Change the `None` values in this dictionary to be the obscurity score
  # of the least obscure path between the two actors
  answer_set = {(u'Boone Junior, Mark', u'Del Toro, Benicio'): None,
            (u'Braine, Richard', u'Coogan, Will'): None,
            (u'Byrne, Michael (I)', u'Quinn, Al (I)'): None,
            (u'Cartwright, Veronica', u'Edelstein, Lisa'): None,
            (u'Curry, Jon (II)', u'Wise, Ray (I)'): None,
            (u'Di Benedetto, John', u'Hallgrey, Johnathan'): None,
            (u'Hochendoner, Jeff', u'Cross, Kendall'): None,
            (u'Izquierdo, Ty', u'Kimball, Donna'): None,
            (u'Jace, Michael', u'Snell, Don'): None,
            (u'James, Charity', u'Tuerpe, Paul'): None,
            (u'Kay, Dominic Scott', u'Cathey, Reg E.'): None,
            (u'McCabe, Richard', u'Washington, Denzel'): None,
            (u'Reid, Kevin (I)', u'Affleck, Rab'): None,
            (u'Reid, R.D.', u'Boston, David (IV)'): None,
            (u'Restivo, Steve', u'Preston, Carrie (I)'): None,
            (u'Rodriguez, Ramon (II)', u'Mulrooney, Kelsey'): None,
            (u'Rooker, Michael (I)', u'Grady, Kevin (I)'): None,
            (u'Ruscoe, Alan', u'Thornton, Cooper'): None,
            (u'Sloan, Tina', u'Dever, James D.'): None,
            (u'Wasserman, Jerry', u'Sizemore, Tom'): None}

  # Here are some test cases.
  # For example, the obscurity score of the least obscure path
  # between 'Ali, Tony' and 'Allen, Woody' is 0.5657
  test_set = {(u'Ali, Tony', u'Allen, Woody'): 0.5657,
          (u'Auberjonois, Rene', u'MacInnes, Angus'): 0.0814,
          (u'Avery, Shondrella', u'Dorsey, Kimberly (I)'): 0.7837,
          (u'Bollo, Lou', u'Jeremy, Ron'): 0.4763,
          (u'Byrne, P.J.', u'Clarke, Larry'): 0.109,
          (u'Couturier, Sandra-Jessica', u'Jean-Louis, Jimmy'): 0.3649,
          (u'Crawford, Eve (I)', u'Cutler, Tom'): 0.2052,
          (u'Flemyng, Jason', u'Newman, Laraine'): 0.139,
          (u'French, Dawn', u'Smallwood, Tucker'): 0.2979,
          (u'Gunton, Bob', u'Nagra, Joti'): 0.2136,
          (u'Hoffman, Jake (I)', u'Shook, Carol'): 0.6073,
          (u'Kamiki, Ryûnosuke', u'Thor, Cameron'): 0.3644,
          (u'Roache, Linus', u'Dreyfuss, Richard'): 0.6731,
          (u'Sanchez, Phillip (I)', u'Wiest, Dianne'): 0.5083,
          (u'Sheppard, William Morgan', u'Crook, Mackenzie'): 0.0849,
          (u'Stan, Sebastian', u'Malahide, Patrick'): 0.2857,
          (u'Tessiero, Michael A.', u'Molen, Gerald R.'): 0.2056,
          (u'Thomas, Ken (I)', u'Bell, Jamie (I)'): 0.3941,
          (u'Thompson, Sophie (I)', u'Foley, Dave (I)'): 0.1095,
          (u'Tzur, Mira', u'Heston, Charlton'): 0.3642}


  imdb_url = 'http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQY69QQDAsSDEF0dGFjaGVkRmlsZRiSrQsM'
  imdb_weights_url = 'http://www.udacity.com/file?file_key=agpzfnVkYWNpdHl1ckALEgZDb3Vyc2UiBWNzMjE1DAsSCUNvdXJzZVJldhgBDAsSBFVuaXQYyY4dDAsSDEF0dGFjaGVkRmlsZRjprR0M'

  casting = get_newline_3tab_delimited_data(imdb_url)
  obscurity = get_newline_3tab_delimited_data(imdb_weights_url)

  graph = make_actor_graph(casting, obscurity)

  for (a1, a2), test_score in test_set.items():
    _, score = dijkstra(graph, a1, a2, accumulate_rule=max)
    assert score == test_score

  # for (a1, a2), _ in answer_set.items():
  #   _, score = dijkstra(graph, a1, a2, accumulate_rule=max)
  #   answer_set[(a1, a2)] = score
  # return answer_set