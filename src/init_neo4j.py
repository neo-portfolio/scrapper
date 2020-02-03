from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()


driver = GraphDatabase.driver("bolt://%s:7687" % os.getenv("NEO_URL"), encrypted=False)


def make_query(symbol: str, sd: float, expected_returns: float, beta: float, alpha: float):
    return "MERGE (:Company {symbol: '%s', sd: %f, expected_returns: %f, beta: %f, alpha: %f})" % \
           (symbol, sd, expected_returns, beta, alpha)


def init_neo4j():
    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks  # Nom database
    collection = db.stock
    elems = collection.find()

    with driver.session() as session:
        try:
            session.run("CREATE CONSTRAINT ON (c: Company) ASSERT c.symbol IS UNIQUE")
        except:
            pass
        for elem in elems:
            del elem["_id"]
            del elem["data"]
            query = make_query(**elem)
            print(query)
            session.run(query)


init_neo4j()
