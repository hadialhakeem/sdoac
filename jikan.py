import time
import requests
import json


class JikanAPI:
    BASE_URL = "https://api.jikan.moe/v4"
    CHARACTER_SEARCH_URL = f"{BASE_URL}/characters"
    REQUEST_DELAY = 3  # Seconds

    DATA_DIR = "data"
    CHARACTERS_LIST_FILE = f"{DATA_DIR}/character_list.json"
    METADATA_FILE = f"{DATA_DIR}/metadata.json"

    def __init__(self):
        with open(self.METADATA_FILE, "r") as jsonFile:
            meta = json.load(jsonFile)
        self.last_page_saved = meta["characters_search"]["last_page_saved"]
        self.last_visible_page = meta["characters_search"]["last_visible_page"]

    def get_all_characters(self):
        for page in range(self.last_page_saved, self.last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            res = self.send_request_and_retry(self.CHARACTER_SEARCH_URL, params)
            res_json = res.json()
            res_characters_list = res_json["data"]
            self.extend_characters_list(res_characters_list)
            self.update_last_saved(page)

            print(f"PAGE {page}/{self.last_visible_page} done")

    def extend_characters_list(self, new_characters_list):
        with open(self.CHARACTERS_LIST_FILE, "r") as jsonFile:
            characters_list = json.load(jsonFile)

        characters_list.extend(new_characters_list)

        with open(self.CHARACTERS_LIST_FILE, "w") as jsonFile:
            json.dump(characters_list, jsonFile)

    def update_last_saved(self, new_last_saved):
        with open(self.METADATA_FILE, "r") as jsonFile:
            metadata = json.load(jsonFile)

        metadata["characters_search"]["last_page_saved"] = new_last_saved

        with open(self.METADATA_FILE, "w") as jsonFile:
            json.dump(metadata, jsonFile)

    def wait_after_request(self):
        time.sleep(self.REQUEST_DELAY)

    @staticmethod
    def send_request_and_retry(url, params):
        res = requests.get(url, params)
        counter = 0
        sleep_intervals = [3, 6, 12, 24]
        while res.status_code != 200 and counter < 3:
            time_to_sleep = sleep_intervals[counter]
            print(f"GOT BAD RESPONSE, RETRY NUM: {counter}")
            print(f"params: {params}")
            print(f"status_code: {res.status_code}")
            print(f"res_json: {res.json()}")
            print(f"waiting {time_to_sleep} seconds before retrying")
            time.sleep(time_to_sleep)
            res = requests.get(url, params)
            counter += 1

        if res.status_code != 200:
            print(f"BAD RESPONSE AFTER ALL RETRIES")
            print(f"params: {params}")
            print(f"status_code: {res.status_code}")
            print(f"res_json: {res.json()}")
            res.raise_for_status()

        return res






