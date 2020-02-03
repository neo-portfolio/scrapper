#!/usr/bin/env python
import pika
import os
from dotenv import load_dotenv
from check_env import check_env
import numpy as np
import pymongo
from neo4j import GraphDatabase
from feed_queue import get_assets


class Worker:
    __memo = {}
    __assets = get_assets()

    def __init__(self):
        mongo_client = pymongo.MongoClient(os.getenv("MONGO_URL"), 27017)  # Connect to MongoDB
        db = mongo_client.stocks  # Nom database
        self.__collection = db.stock  # Catégorie
        self.__driver = GraphDatabase.driver("bolt://%s:7687" % os.getenv("NEO_URL"))
        credentials = pika.PlainCredentials('admin', 'test1234')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv("QUEUE_URL"), credentials=credentials))
        self.__channel = connection.channel()
        self.__channel.queue_declare(queue='stocks', durable=True)
        self.__channel.basic_qos(prefetch_count=1)
        self.__consumer_tag = self.__channel.basic_consume(queue='stocks', on_message_callback=self.__callback)

    def start(self):
        try:
            self.__channel.start_consuming()
        except KeyboardInterrupt:
            self.__channel.stop_consuming()
        self.__channel.close()

    def __callback(self, channel, method, properties, body):
        symbol1, symbol2 = body.decode("utf-8").split(",")
        stock1, stock2 = self.__get(symbol1), self.__get(symbol2)
        correl = np.corrcoef(stock1, stock2)[0, 1]
        query = self.make_query(symbol1, symbol2, correl)
        print(query)
        with self.__driver.session() as session:
            session.run(query)
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def __get(self, ticker: str):
        if ticker in self.__memo:
            return self.__memo[ticker]
        else:
            stock = np.array(self.__collection.find_one({"symbol": ticker})["data"])
            self.__memo[ticker] = stock
            return stock

    @staticmethod
    def make_query(symbol1, symbol2, corr12):
        return "MATCH (a:Company {name: '%s'}), (b:Company {name: '%s'})\
        CREATE (a)-[:Correlated {corr: %d}]->(b)" % (symbol1, symbol2, corr12)


def main():
    load_dotenv()
    check_env(["API_KEY", "SECRET", "QUEUE_URL", "MONGO_URL", "NEO_URL"])
    worker = Worker()
    worker.start()


if __name__ == "__main__":
    main()
