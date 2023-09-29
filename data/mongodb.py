import os
import certifi
import pymongo

from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoAPI:
    def __init__(self):
        self.client_atlas = MongoClient(os.environ["MONGODB_CONNECTION_ATLAS"],
                                        server_api=ServerApi('1'),
                                        tlsCAFile=certifi.where())
        self.client_local = MongoClient(os.environ["MONGODB_CONNECTION_LOCAL"])

        self.db_atlas = self.client_atlas.main
        self.db_local = self.client_local.sdoac

        self.character_list = self.db_local.character_list
        self.character_full = self.db_local.character_full

        self.ANIME_ONLY_FILTER = {"anime": {"$not": {"$eq": []}}}

    def insert_character_list(self, new_characters):
        self.character_list.insert_many(new_characters)

    def insert_character_full(self, new_character):
        self.character_full.insert_one(new_character)

    def insert_persons(self, new_persons):
        self.db_local.person.insert_many(new_persons)

    def insert_animes(self, new_animes):
        self.db_local.anime.insert_many(new_animes)

    def get_character_list_after_last_full_inserted(self):
        last_inserted = self.get_last_character_full_inserted()
        q_filter = {}

        if last_inserted:
            q_filter = {
                "mal_id": {
                    "$gt": last_inserted["mal_id"]
                }
            }

        return self.character_list.find(q_filter, sort=[("_id", pymongo.ASCENDING)])

    def get_last_character_full_inserted(self):
        return self.character_full.find(sort=[("_id", pymongo.DESCENDING)], limit=1)[0]

    def get_anime_character_full_sorted_favorites(self, limit=0):
        return self.character_full.find(self.ANIME_ONLY_FILTER).sort("favorites", pymongo.DESCENDING).limit(limit)
