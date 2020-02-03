#!/usr/bin/env python
import pika
import os
from dotenv import load_dotenv
from check_env import check_env
import pymongo
from typing import List


def register_channel(channel):
    def push_message(s1, s2):
        channel.basic_publish(exchange='', routing_key='stocks', body='%s,%s' % (s1, s2))

    return push_message


def get_assets() -> List[str]:
    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks  # Nom database
    collection = db.stock  # Catégorie
    return [item["symbol"] for item in collection.find({}, {"symbol": 1})]


def feed_queue(channel):
    channel.queue_declare(queue='stocks', durable=True)
    push_message = register_channel(channel)
    stocks = get_assets()
    length = len(stocks)
    for i in range(length):
        for j in range(i + 1, length):
            push_message(stocks[i], stocks[j])


def main():
    load_dotenv()
    check_env(["API_KEY", "SECRET", "QUEUE_URL", "MONGO_URL", "NEO_URL"])
    credentials = pika.PlainCredentials('admin', 'test1234')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("QUEUE_URL"), credentials=credentials))
    channel = connection.channel()
    feed_queue(channel)

    connection.close()


if __name__ == "__main__":
    main()
