import pymongo
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client['imdb']
top250 = db['top250']


def dropDups():
    """删除重复item"""
    dup_count = 0
    for i in range(1, 251):
        if top250.find({"rank": str(i)}).count() > 1:
            top250.delete_one({"rank": str(i)})
        if top250.find({"rank": str(i)}).count() < 1:
            print("Not found Rank: %d" % i)

    print("Dup Count: %d" % dup_count)
    print("Now count: %d" % top250.count())


dropDups()
