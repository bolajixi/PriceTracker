from bs4 import BeautifulSoup
import requests
import smtplib

URL = 'https://www.konga.com/product/apple-iphone-11-128gb-rom-4gb-ram-ios-6-1-white-4823239'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}

page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

product_title = soup.find('h4', attrs={'class': '_24849_2Ymhg'}).get_text()
price = soup.find('div', attrs={'class': '_678e4_e6nqh'}).get_text()
converted_price = float(''.join(price[1:].split(',')))


def pricetracker():  # todo complete price tracker function
    pass


def email():
    pass