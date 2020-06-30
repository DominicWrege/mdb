import json
import pprint
import threading
from pymongo import MongoClient, database
import logging
import sys
from mdb_reddit.util import get_reddit_db, get_kafka_consumer
class Setup:
    def __init__(self, topic, collection):
        # logging.basicConfig(level=logging.INFO)
        self.topic = topic
        self.collection = collection
        self.kafka = get_kafka_consumer(topic)
        self.mongodb = get_reddit_db()
        self.pp = pprint.PrettyPrinter(indent=4)


def kafka_listener(topic_name, collection):
    setup = Setup(topic_name, collection)
    db_posts = setup.mongodb[setup.collection] #setup.mongodb.top_posts 
    pp = setup.pp
    pp.pprint("waiting for kafka messages...")
    pp.pprint(f"topic_name: {topic_name}")
    for msg in setup.kafka:
        post = json.loads(msg.value.decode("UTF-8"))
        if db_posts.find_one({ "id": post["id"] }) == None: # for dups
            db_posts.insert(post)
            # pp.pprint("<------------------new post------------------------>")
            # pp.pprint(post)

def new_thread(topic_name, collection_name):
    threading.Thread(target=kafka_listener, args=([topic_name, collection_name])).start()

###---------####

# p_hot_posts
# p_top_posts
# p_rising_posts
# p_controversial_posts

###--------#######

def main():
    try:
        new_thread(topic_name="p_hot_posts", collection_name="hot_posts")
        new_thread(topic_name="p_top_posts", collection_name="top_posts")
        new_thread(topic_name="p_rising_posts", collection_name="rising_posts")
        new_thread(topic_name="p_controversial_posts", collection_name="controversial_posts")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e, file=sys.stderr)
if __name__ == "__main__":
    main()

# TODO create collection if not exists
