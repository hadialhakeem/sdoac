from dotenv import load_dotenv
from apis.mongodb import MongoAPI
from apis.neo import NeoAPI

load_dotenv()


if __name__ == "__main__":
    mongo = MongoAPI()
    neo = NeoAPI()

    # do stuff

    neo.close()

