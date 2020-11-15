from log_config import LOGGER
import json
import requests

artists = []
albums = []

def get_tracks(url, tracks):
    res = parse_response(requests.get(url))
    data = res["data"]
    for track in data:
        tracks.append({
            "full_title" : track["title"],
            "title" : track["title_short"],
            "album" : track["album"]["title"],
            "artist" : track["artist"]["name"]
        })
    try:
        next_batch = res["next"]
    except KeyError:
        next_batch = None
    return next_batch

def parse_response(res):
    last_char = len(res.text) - 1
    return json.loads(res.text[1:last_char])

def process_playlist_data(batch):
    for playlist in batch:
        tracks = []
        title = playlist["title"].replace(" ", "_")
        title = title.replace("/", "&")
        nb_tracks = playlist["nb_tracks"]
        tracklist = playlist["tracklist"]
        LOGGER.info(f"Treating {title} - {nb_tracks}")
        next_batch_url = get_tracks(tracklist + f"&output=jsonp&access_token={access_token}", tracks)
        while next_batch_url is not None:
            next_batch_url = get_tracks(next_batch_url, tracks)
        with open(f"data/playlists/{title}.json", "w") as f:
            json.dump(tracks, f, indent=4)

def process_album_data(batch):
    for album in batch:
        albums.append({
            "title" : album["title"],
            "release_date" : album["release_date"],
            "artist" : album["artist"]["name"]
        })

def process_artist_data(batch):
    for artist in batch:
        artists.append({
            "name" : artist["name"]
        })

def pagination_loop(url, callback, batch_size = 100):
    index = 0
    limit = batch_size
    total = batch_size + 1
    while limit < total + batch_size:
        res = parse_response(requests.get(url + f"&index={index}&limit={limit}"))

        batch = res["data"]
        total = res["total"]
        if index == 0:
            LOGGER.info(f"{total} total values")
        callback(batch)
        index = limit
        limit += batch_size

access_token = ""
user_id = ""
playlist_url = f"https://api.deezer.com/user/{user_id}/playlists?output=jsonp&output=jsonp&access_token={access_token}"
albums_url = f"https://api.deezer.com/user/{user_id}/albums?output=jsonp&output=jsonp&access_token={access_token}"
artists_url = f"https://api.deezer.com/user/{user_id}/artists?output=jsonp&output=jsonp&access_token={access_token}"

pagination_loop(playlist_url, process_playlist_data)
pagination_loop(albums_url, process_album_data)
pagination_loop(artists_url, process_artist_data)

LOGGER.info(f"writing {len(artists)} artists to file")
with open("data/artists.json", "w") as f:
    json.dump(artists, f, indent=4)

LOGGER.info(f"writing {len(albums)} albums to file")
with open("data/albums.json", "w") as f:
    json.dump(albums, f, indent=4)
