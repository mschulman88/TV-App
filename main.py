import os
from bottle import (get, post, redirect, request, route, run, static_file,
                    template, error)
import utils
import json


# Static Routes


@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = {})


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = {})


@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = {})


# Dynamic Routes


@route('/browse')
def browse():
    sectionTemplate = "./templates/browse.tpl"
    result = [json.loads(utils.getJsonFromFile(elem)) for elem in utils.AVAILABE_SHOWS]
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = result)


@route('/show/<show_id>')
def show(show_id):
    sectionTemplate = "./templates/show.tpl"
    show_current = json.loads(utils.getJsonFromFile(show_id))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = show_current)


@route('/ajax/show/<show_id>')
def show(show_id):
    sectionTemplate = "./templates/show.tpl"
    show_current = json.loads(utils.getJsonFromFile(show_id))
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = show_current)


@route('/show/<show_id>/episode/<episode_id>')
def episode(show_id, episode_id):
    sectionTemplate = "./templates/episode.tpl"
    show_current = json.loads(utils.getJsonFromFile(show_id))
    episode_current = show_current['_embedded']['episodes'][0]
    for elem in show_current['_embedded']['episodes']:
        if elem['id'] == int(episode_id):
            episode_current = elem
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = episode_current)


@route('/ajax/show/<show_id>/episode/<episode_id>')
def episode(show_id, episode_id):
    sectionTemplate = "./templates/episode.tpl"
    show_current = json.loads(utils.getJsonFromFile(show_id))
    episode_current = show_current['_embedded']['episodes'][0]
    for elem in show_current['_embedded']['episodes']:
        if elem['id'] == int(episode_id):
            episode_current = elem
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData = episode_current)


run(host='0.0.0.0', port=os.environ.get('PORT', 5000))