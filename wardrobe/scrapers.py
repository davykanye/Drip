import random
import time

import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def pinterest_scraper(search):
    session = HTMLSession()
    r = session.get("https://in.pinterest.com/search/pins/?q=" + search)
    r.html.render(timeout=20, sleep=1, keep_page=True, scrolldown=1)

    soup = BeautifulSoup(r.html.raw_html, 'html.parser')

    pics = soup.find_all('img')

    links = []
    for img in pics:
        link = img['src']
        links.append(link)

    if links == []:
        print('life be like yam')

    r.close()
    session.close()

    return {str(search): links}

def item_scraper(search):

    links = []
    return {str(search): links}
