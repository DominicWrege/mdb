import time
import arrow
import json
from pymongo import MongoClient, database
from kafka import KafkaProducer
from kafka import KafkaConsumer
from dotenv import load_dotenv
import praw
import os

broker_url = '127.0.0.1:9092'

def time_now():
    return arrow.now().format('YYYY-MM-DD HH:mm:ss')


def sleep_min(min):
    time.sleep( min * 60 )


def get_reddit_db():
    return MongoClient("mongodb://root:dortmund@127.0.0.1").reddit


def get_kafka_producer():
    return KafkaProducer(bootstrap_servers=broker_url, compression_type="gzip", value_serializer=lambda v: json.dumps(v).encode('utf-8')) 

def get_kafka_consumer(topic):
    return KafkaConsumer(topic, bootstrap_servers=broker_url)

def get_reddit_client():
    load_dotenv()
    return praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                       client_secret=os.getenv("CLIENT_SECRET"),
                       user_agent="praw_python_fhdo_projekt")