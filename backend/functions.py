from bs4 import BeautifulSoup
import requests
from config import *
from urllib import parse
from config import *

def scrape_anime(name):
    url_name = parse.quote(name)
    response = requests.get(anime_string + url_name)

    search_soup = BeautifulSoup(response.text, 'html.parser')

    picrefs = search_soup.fins_all('div', class_='picSurround')

    href = picrefs[0].a['href']

    response = requests.get(href)

    page_soup = BeautifulSoup(response.text, 'html.parser')
    return

def scrape_manga(name):
    url_name = parse.quote(name)
    response = requests.get(manga_string + url_name)

    search_soup = BeautifulSoup(response.text, 'html.parser')

    picrefs = search_soup.fins_all('div', class_='picSurround')

    href = picrefs[0].a['href']

    response = requests.get(href)

    page_soup = BeautifulSoup(response.text, 'html.parser')
    return

# Compares json dict with example dict from config.py to see if
# keys are equal
def compare_json(json, type_):
    equal = True

    if type_ == 'anime':
        base = Anime
    elif type_ == 'manga':
        base = Manga

    for key in json: 
        if key not in base:
            equal = False

    for key in base:
        if key not in json:
            equal = False

    return equal