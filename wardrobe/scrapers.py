import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup


def pinterest_scraper(search):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("wardrobe\chromedriver.exe", options=options)
    driver.get("https://in.pinterest.com/search/pins/?q=" + search)
    links = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    pics = soup.find_all('img')

    for img in pics:
        link = img['src']
        links.append(link)

    if links == []:
        print('life be like yam')
    else:
        print(links[:4])
        print(len(links))

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
