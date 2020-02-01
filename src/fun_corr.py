import numpy as np
import pymongo


def corr(ticker1: str, ticker2: str):
    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks  # Nom database
    collection = db.stock  # Catégorie

    stock1 = collection.find_one({"symbol": ticker1})
    stock2 = collection.find_one({"symbol": ticker2})

    r1 = np.array(stock1["data"])
    r2 = np.array(stock2["data"])
    return float(np.corrcoef(r1, r2)[0, 1])