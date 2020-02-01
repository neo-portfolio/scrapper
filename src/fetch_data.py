from dotenv import load_dotenv
from alpaca import Driver
from check_env import check_env

import numpy as np
import pymongo


def main():
    # Connection
    load_dotenv()
    check_env(["API_KEY", "SECRET"])
    driver = Driver()

    mongo_client = pymongo.MongoClient("localhost", 27017)  # Connect to MongoDB
    db = mongo_client.stocks  # Nom database
    collection = db.stock  # Catégorie

    # Load asset names
    assets = driver.assets()

    nb_request = 200
    for i in range(0, len(assets), nb_request):
        data = driver.daily(assets[i:i + nb_request], 1000)

        for key in data.keys():
            stock = data[key]

            if len(stock) == 1000:
                close = [period['c'] for period in stock]
                close = np.array(close)
                close = np.diff(np.log(close))
                close = close[1:]
                r = close.mean()
                std = close.std()
                query = {"symbol": key}
                update = {'$set': {"sd": std, "expected_returns": r, "data": list(close)}}

                if np.isnan(close).any():
                    try:
                        result = collection.delete_one(query)  # Delete none data stocks
                    except pymongo.errors.BulkWriteError as bwe:
                        print(bwe.details)
                        print("\nAn error occured during import, read the text before for further details")

                else:
                    try:
                        result = collection.update_one(query, update)  # Do the update
                    except pymongo.errors.BulkWriteError as bwe:
                        print(bwe.details)
                        print("\nAn error occured during import, read the text before for further details")

            else:
                query = {"symbol": key}
                try:
                    result = collection.delete_one(query)  # Delete none data stocks
                except pymongo.errors.BulkWriteError as bwe:
                    print(bwe.details)
                    print("\nAn error occured during import, read the text before for further details")


if __name__ == "__main__":
    main()
