from dotenv import load_dotenv
from check_env import check_env
import pika

load_dotenv()


def main():
    check_env(["API_KEY", "SECRET"])
    


if __name__ == "__main__":
    main()
