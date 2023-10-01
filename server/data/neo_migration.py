import os

from mongodb import MongoAPI
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.environ["NEO_CONNECTION_URI"]
AUTH = (os.environ["NEO_USERNAME"], os.environ["NEO_PASSWORD"])


def migrate(max_count=100):
    mongo = MongoAPI()
    persons = mongo.get_voice_actors()

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        l= mongo.get_all_anime()
        count = 0
        for anime in animes:
            if anime["titles"][0]["type"] != "Default":
                print(f"First anime title is not default for mal_id {anime['mal_id']}")

            titles = [title_info["title"] for title_info in anime["titles"]]
            parameters = {
                "anime": {
                    "mal_id": anime["mal_id"],
                    "mal_url": anime["url"],
                    "img_url": anime["images"]["jpg"]["image_url"],
                    "approved": anime["approved"],
                    "titles": titles,
                    "title_default": titles[0],
                    "type": anime["type"],
                    "source": anime["source"],
                    "episodes": anime["episodes"],
                    "status": anime["status"],
                    "airing": anime["airing"],
                    "duration": anime["duration"],
                    "rating": anime["rating"],
                    "score": anime["score"],
                    "scored_by": anime["scored_by"],
                    "rank": anime["rank"],
                    "popularity": anime["popularity"],
                    "members": anime["members"],
                    "favorites": anime["favorites"],
                    "synopsis": anime["synopsis"],
                    "background": anime["background"],
                    "season": anime["season"],
                    "year": anime["year"],
                }
            }
            driver.execute_query(
                "CREATE (:Anime $anime);",
                parameters_=parameters,
                database_="neo4j",
            )
            count += 1
            print(f"Created anime: {count}")

        characters = mongo.get_anime_character_full_sorted_favorites(max_count)
        characters = [ch for ch in characters]
        count = 0
        for character in characters:
            parameters = {
                "character": {
                    "mal_id": character["mal_id"],
                    "mal_url": character["url"],
                    "img_url": character["images"]["jpg"]["image_url"],
                    "name": character["name"],
                    "name_kanji": character["name_kanji"],
                    "nicknames": character["nicknames"],
                    "favorites": character["favorites"],
                    "about": character["about"],
                }
            }
            driver.execute_query(
                "CREATE (:Character $character);",
                parameters_=parameters,
                database_="neo4j",
            )

            persons = [va for va in character["voices"] if va["language"] == "Japanese"]
            animes = character["anime"]

            for voice in persons:
                person = voice["person"]
                parameters = {
                    "ch_mal_id": character["mal_id"],
                    "language": voice["language"],
                    "person_mal_id": person["mal_id"],
                }
                driver.execute_query(
                    "MATCH (ch:Character {mal_id: $ch_mal_id}), (person:Person {mal_id: $person_mal_id}) "
                    "CREATE (person)-[:VOICES {language: $language}]->(ch);",
                    parameters_=parameters,
                    database_="neo4j",
                )

            for anime_info in animes:
                anime = anime_info["anime"]
                parameters = {
                    "ch_mal_id": character["mal_id"],
                    "role": anime_info["role"],
                    "anime_mal_id": anime["mal_id"],
                }
                driver.execute_query(
                    "MATCH (ch:Character {mal_id: $ch_mal_id}), (anime:Anime {mal_id: $anime_mal_id}) "
                    "CREATE (anime)-[:HAS_CHARACTER {role: $role}]->(ch);",
                    parameters_=parameters,
                    database_="neo4j",
                )

            count += 1
            print(f"Completed: {count}")


if __name__ == "__main__":
    num_characters = 0
    migrate(num_characters)

