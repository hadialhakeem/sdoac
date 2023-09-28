import os

from mongodb import MongoAPI
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.environ["NEO_CONNECTION_URI"]
AUTH = (os.environ["NEO_USERNAME"], os.environ["NEO_PASSWORD"])


def count_rels(max_count=100):
    mongo = MongoAPI()
    characters = mongo.get_anime_character_full_sorted_favorites(max_count)

    rels = 0
    nodes = 0
    voices = set()
    animes = set()
    for character in characters:
        vas = [va for va in character["voices"] if va["language"] == "Japanese"]
        for anime in character["anime"]:
            animes.add(anime["anime"]["mal_id"])

        for va in vas:
            voices.add(va["person"]["mal_id"])

        num_animes = len(character["anime"])
        num_voices = len(vas)

        rels += num_voices + num_animes
        nodes += 1

    nodes += len(voices) + len(animes)
    print(f"Rels: {rels}")
    print(f"Nodes: {nodes}")


def migrate(max_count=100):
    mongo = MongoAPI()
    characters = mongo.get_anime_character_full_sorted_favorites(max_count)

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        count = 0
        for character in characters:
            parameters = {
                "props": {
                    "mal_id": character["mal_id"],
                    "mal_url": character["url"],
                    "name": character["name"],
                    "name_kanji": character["name_kanji"],
                    "nicknames": character["nicknames"],
                    "favorites": character["favorites"],
                    "about": character["about"],
                    "img_url": character["images"]["jpg"]["image_url"],
                }
            }
            driver.execute_query(
                "CREATE (:Character $props);",
                parameters_=parameters,
                database_="neo4j",
            )

            voices = [va for va in character["voices"] if va["language"] == "Japanese"]
            animes = character["anime"]

            for voice in voices:
                person = voice["person"]
                va = {
                    "mal_id": person["mal_id"],
                    "mal_url": person["url"],
                    "name": person["name"],
                    "img_url": person["images"]["jpg"]["image_url"],
                }
                parameters = {
                    "ch_mal_id": character["mal_id"],
                    "language": voice["language"],
                    **va,
                }
                driver.execute_query(
                    "MERGE (va:Voice {mal_id: $mal_id, mal_url: $mal_url, name: $name, img_url: $img_url }) "
                    "WITH va "
                    "MATCH (ch:Character {mal_id: $ch_mal_id}) "
                    "CREATE (va)-[:VOICES {language: $language}]->(ch);",
                    parameters_=parameters,
                    database_="neo4j",
                )

            for anime_info in animes:
                anime = anime_info["anime"]
                anime_props = {
                    "mal_id": anime["mal_id"],
                    "mal_url": anime["url"],
                    "title": anime["title"],
                    "img_url": anime["images"]["jpg"]["image_url"],
                }

                parameters = {
                    "ch_mal_id": character["mal_id"],
                    "role": anime_info["role"],
                    **anime_props,
                }
                driver.execute_query(
                    "MERGE (anime:Anime {mal_id: $mal_id, mal_url: $mal_url, title: $title, img_url: $img_url }) "
                    "WITH anime "
                    "MATCH (ch:Character {mal_id: $ch_mal_id}) "
                    "CREATE (anime)-[:HAS_CHARACTER {role: $role}]->(ch);",
                    parameters_=parameters,
                    database_="neo4j",
                )
            count += 1
            print(f"Completed: {count}/{max_count}")


if __name__ == "__main__":
    num_characters = 1000
    count_rels(num_characters)
    migrate(num_characters)

