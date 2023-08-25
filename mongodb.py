import os
import certifi
import pymongo

from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoAPI:
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_CONNECTION"],
                                  server_api=ServerApi('1'),
                                  tlsCAFile=certifi.where())
        self.db = self.client.main

        self.character_list = self.db.character_list
        self.character_full = self.db.character_full

    def insert_character_list(self, new_characters):
        self.character_list.insert_many(new_characters)

    def insert_character_full(self, new_character):
        self.character_full.insert_one(new_character)

    def get_character_list_by_favourites(self):
        return self.character_list.find().sort("favorites", pymongo.DESCENDING)
