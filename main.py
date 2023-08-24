from jikan import JikanAPI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Running main...")
    j = JikanAPI()
    j.run_print()
    # j.get_all_characters()

