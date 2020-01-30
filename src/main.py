from dotenv import load_dotenv
from alpaca import Driver
from check_env import check_env

load_dotenv()


def main():
    check_env(["API_KEY", "SECRET"])
    driver = Driver()
    stocks = ["AAPL", "MSFT"]
    print(driver.daily(stocks))


if __name__ == "__main__":
    main()
