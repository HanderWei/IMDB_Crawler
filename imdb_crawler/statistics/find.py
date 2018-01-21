import pymongo
from pymongo import MongoClient
import operator

client = MongoClient('localhost', 27017)
db = client['imdb']
top250 = db['top250']
output_path = "chart/"


def find_year_rank(year):
    movies = top250.find({"year": year})
    if movies.count() > 0:
        print("There are %d movie in %d" % (movies.count(), year))
        rank = 0
        for movie in movies:
            print(movie['title'])
            rank += movie['rank']
        print("%d on average." % float(rank / movies.count()))
        return float(rank / movies.count())
    else:
        return None


def find_year_count(year):
    return top250.find({"year": year}).count()


def find_all_year():
    all_year_dict = {}
    for year in range(1920, 2018):
        rank = find_year_rank(year)
        if rank is not None:
            all_year_dict[year] = rank
    sorted_dict = dict(sorted(all_year_dict.items(), key=operator.itemgetter(1)))
    for year, rank in sorted_dict.items():
        print("Year:%d \t Average Rank:%.1f \t Movies Count:%d" % (year, rank, find_year_count(year)))


find_all_year()
