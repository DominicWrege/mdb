#
# Just for playing with reddit api 
#

import praw
import json 
import math
import arrow
import redis
import pickle
import os
from dotenv import load_dotenv

from mdb_reddit.util import get_kafka_producer

def runner():
    print("runn")

def runn(runner):
    runner()


def main():
    # db = redis.Redis(host='127.0.0.1', port=6379, db=0, password="12ingaingainga")
    # # print(type(db))
    # # print(db.dbsize())
    # a = set()
    # db.sadd("tes1", *set(a))
    # print(db.smembers("tes1"))
    # print(pickle.loads(db.get("test")))
    # for key in db.scan_iter("*").items():
    #     print(key)
    # kafka = get_kafka_producer() 
    # kafka.send("telegram", {
    #         "title": "Lotti Test1",
    #         "id": "test.com",
    #         "url": "abc.de",
    #         "score": 2342,
    #         "num_comments": 289,
    #         "created_utc": "2020-06-22T14:08:36+00:00",
    #         "subbredit": "pics",
    #         "subbredit_id": "3h47q",
    # })
    # print("send done")
    # print(arrow.now().format('YYYY-MM-DD HH:mm:ss'))
    # runn(runner)
    aa()
    #reddit.front.top(time_filter="day", limit=10):
    #reddit.front.hot(limit=10):
    #reddit.front.controversial(time_filter="day", limit=10):
    #reddit.front.rising(limit=10)
    for submission in reddit.front.rising(limit=10):
        print("title:", submission.title, "  url:", submission.url)
    #     post_j = json.dumps({"title": submission.title, "url": submission.url})
    #     print(post_j)

def aa():
    load_dotenv()

if __name__ == "__main__":
    main()

    