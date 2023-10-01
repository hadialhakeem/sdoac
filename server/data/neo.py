import os

from neo4j import GraphDatabase


class NeoAPI:
    URI = os.environ["NEO_CONNECTION_URI"]
    AUTH = (os.environ["NEO_USERNAME"], os.environ["NEO_PASSWORD"])

    def __init__(self):
        self.driver = GraphDatabase.driver(self.URI, auth=self.AUTH)
        self.driver.verify_connectivity()

    def create_person(self, person_json):
        parameters = {
            "person": {
                "mal_id": person_json["mal_id"],
                "mal_url": person_json["url"],
                "website_url": person_json["website_url"],
                "img_url": person_json["images"]["jpg"]["image_url"],
                "name": person_json["name"],
                "given_name": person_json["given_name"],
                "family_name": person_json["family_name"],
                "alternate_names": person_json["alternate_names"],
                "birthday": person_json["birthday"],
                "favorites": person_json["favorites"],
                "about": person_json["about"],
            }
        }
        self.driver.execute_query(
            "CREATE (:Person $person);",
            parameters_=parameters,
            database_="neo4j",
        )
        print(f"Created Person: {person_json['mal_id']}")

    def create_anime(self, anime_json):
        if anime_json["titles"][0]["type"] != "Default":
            print(f"First anime title is not the default for mal_id {anime_json['mal_id']}")

        titles = [title_info["title"] for title_info in anime_json["titles"]]
        parameters = {
            "anime": {
                "mal_id": anime_json["mal_id"],
                "mal_url": anime_json["url"],
                "img_url": anime_json["images"]["jpg"]["image_url"],
                "approved": anime_json["approved"],
                "titles": titles,
                "title_default": titles[0],
                "type": anime_json["type"],
                "source": anime_json["source"],
                "episodes": anime_json["episodes"],
                "status": anime_json["status"],
                "airing": anime_json["airing"],
                "duration": anime_json["duration"],
                "rating": anime_json["rating"],
                "score": anime_json["score"],
                "scored_by": anime_json["scored_by"],
                "rank": anime_json["rank"],
                "popularity": anime_json["popularity"],
                "members": anime_json["members"],
                "favorites": anime_json["favorites"],
                "synopsis": anime_json["synopsis"],
                "background": anime_json["background"],
                "season": anime_json["season"],
                "year": anime_json["year"],
            }
        }
        self.driver.execute_query(
            "CREATE (:Anime $anime);",
            parameters_=parameters,
            database_="neo4j",
        )
        print(f"Created Anime: {anime_json['mal_id']}")

    def create_character(self, character_json):
        parameters = {
            "character": {
                "mal_id": character_json["mal_id"],
                "mal_url": character_json["url"],
                "img_url": character_json["images"]["jpg"]["image_url"],
                "name": character_json["name"],
                "name_kanji": character_json["name_kanji"],
                "nicknames": character_json["nicknames"],
                "favorites": character_json["favorites"],
                "about": character_json["about"],
            }
        }
        self.driver.execute_query(
            "CREATE (:Character $character);",
            parameters_=parameters,
            database_="neo4j",
        )

        print(f"Created Character: {character_json['mal_id']}")

    def create_character_relationships(self, character_json):
        """
        Create the relationships between nodes using the voices and anime field in the character json
        :param character_json:
        :return:
        """
        persons = [va for va in character_json["voices"] if va["language"] == "Japanese"]
        animes = character_json["anime"]

        for voice in persons:
            person = voice["person"]
            parameters = {
                "ch_mal_id": character_json["mal_id"],
                "language": voice["language"],
                "person_mal_id": person["mal_id"],
            }
            self.driver.execute_query(
                "MATCH (ch:Character {mal_id: $ch_mal_id}), (person:Person {mal_id: $person_mal_id}) "
                "CREATE (person)-[:VOICES {language: $language}]->(ch);",
                parameters_=parameters,
                database_="neo4j",
            )

        for anime_info in animes:
            anime = anime_info["anime"]
            parameters = {
                "ch_mal_id": character_json["mal_id"],
                "role": anime_info["role"],
                "anime_mal_id": anime["mal_id"],
            }
            self.driver.execute_query(
                "MATCH (ch:Character {mal_id: $ch_mal_id}), (anime:Anime {mal_id: $anime_mal_id}) "
                "CREATE (anime)-[:HAS_CHARACTER {role: $role}]->(ch);",
                parameters_=parameters,
                database_="neo4j",
            )

    def close(self):
        self.driver.close()
