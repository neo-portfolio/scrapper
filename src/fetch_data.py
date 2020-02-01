from dotenv import load_dotenv
from alpaca import Driver
from check_env import check_env

import numpy as np

# Connection
load_dotenv()
check_env(["API_KEY", "SECRET"])
driver = Driver()

# Load asset names
assets = driver.assets()

nb_request = 200
for i in range(0, len(assets), nb_request):
    data = driver.daily(assets[i:i+nb_request], 1000)

    for key in data.keys():
        stock = data[key]

        if len(stock) == 1000:
            close = []

            for period in stock:
                close.append(period['c'])

            close = np.array(close)
            r = close.mean()
            std = close.std()
            print(close,"  ",r,"   ",std)