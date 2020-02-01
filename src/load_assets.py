import pymongo
from dotenv import load_dotenv
from alpaca import Driver
from check_env import check_env
import os


def main():
    load_dotenv()
    check_env(["API_KEY", "SECRET"])  # Load env variables
    alpaca_driver = Driver()  # Init driver
    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks
    collection = db.stock
    collection.create_index("symbol", unique=True)  # Create Index
    assets = alpaca_driver.assets()  # Fetch assets
    to_insert = [{"symbol": asset, "sd": None, "expected_returns": None,  "data": None} for asset in set(assets)]
    # set to deal with duplications
    try:
        result = collection.insert_many(to_insert)  # Do the import
        print(result.inserted_ids)
    except pymongo.errors.BulkWriteError as bwe:
        print(bwe.details)
        print("\nAn error occured during import, read the text before for further details")


if __name__ == "__main__":
    main()
