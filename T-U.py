from bottle import template
import os
import requests
import json

p = os.getcwd()

JSON_FOLDER = p + '/data/'
AVAILABLE_SHOWS = ["7", "66", "73", "82", "112", "143", "175", "216", "1371", "1871", "2993", "305"]


def getVersion():
    return "0.0.1"


def getJsonFromFile(showName):
    try:
        return template("{folder}/{filename}.json".format(folder=JSON_FOLDER, filename=showName))
    except:
        return "{}"


def get_show_by_id(show_id):
    show_as_list = [show for show in data["result"] if show['id'] == show_id]
    return show_as_list[0] if any(show_as_list) else {}


def get_episode_by_id(show_id, episode_id):
    show = get_show_by_id(show_id)
    if show:
        episode_as_list = [episode for episode in show["_embedded"]["episodes"] if episode["id"] == episode_id]
        return episode_as_list[0] if any(episode_as_list) else {}
    else:
        return {}


def load_data():
    # using the API to load data
    url = "http://api.tvmaze.com/shows/"
    results = []
    for show in AVAILABLE_SHOWS:
        show_req = requests.get(url + show)
        episode_req = requests.get(url + show + "/episodes")
        show_info = json.loads(show_req.text)
        show_info["_embedded"] = {}
        show_info["_embedded"]["episodes"] = json.loads(episode_req.text)
        results.append(show_info)
    return results

def load_local_data():
    # if loading from local data provided
    return [json.loads(getJsonFromFile(show)) for show in AVAILABLE_SHOWS]


def sort_browse(shows, order):
    if order == "rating":
        return reversed(sorted(shows, key=lambda result: result["rating"]["average"]))
    elif order == "name":
        return sorted(shows, key=lambda result: result["name"])
    else:
        return shows


def find_episodes(input):
    input = input.lower().strip()
    showresults = []
    for show in data["result"]:
        if input in show["name"].lower():
            showreturn = {}
            showreturn["showid"] = show["id"]
            showreturn["episodeid"] = show["_embedded"]["episodes"][0]["id"]
            showreturn["text"] = show["name"] + ": " + show["_embedded"]["episodes"][0]["name"]
            showreturn["rating"] = show["rating"]["average"]
            showresults.append(showreturn)
        for episode in show["_embedded"]["episodes"]:
            if input in episode["name"].lower() or (episode["summary"] and input in episode["summary"].lower()):
                episodereturn = {}
                episodereturn["episodeid"] = episode["id"]
                episodereturn["showid"] = show["id"]
                episodereturn["text"] = show["name"] + ": " + episode["name"]
                episodereturn["rating"] = show["rating"]["average"]
                showresults.append(episodereturn)
    return showresults


def sort_results(results, order):
    if order == "rating":
        return reversed(sorted(results, key=lambda result: result["rating"]))
    else:
        return sorted(results, key=lambda result: result["text"])


data = {
    "result": load_data()
}