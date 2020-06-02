from kafka import KafkaConsumer
import json
import pprint
from pymongo import MongoClient

 
def connect_mongodb():
    return MongoClient("mongodb://root:test@localhost").reddit


def main():
    consumer = KafkaConsumer('top_posts', bootstrap_servers='localhost:9092')
    print("waiting")
    db = connect_mongodb()
    db_posts = db.posts

    for msg in consumer:
        #print(msg)        
        
        pp = pprint.PrettyPrinter(indent=4)
        v = json.loads(msg.value.decode("UTF-8"))
        print("<------------------new post------------------------>")
        pp.pprint(v)
        db_posts.insert(v)


if __name__ == "__main__":
    main()
