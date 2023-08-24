from jikan import JikanAPI
from mongodb import MongoAPI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Running main...")
    m = MongoAPI()
    j = JikanAPI(mongo=m)
    # j.run_print()
    j.get_all_characters()

