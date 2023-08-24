from jikan import JikanAPI
from mongodb import MongoAPI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Running main...")
    mongo = MongoAPI()
    j = JikanAPI(mongo=mongo)
    j.get_all_characters()
