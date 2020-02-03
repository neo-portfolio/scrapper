from neo4j import GraphDatabase
from typing import Dict
import pymongo

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))


def make_query(symbol: str, sd: float, expected_returns: float, beta: float, alpha: float):
    return "MERGE (:Company {symbol: '%s', sd: %f, expected_returns: %f, beta: %f, alpha: %f})" % \
           (symbol, sd, expected_returns, beta, alpha)


def init_neo4j():
    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks  # Nom database
    collection = db.stock
    elems = collection.find()

    with driver.session() as session:
        session.run("CREATE CONSTRAINT ON (c: Company) ASSERT c.symbol IS UNIQUE")
        for elem in elems:
            del elem["_id"]
            del elem["data"]
            query = make_query(**elem)
            print(query)
            session.run(query)


init_neo4j()
