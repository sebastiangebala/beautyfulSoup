#before using, change the parametr 'termin' for date you are interested in.


import requests
from bs4 import BeautifulSoup

body_link = "http://warszawa.wyborcza.pl/warszawa/0,135838.html?repertoireType=1&showDay="
termin = "22-01-2017"
link_end = "&cinema=&movie=&sortType=4"
link = body_link + termin + link_end
r = requests.get(link)

soup = BeautifulSoup(r.content, 'html.parser')

def get_details():
	details = soup.findAll('tr')
	movies = []
	cinemas = []
	origins = []
	durations = []
	for items in details:
		try:
			movie = items.findAll('p', {'class':'title'})[0].text
			cinema = items.findAll('td')[1].text
			origin = items.findAll('span', {'class':'origin'})[0].text
			duration = items.findAll('span', {'class':'duration'})[0].text
			movies.append(movie)
			cinemas.append(cinema)
			origins.append(origin)
			durations.append(duration)
		except:
			pass
	return movies, cinemas, origins, durations
	#return len(movies), len(cinemas), len(origins), len(durations)

def get_times():
	details = soup.findAll('caption')
	times = []
	for items in details:
		try:
			time = items.findAll('p', {'class':'title'})[0].text
			times.append(time)
		except:
			pass
	return times

def len_details():
	details = soup.findAll('tr')
	movies = []
	for items in details:
		movie = items.findAll('p', {'class':'title'})[0].text
		movies.append(movie)
	return len(movies)

def movie_in_time():
	details = soup.findAll('tbody')
	nums = []
	for item in details:
		movie = item.findAll('tr')
		nums.append(len(movie))
	return nums

def get_time_list():
	final_list = []
	i = 0
	for item in get_times():
		ww = 1
		while movie_in_time()[i] >= ww:
			final_list.append(item)
			ww += 1
		i += 1
	return final_list

def all_details():
	all_list = []
	all_list.append(get_details()[0])
	all_list.append(get_details()[1])
	all_list.append(get_details()[2])
	all_list.append(get_details()[3])
	all_list.append(get_time_list())
	return all_list

def make_pair(i):
	pairs = []
	pairs.append(all_details()[0][i])
	pairs.append(all_details()[1][i])
	pairs.append(all_details()[2][i])
	pairs.append(all_details()[3][i])
	pairs.append(all_details()[4][i])
	return pairs

def src_position(movie_name):
	pairs = []
	i = 0
	for name in all_details()[0]:
		if name.upper() == movie_name.upper():
			return i
		i += 1

#not usefull if we have more than one the same title
#just for searching
def make_pairs_by_name(movie_name):
	pairs = []
	i = src_position(movie_name)
	pairs.append(all_details()[0][i])
	pairs.append(all_details()[1][i])
	pairs.append(all_details()[2][i])
	pairs.append(all_details()[3][i])
	pairs.append(all_details()[4][i])
	return pairs



#danger
#it can crash your pc!
#but it give you full list
#use celery/redis!
def make_pairs():
	pairs = []
	i = 0
	while len_details() > i:
		pairs.append(make_pair(i))
		i += 1
	return pairs
	
