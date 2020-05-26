from kafka import KafkaConsumer
import json

def main():
    consumer = KafkaConsumer('test', bootstrap_servers='localhost:9092')
    for msg in consumer:
        #print(msg)
        v = json.loads(msg.value)
        print(v)


if __name__ == "__main__":
    main()
