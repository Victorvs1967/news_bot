import re
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class Parser:
    host = 'https://vesti.ua/'
    url = 'https://vesti.ua/vse-novosti'

    lastkey = ''
    lastkey_file = ''

    def __init__(self, lastkey_file):
        
        self.lastkey_file = lastkey_file

        if os.path.exists(lastkey_file):
            self.lastkey = open(lastkey_file, 'r').read()
        else:
            with(open(lastkey_file, 'w')) as file:
                self.lastkey = self.get_lastkey()
                file.write(self.lastkey)

    def new_posts(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')

        news = []
        items = soup.select('.page-main-full > .posts > .post > .post-content > .title > a')

        for item in items:
            link = item['href']

            res = requests.get(link)
            soup = BeautifulSoup(res.content, 'lxml')
            heads = soup.find_all('div', {'class': 'content-head'})
            id = soup.find('div', {'class': 'full-post'})['data-id']

            if self.lastkey < id:
                news.append(link)

        return news

    def post_info(self, link):

        res = requests.get(link)
        soup = BeautifulSoup(res.content, 'lxml')
        heads = soup.find_all('div', {'class': 'content-head'})

        try:
            img = soup.find('div', {'class': 'first-post-image'}).img['src']
        except:
            img = 'https://picsum.photos/800/500'

        id = soup.find('div', {'class': 'full-post'})['data-id']
        title = heads[0].h1.text
        author = heads[0].find('div', {'class': 'author'}).a.text
        date = heads[0].find('div', {'class': 'date'}).text
        subtitle = heads[1].find('div', {'class': 'post-subtitle'}).text

		# form data
        info = {
            "id": id,
            "title": title,
            "link": link,
            "image": img,
            "excerpt": subtitle + ' ...'
        }

        return info

    def download_image(self, url):
        res = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = f'img_news/{os.path.basename(a.path)}'
        open(filename, 'wb').write(res.content)

        return filename

    def get_lastkey(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, 'lxml')
        link = soup.select('.page-main-full > .posts > .post > .post-content > .title > a')[0]['href']

        rs = requests.get(link)
        sp = BeautifulSoup(rs.content, 'lxml')
        key = sp.find('div', {'class': 'full-post'})['data-id']
        return str(key)

    def update_lastkey(self, new_key):
        self.lastkey = new_key

        with open(self.lastkey_file, 'r+') as file:
            data = file.read()
            file.seek(0)
            file.write(str(new_key))
            file.truncate()

        return new_key
