from dotenv import load_dotenv
from alpaca import Driver
from check_env import check_env

load_dotenv()


def main():
    check_env(["API_KEY", "SECRET"])
    driver = Driver()
    print(driver.assets())


if __name__ == "__main__":
    main()
