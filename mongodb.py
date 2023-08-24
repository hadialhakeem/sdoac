import os
import certifi

from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoAPI:
    def __init__(self):
        self.client = MongoClient(os.environ["MONGODB_CONNECTION"],
                                  server_api=ServerApi('1'),
                                  tlsCAFile=certifi.where())
        self.db = self.client.main

        self.character_list = self.db.character_list
        self.character_details = self.db.character_details

    def insert_character_list(self, new_characters):
        self.character_list.insert_many(new_characters)
