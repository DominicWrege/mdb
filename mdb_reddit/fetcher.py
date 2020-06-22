from kafka import KafkaProducer
import arrow
import json
import time
import praw
from typing import List
from praw import Reddit
import json
import logging
import pprint
import sys
from mdb_reddit.util import time_now, sleep_min

###---------####

# p_hot_posts
# p_rising_posts
# p_controversial_posts
# p_top_posts

###--------#######


#https://pypi.org/project/arrow/

def reddit_client():
    return praw.Reddit(client_id="ZuAQ4z82JQDngA",
                       client_secret="yzTKHSRGbl0O8ROCq2oi1gnX8vA",
                       user_agent="praw_python_fhdo_projekt")


# fetcher type
# client.front.top(time_filter="day", limit=250):
# client.front.hot(limit=10):
# client.front.controversial(time_filter="day", limit=10):
# client.front.rising(limit=10)

def fetch_from_reddit(fetcher, name):
    print(f"{time_now()} fetching {name} posts")   
    posts = front_page(fetcher)
    send_posts_to_kafka(posts, name)
    time.sleep(3)
    print("delay for 3sec")


def front_page(fetcher) -> List[any]:
    posts: List = []
    for post in fetcher:
        if post.author is None:
            author_fullname = None
        else:
            author_fullname = post.author.name
        post_j = {
                "title": post.title,
                "url": post.url, 
                "id": post.id, 
                "score": post.score,
                "num_comments" :post.num_comments,
                "created_utc": arrow.get(post.created_utc).isoformat(),
                "subbredit": post.subreddit.display_name,
                "subbredit_id": post.subreddit.id,
                "over_18": post.over_18,
                "is_video": post.is_video,
                "upvote_ratio": post.upvote_ratio,
                "author_fullname" : author_fullname,
                "subreddit_subcribers"  : post.subreddit.subscribers 
            }
        posts.append(post_j)
    return posts


def send_posts_to_kafka(list_posts, topic_name):
    producer = KafkaProducer(bootstrap_servers='127.0.0.1:9092', compression_type="gzip",
                value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    for p in list_posts:
        producer.send(f"p_{topic_name}_posts", p)

def all_fetching(interval, posts_limit, client):
    #client.front.top(time_filter="day", limit=250):
    fetch_from_reddit(client.front.top(time_filter="day", limit=posts_limit), name="top")
    fetch_from_reddit(client.front.hot(limit=posts_limit), name="hot")
    fetch_from_reddit(client.front.controversial(time_filter="day", limit=posts_limit), name="controversial")
    fetch_from_reddit(client.front.rising(limit=posts_limit), name="rising")
    print(f"{time_now()}  now sleeping {interval}min")
    sleep_min(interval)

def main():
    interval = 40 # in min
    posts_limit = 250
    # logging.basicConfig(level=logging.INFO)
    client = reddit_client()
    print(f"{time_now()} fechting every {interval} min, posts_limit {posts_limit}")
    while True:
        try:
            all_fetching(interval, posts_limit, client)
        except KeyboardInterrupt:
           exit()
        except Exception as e:
           print(time_now(), "Exception with the broker or reddit is down", file=sys.stderr)
           print(e, file=sys.stderr)
if __name__ == "__main__":
    main()
