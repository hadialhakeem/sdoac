import sys
import time

from dotenv import load_dotenv

from apis.jikan import JikanAPI
from apis.mongodb import MongoAPI

load_dotenv()

if __name__ == "__main__":
    print("Running main...")
    mongo = MongoAPI()
    j = JikanAPI(mongo=mongo)

    max_attempts = 5
    script_retry_delays = [120, 300, 600, 1200]
    for i in range(max_attempts):
        try:
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
            sys.stdout.flush()
            time.sleep(delay)
