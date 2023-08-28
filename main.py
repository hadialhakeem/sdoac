import time

from jikan import JikanAPI
from mongodb import MongoAPI
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("Running main...")
    mongo = MongoAPI()
    j = JikanAPI(mongo=mongo)

    max_attempts = 5
    script_retry_delays = [60, 300, 600, 1200]
    for i in range(max_attempts):
        try:
            j.get_all_characters_fully()
            break
        except Exception as e:
            attempt_num = i + 1
            last_attempt = (attempt_num == max_attempts)
            if last_attempt:
                print(f"Attempt {attempt_num} failed. This was the last attempt, raising error...")
                raise e

            delay = script_retry_delays[i]
            print(f"Attempt {attempt_num} failed, retrying after {delay} seconds")
            print(f"exception: {str(e)}")
            time.sleep(delay)
