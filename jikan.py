import time
import requests
import json
import sys

from mongodb import MongoAPI


class JikanAPI:
    BASE_URL = "https://api.jikan.moe/v4"
    CHARACTER_SEARCH_URL = f"{BASE_URL}/characters"
    REQUEST_DELAY = 3  # Seconds

    DATA_DIR = "data"
    METADATA_FILE = f"{DATA_DIR}/metadata.json"

    def __init__(self, mongo: MongoAPI):
        self.mongo = mongo

        with open(self.METADATA_FILE, "r") as jsonFile:
            meta = json.load(jsonFile)
        self.last_page_saved = meta["characters_search"]["last_page_saved"]
        self.last_visible_page = meta["characters_search"]["last_visible_page"]

    def get_all_characters(self):
        self._log("COMMENCING GETTING ALL CHARACTERS")
        for page in range(self.last_page_saved + 1, self.last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            self._log(f"sending request for page: {page}")
            res = self.send_request_and_retry(self.CHARACTER_SEARCH_URL, params)
            res_json = res.json()
            res_character_list = res_json["data"]
            self.extend_character_list(res_character_list)
            self.update_last_saved(page)

            self._log(f"{page}/{self.last_visible_page} pages done")
            self._log("============================================")

    def extend_character_list(self, new_character_list):
        self.mongo.insert_character_list(new_character_list)

    def update_last_saved(self, new_last_saved):
        with open(self.METADATA_FILE, "r",  encoding='utf8') as jsonFile:
            metadata = json.load(jsonFile)

        metadata["characters_search"]["last_page_saved"] = new_last_saved

        with open(self.METADATA_FILE, "w",  encoding='utf8') as jsonFile:
            json.dump(metadata, jsonFile, indent=4, ensure_ascii=False)

    def wait_after_request(self):
        time.sleep(self.REQUEST_DELAY)

    def send_request_and_retry(self, url, params):
        res = requests.get(url, params)
        counter = 0
        sleep_intervals = [3, 6, 12, 24]
        while res.status_code != 200 and counter < 3:
            time_to_sleep = sleep_intervals[counter]
            self._log(f"GOT BAD RESPONSE, RETRY NUM: {counter}")
            self._log(f"params: {params}")
            self._log(f"status_code: {res.status_code}")
            self._log(f"res_json: {res.json()}")
            self._log(f"waiting {time_to_sleep} seconds before retrying")
            time.sleep(time_to_sleep)
            res = requests.get(url, params)
            counter += 1

        if res.status_code != 200:
            self._log(f"BAD RESPONSE AFTER ALL RETRIES")
            self._log(f"params: {params}")
            self._log(f"status_code: {res.status_code}")
            self._log(f"res_json: {res.json()}")
            res.raise_for_status()

        return res

    @staticmethod
    def _log(arg):
        print(arg)
        sys.stdout.flush()




