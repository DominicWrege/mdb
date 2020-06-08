from kafka import KafkaConsumer
import json
import pprint
from pymongo import MongoClient, database

class Setup:
    def __init__(self):
        self.kafka = KafkaConsumer('top_posts', bootstrap_servers='localhost:9092') 
        self.mongodb = MongoClient("mongodb://root:test@localhost").reddit
        self.pp = pprint.PrettyPrinter(indent=4)

def main():
    setup = Setup()
    print("waiting")
    db_posts = setup.mongodb.posts
    pp = setup.pp
    for msg in setup.kafka:
        #print(msg)
        post = json.loads(msg.value.decode("UTF-8"))
        if db_posts.find_one({ "id": post["id"] }) == None: # for dups
            db_posts.insert(post)
            print("<------------------new post------------------------>")
            pp.pprint(post)
        else:
            db_posts.find_one_and_update(
                    { "id": post["id"] },
                    { "$set":  
                        { "score": post["score"],  "num_comments": post["num_comments"] }
                    }
                )
if __name__ == "__main__":
    main()


