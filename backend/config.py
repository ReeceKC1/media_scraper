from pymongo import *

client = MongoClient("mongodb://reece:Puppypower1$@192.168.0.110:27017/media_scraper")

# add to document using collection.insert_one(item)
# get single document with find_one({'key': 'value'}) - return dict
# get many with .find() - return cursor
db = client.media_scraper
anime_collection = db.anime_collection
manga_collection = db.manga_collection
game_collection = db.game_collection
media_collection = db.media_collection

# db json format:
# key is name and type
Manga = {
    'name': 'name',
    'type': 'type',
    'alternative_titles': ['alternative_titles'],
    'volumes': 'volumes',
    'chapters': 'chapters',
    'status': 'status',
    'genres': ['genres'],
    'authors': ['authors'],
    'image': 'image',
    'synopsis': 'synopsis',
    'rating': 'rating',
    'read_status': 'read_status',
}
Anime = {
    'name': 'name',
    'type': 'type',
    'alternative_titles': ['alternative_titles'],
    'episodes': 'episodes',
    'durations': 'durations',
    'status': 'status',
    'genres': ['genres'],
    'image': 'image',
    'synopsis': 'synopsis',
    'rating': 'rating',
    'watch_status': 'watch_status',
}

anime_string = "https://myanimelist.net/anime.php?q="
manga_string = "https://myanimelist.net/manga.php?q="