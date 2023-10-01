from mongodb import MongoAPI
from jikan import JikanAPI
from dotenv import load_dotenv

load_dotenv()


def validate_mal_id_for_collection(collection, collection_name):
    seen = set()
    to_delete = []

    for item in collection:
        mal_id = item["mal_id"]
        if mal_id in seen:
            print(f"Item duplicated for id: {mal_id}, {collection_name}")
            to_delete.append(item["_id"])
        else:
            seen.add(mal_id)

    return to_delete


def validate():
    mongo = MongoAPI()
    characters = mongo.get_anime_character_full_sorted_favorites()
    vas = mongo.get_voice_actors()
    animes = mongo.get_all_anime()

    del_ch = validate_mal_id_for_collection(characters, "character_full")
    del_p = validate_mal_id_for_collection(vas, "person")
    del_an = validate_mal_id_for_collection(animes, "anime")

    # mongo.delete_many_mongo_ids_from_collection("character_full", del_ch)
    # mongo.delete_many_mongo_ids_from_collection("person", del_p)
    # mongo.delete_many_mongo_ids_from_collection("anime", del_an)

    characters = mongo.get_anime_character_full_sorted_favorites()

    rels = 0
    nodes = 0
    voice_rels = 0
    anime_rels = 0

    va_mal_ids = set()
    anime_mal_ids = set()
    for character in characters:
        jp_vas = [va for va in character["voices"] if va["language"] == "Japanese"]
        for anime in character["anime"]:
            anime_mal_ids.add(anime["anime"]["mal_id"])

        for va in jp_vas:
            va_mal_ids.add(va["person"]["mal_id"])

        num_animes = len(character["anime"])
        num_voices = len(jp_vas)

        rels += num_voices + num_animes
        voice_rels += num_voices
        anime_rels += num_animes
        nodes += 1

    animes = mongo.get_all_anime()
    db_mal_ids = [anime["mal_id"] for anime in animes]
    db_mal_ids = set(db_mal_ids)

    discrepancy = []
    for anime_id in anime_mal_ids:
        if anime_id not in db_mal_ids:
            discrepancy.append(anime_id)

    print(f"In character but not in anime db: {discrepancy}")
    print(f"DB Mal IDS: {len(db_mal_ids)}")
    print(f"animes in character set: {len(anime_mal_ids)}")
    print(f"Rels: {rels}")
    print(f"HAS_CHARACTER: {anime_rels}")
    print(f"VOICES: {voice_rels}")
    print(f"TOTAL RELS: {anime_rels + voice_rels}")
    print(f"Nodes from character set: {nodes + len(va_mal_ids) + len(anime_mal_ids)}")
    print(f"Nodes from total set: {nodes + 7197 + 25359}")


if __name__ == "__main__":
    validate()




