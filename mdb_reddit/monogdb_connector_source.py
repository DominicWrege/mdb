
import threading
import time
import json
import pdb
import sys
from mdb_reddit.util import get_reddit_db, get_kafka_producer
# https://docs.mongodb.com/manual/reference/method/db.watch/
# https://api.mongodb.com/python/current/api/pymongo/change_stream.html
# https://docs.mongodb.com/manual/tutorial/deploy-replica-set/

sleep_time = 3

# waits for db insert and posts it to kafka
def run(collection_name, topic):
    posts_colllection = get_reddit_db()[collection_name]
    kafka = get_kafka_producer() 
    pipeline = [{'$match': {'operationType': 'insert'}}]
    while True:
        with posts_colllection.watch(pipeline) as stream:
            for insert_change in stream:
                    value = insert_change["fullDocument"] 
                    del value["_id"]
                    kafka.send(topic, value)
                    kafka.send("telegram", value)
        time.sleep(sleep_time)
        print(f"sleep for {sleep_time} sec")
            
def new_listener(collection_name):
    print(f"listening for collection: {collection_name}")
    topic=collection_name
    threading.Thread(target=run, args=([collection_name, topic])).start()


###---------####

# hot_posts
# risincposts
# controversial_posts
# top_posts

###--------#######

def main():
    try:
        print("mongodb source connector started:")
        new_listener("top_posts")
        new_listener("rising_posts")
        new_listener("controversial_posts")
        new_listener("hot_posts")
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == "__main__":
    main()
    
