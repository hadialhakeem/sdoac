import time
import requests
import json
import sys

from apis.mongodb import MongoAPI


class JikanAPI:
    BASE_URL = "https://api.jikan.moe/v4"
    CHARACTER_SEARCH_URL = f"{BASE_URL}/characters"
    CHARACTER_FULL_DETAILS_URL = BASE_URL + "/characters/{id}/full"
    PERSON_SEARCH_URL = BASE_URL + "/people"
    PERSON_DETAILS_URL = BASE_URL + "/people/{}"
    ANIME_SEARCH_URL = BASE_URL + "/anime"

    REQUEST_DELAY = 2  # Seconds

    METADATA_FILE = f"data/metadata.json"

    def __init__(self, mongo: MongoAPI):
        self.mongo = mongo

        with open(self.METADATA_FILE, "r") as jsonFile:
            meta = json.load(jsonFile)
        self.meta = meta
        self.last_page_saved = meta["characters_search"]["last_page_saved"]
        self.last_visible_page = meta["characters_search"]["last_visible_page"]
        self.list_only_ids = meta["list_only_ids"]

    def get_all_characters(self):
        self._log("COMMENCING get_all_characters")
        for page in range(self.last_page_saved + 1, self.last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            self._log(f"sending request for page: {page}")
            res = self.send_request_and_retry(self.CHARACTER_SEARCH_URL, True, params)
            res_json = res.json()
            res_character_list = res_json["data"]
            self.mongo.insert_character_list(res_character_list)
            self.update_last_saved(page, "characters_search")

            self._log(f"{page}/{self.last_visible_page} pages done")
            self._log("============================================")

    def get_all_characters_fully(self):
        self._log("COMMENCING get_all_characters_fully")

        characters_incomplete = self.mongo.get_character_list_after_last_full_inserted()
        counter = 0
        for character in characters_incomplete:
            mal_id = character["mal_id"]
            if mal_id in self.list_only_ids:
                continue
            self.get_character_full(mal_id)
            counter += 1
            self._log(f"Character #{counter} inserted.")
            self._log("============================================")
            self.wait_after_request()

    def get_character_full(self, character_mal_id):
        self._log(f"get_character for id: {character_mal_id}")

        req_url = self.CHARACTER_FULL_DETAILS_URL.format(id=character_mal_id)
        res = self.send_request_and_retry(req_url, False)
        res_json = res.json()

        if res.status_code == 404 and res_json["type"] == "BadResponseException" and \
                res_json["message"] == "Resource does not exist":
            self._log(f"Character id {character_mal_id} does not exist on mal. Skipping.")
            self.add_list_only_id(character_mal_id)
            return

        res.raise_for_status()

        if "data" not in res_json:
            self._log(f"res_json:{res_json}")
        character_data = res_json["data"]
        self.mongo.insert_character_full(character_data)

        self._log(f"Character id:{character_mal_id} retrieved.")

    def get_person_details(self, person_mal_id):
        self._log(f"Get person for id: {person_mal_id}")

        req_url = self.PERSON_DETAILS_URL.format(person_mal_id)
        res = self.send_request_and_retry(req_url, False)
        res_json = res.json()

        if res.status_code == 404 and res_json["type"] == "BadResponseException" and \
                res_json["message"] == "Resource does not exist":
            self._log(f"person id {person_mal_id} does not exist on mal. Skipping.")
            return

        res.raise_for_status()

        if "data" not in res_json:
            self._log(f"res_json:{res_json}")
        person_data = res_json["data"]
        self.mongo.insert_persons([person_data])

        self._log(f"person id:{person_mal_id} retrieved.")

    def get_all_persons(self):
        self._log("COMMENCING get_all_persons")

        last_page_saved = self.meta["person_search"]["last_page_saved"]
        last_visible_page = self.meta["person_search"]["last_visible_page"]

        for page in range(last_page_saved + 1, last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            self._log(f"sending request for page: {page}")
            res = self.send_request_and_retry(self.PERSON_SEARCH_URL, True, params)
            res_json = res.json()
            res_person_list = res_json["data"]

            self.mongo.insert_persons(res_person_list)
            self.update_last_saved(page, "person_search")

            self._log(f"{page}/{last_visible_page} pages done")
            self._log("============================================")

    def get_all_anime(self):
        self._log("COMMENCING get_all_anime")

        last_page_saved = self.meta["anime_search"]["last_page_saved"]
        last_visible_page = self.meta["anime_search"]["last_visible_page"]

        for page in range(last_page_saved + 1, last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            self._log(f"sending request for page: {page}")
            res = self.send_request_and_retry(self.ANIME_SEARCH_URL, True, params)
            res_json = res.json()
            res_anime_list = res_json["data"]

            self.mongo.insert_animes(res_anime_list)
            self.update_last_saved(page, "anime_search")

            self._log(f"{page}/{last_visible_page} pages done")
            self._log("============================================")

    def update_last_saved(self, new_last_saved, namespace):
        with open(self.METADATA_FILE, "r", encoding='utf8') as jsonFile:
            metadata = json.load(jsonFile)

        metadata[namespace]["last_page_saved"] = new_last_saved

        with open(self.METADATA_FILE, "w", encoding='utf8') as jsonFile:
            json.dump(metadata, jsonFile, indent=4, ensure_ascii=False)

    def add_list_only_id(self, new_id):
        with open(self.METADATA_FILE, "r", encoding='utf8') as jsonFile:
            metadata = json.load(jsonFile)

        metadata["list_only_ids"].append(new_id)

        with open(self.METADATA_FILE, "w", encoding='utf8') as jsonFile:
            json.dump(metadata, jsonFile, indent=4, ensure_ascii=False)

    def wait_after_request(self):
        time.sleep(self.REQUEST_DELAY)

    def send_request_and_retry(self, url, raise_exception, *args):
        res = requests.get(url, *args)
        counter = 0
        sleep_intervals = [3, 6, 12, 24]

        while res.status_code != 200 and counter < 3:
            try:
                res_json = res.json()
            except Exception:
                res_json = None
            time_to_sleep = sleep_intervals[counter]
            self._log(f"GOT BAD RESPONSE, RETRY NUM: {counter}")
            self._log(f"args: {args}")
            self._log(f"status_code: {res.status_code}")
            self._log(f"res: {res}")
            self._log(f"res_json: {res_json}")
            self._log(f"waiting {time_to_sleep} seconds before retrying")
            time.sleep(time_to_sleep)
            res = requests.get(url, *args)
            counter += 1

        try:
            res_json = res.json()
        except Exception:
            res_json = None
        if res.status_code != 200:
            self._log(f"BAD RESPONSE AFTER ALL RETRIES")
            self._log(f"args: {args}")
            self._log(f"status_code: {res.status_code}")
            self._log(f"res: {res}")
            self._log(f"res_json: {res_json}")
            if raise_exception:
                res.raise_for_status()

        return res

    def get_persons_from_id_list(self, p_id_list):
        counter = 0
        for p_id in p_id_list:
            self.get_person_details(p_id)
            counter += 1
            self._log(f"Person #{counter} inserted.")
            self._log("============================================")
            self.wait_after_request()

    @staticmethod
    def _log(arg):
        print(arg)
        sys.stdout.flush()