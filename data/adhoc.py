import os

from mongodb import MongoAPI
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.environ["NEO_CONNECTION_URI"]
AUTH = (os.environ["NEO_USERNAME"], os.environ["NEO_PASSWORD"])


if __name__ == "__main__":
    mongo = MongoAPI()
    missing_person_list = [67384, 67411, 67618, 67724, 67725, 67756, 67820]
    persons = mongo.get_persons_in_mal_id_list(missing_person_list)

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

        count = 0
        for person in persons:
            parameters = {
                "person": {
                    "mal_id": person["mal_id"],
                    "mal_url": person["url"],
                    "website_url": person["website_url"],
                    "img_url": person["images"]["jpg"]["image_url"],
                    "name": person["name"],
                    "given_name": person["given_name"],
                    "family_name": person["family_name"],
                    "alternate_names": person["alternate_names"],
                    "birthday": person["birthday"],
                    "favorites": person["favorites"],
                    "about": person["about"],
                }
            }
            driver.execute_query(
                "CREATE (:Person $person);",
                parameters_=parameters,
                database_="neo4j",
            )
            count += 1
            print(f"Created Persons: {count}")
