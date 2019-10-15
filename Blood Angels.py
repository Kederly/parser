#!/usr/bin/env python3.7

import requests
from bs4 import BeautifulSoup
import csv
import os

os.remove('OrkShop.csv')

with open('OrkShop.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(('side', 'race', 'title', 'price', 'status', 'url'))

start_url = 'https://goodork.ru/categories/adeptus-astartes-blood-angels?page=1'
base = 'https://goodork.ru/categories/adeptus-astartes-blood-angels?page=?page='
name = 'Blood Angels'
side1 = 'Imperium'

def get_html(url):
    r = requests.get(url)
    return r.text

def get_total_pages(html):
    soup = BeautifulSoup(html, 'html5lib')
    pages = soup.find('div', class_='pagenumberer')
    if pages is None:
        total_pages = '1'
    else:
        pages = \
        soup.find('div', class_='pagenumberer').find_all('a', class_='pagenumberer-item pagenumberer-item-link')[-1].get('href')
        total_pages = pages.split('=')[1]

    return int(total_pages)

def write_csv(data):
    with open('OrkShop.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow((data['side'],
                         data['race'],
                         data['title'],
                         data['price'],
                         data['status'],
                         data['url']))

def get_page_data(html):
    soup = BeautifulSoup(html, 'html5lib')

    ads = soup.find('div', class_='row products-view products-view-tile productview-wow').find_all('div', class_='products-view-block')

    for ad in ads:

        try:
            title = ad.find('div', class_='products-view-name products-view-name-default').find('a').get('title')
        except:
            title = ''
        try:
            price = ad.find('div', class_='price').find('div', class_='price-number').text.strip()
        except:
            price = ''
        try:
            status = ad.find('div', class_='products-view-buttons').find('a', class_='btn btn-big btn-buy products-view-buy').text.strip()
            if status == 'В корзину':
                status = 'В наличии'
            else:
                status = 'Нет в наличии'
        except:
            status = 'Нет в наличии'
        try:
            url = ad.find('figure', class_='products-view-pictures').find('a', class_='products-view-picture-link products-view-shadow-hover').get('href')
        except:
            url = ''
        race = name
        side = side1
        data = {'side': side,
            'race': race,
            'title': title,
            'price': price,
            'status': status,
            'url': url}
        write_csv(data)

def main():
    url = start_url
    base_url = base

    total_pages = get_total_pages(get_html(url))

    for i in range(1, total_pages+1):
        url_gen = base_url + str(i)
        html = get_html(url_gen)
        get_page_data(html)

if __name__ == '__main__':
    main()
