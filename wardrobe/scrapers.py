import random
import time
import asyncio
import requests
from bs4 import BeautifulSoup
from requests_html import AsyncHTMLSession, HTMLSession

def pinterest_scraper(search):
    session = HTMLSession()
    r = session.get("https://in.pinterest.com/search/pins/?q=" + search)
    r.html.render(timeout=20, sleep=10, keep_page=True, scrolldown=1)

    soup = BeautifulSoup(r.html.raw_html, 'html.parser')

    pics = soup.find_all('img')

    links = []
    for img in pics:
        link = img['src']
        links.append(link)

    if links == []:
        print('life be like yam')

    # r.close()
    # session.close()

    return {str(search): links}

def item_scraper(search):
    domain = 'https://www.pngegg.com/en/search?q='
    search = str(search)
    search = '+'.join(search.split())
    url = domain + search
    

    html = requests.get(url)
    response = html.text
    soup = BeautifulSoup(response, 'html.parser')

    images = soup.find_all("img", class_="lazy lst_img")
    links = []
    
    for img in images:
        link = img['data-src']
        links.append(link)

    return links
