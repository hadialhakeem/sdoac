import time
import requests
import json
import sys

from enum import Enum
from apis.mongodb import MongoAPI


class Resource(Enum):
    CHARACTER = "character"
    PERSON = "person"
    ANIME = "anime"

    def __str__(self):
        return self.value


class JikanAPI:
    BASE_URL = "https://api.jikan.moe/v4"
    CHARACTER_SEARCH_URL = f"{BASE_URL}/characters"
    PERSON_SEARCH_URL = BASE_URL + "/people"
    ANIME_SEARCH_URL = BASE_URL + "/anime"

    CHARACTER_FULL_DETAILS_URL = BASE_URL + "/characters/{id}/full"
    PERSON_DETAILS_URL = BASE_URL + "/people/{}"
    ANIME_DETAILS_URL = BASE_URL + "/anime/{}"

    REQUEST_DELAY = 2  # Seconds

    METADATA_FILE = "H:/six-degrees-of-anime-characters/server/apis/meta/metadata.json"

    def __init__(self, mongo: MongoAPI):
        self.mongo = mongo

        with open(self.METADATA_FILE, "r") as jsonFile:
            meta = json.load(jsonFile)
        self.meta = meta

    def get_all_for_resource(self, resource: Resource):
        self._log(f"get_all_resource for resource {resource}")
        resource_to_url_map = {
            Resource.CHARACTER: self.CHARACTER_SEARCH_URL,
            Resource.PERSON: self.PERSON_SEARCH_URL,
            Resource.ANIME: self.ANIME_SEARCH_URL,
        }
        resource_to_mongo_insert_map = {
            Resource.CHARACTER: self.mongo.insert_character_list,
            Resource.PERSON: self.mongo.insert_persons,
            Resource.ANIME: self.mongo.insert_animes,
        }
        request_url = resource_to_url_map[resource]

        last_page_saved = self.meta[resource.value]["last_page_saved"]
        last_visible_page = self.meta[resource.value]["last_visible_page"]

        for page in range(last_page_saved + 1, last_visible_page + 1):
            self.wait_after_request()
            params = {
                "page": page
            }
            self._log(f"sending request for page: {page}")
            res = self.send_request_and_retry(request_url, True, params)
            res_json = res.json()
            res_data = res_json["data"]

            resource_to_mongo_insert_map[resource](res_data)
            self.update_last_saved(page, resource.value)

            self._log(f"{page}/{last_visible_page} pages done")
            self._log("============================================")

    def get_all_characters_fully(self):
        self._log("get_all_characters_fully")

        characters_incomplete = self.mongo.get_character_list_after_last_full_inserted()
        counter = 0
        for character in characters_incomplete:
            mal_id = character["mal_id"]
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
            return

        res.raise_for_status()

        if "data" not in res_json:
            self._log(f"res_json:{res_json}")
        character_data = res_json["data"]
        self.mongo.insert_character_full(character_data)

        self._log(f"Character id:{character_mal_id} retrieved.")

    def get_resource_details(self, mal_id, resource: Resource):
        self._log(f"Get Resource Details for mal_id: {mal_id}, resource: {resource}")
        resource_to_url_map = {
            Resource.PERSON: self.PERSON_DETAILS_URL,
            Resource.ANIME: self.ANIME_DETAILS_URL,
        }
        resource_to_mongo_insert_map = {
            Resource.PERSON: self.mongo.insert_persons,
            Resource.ANIME: self.mongo.insert_animes
        }

        req_url = resource_to_url_map[resource].format(mal_id)
        res = self.send_request_and_retry(req_url, False)
        res_json = res.json()

        if res.status_code == 404 and res_json["type"] == "BadResponseException" and \
                res_json["message"] == "Resource does not exist":
            self._log(f"Resource id {mal_id} does not exist on MAL. Skipping.")
            return

        res.raise_for_status()

        if "data" not in res_json:
            self._log(f"res_json:{res_json}")

        resource_data = res_json["data"]
        resource_to_mongo_insert_map[resource]([resource_data])

        self._log(f"Resource id:{mal_id} retrieved.")

    def update_last_saved(self, new_last_saved, namespace):
        with open(self.METADATA_FILE, "r", encoding='utf8') as jsonFile:
            metadata = json.load(jsonFile)

        metadata[namespace]["last_page_saved"] = new_last_saved

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

    def get_resources_from_id_list(self, mal_id_list, resource: Resource):
        counter = 0
        for mal_id in mal_id_list:
            self.get_resource_details(mal_id, resource)
            counter += 1
            self._log(f"Resource #{counter} inserted.")
            self._log("============================================")
            self.wait_after_request()

    @staticmethod
    def _log(arg):
        print(arg)
        sys.stdout.flush()
