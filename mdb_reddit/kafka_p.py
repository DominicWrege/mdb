from kafka import KafkaProducer

import json
import time
import praw
from typing import List
from praw import Reddit
import json 

#https://pypi.org/project/arrow/

def reddit_client() -> str:
    return praw.Reddit(client_id="ZuAQ4z82JQDngA",
                       client_secret="yzTKHSRGbl0O8ROCq2oi1gnX8vA",
                       user_agent="python_i_guess")


def front_page_top(client: Reddit) -> List[any]:
    posts: List = []
    for submission in client.front.top(time_filter="day", limit=50):
        post_j = {
                "title": submission.title,
                "url": submission.url, 
                "id": submission.id, 
                "score": submission.score,
                "num_comments" :submission.num_comments,
                "created_utc": submission.created_utc
            }
        posts.append(post_j)
    return posts


def send_posts_to_kafka(client: Reddit):
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        #t = time.gmtime()
    for p in front_page_top(client):
        producer.send("top_posts", p)

def main():
    while True:
        print("fetching every 1 min")
        client: Reddit = reddit_client()
        send_posts_to_kafka(client)
        time.sleep(60 * 10 ) # 10 min

if __name__ == "__main__":
    main()
