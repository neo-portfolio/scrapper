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
    mongo_client.drop_database('stocks')
    db = mongo_client.stocks  # Nom database
    collection = db.stock  # Catégorie
    collection.create_index("symbol", unique=True)  # Create Index

    # Load asset names
    assets = driver.assets()

    # S&P data
    sp = driver.daily(["SPY"], 1000)
    sp = [period['c'] for period in sp['SPY']]
    sp = np.array(sp)
    sp = np.diff(np.log(sp))
    sp = sp[1:]
    rm = sp.mean()
    rf = 0.02 ** (1 / 252)
    rp = rm - rf

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
                beta = np.corrcoef(sp, close)[0, 1]
                alpha = r - rf - beta * rp
                query = {"symbol": key, "sd": std, "expected_returns": r, "beta": beta, "alpha": alpha,
                         "data": list(close)}

                if not np.isnan(close).any():

                    try:
                        result = collection.insert(query)  # Do the update
                    except pymongo.errors.BulkWriteError as bwe:
                        print(bwe.details)
                        print("\nAn error occured during import, read the text before for further details")


if __name__ == "__main__":
    main()
