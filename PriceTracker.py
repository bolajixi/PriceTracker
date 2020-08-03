import argparse
import random
import schedule
import smtplib
import time

import requests
from bs4 import BeautifulSoup

import config


def parse_args():
    parser = argparse.ArgumentParser(description='Price tracker for retail goods')

    parser.add_argument('URL', type=str, help="Link to item you will like to track")
    parser.add_argument('--set_target_percent', type=float, help='Set the target percent you want', default=5)
    parser.add_argument('--email', type=str, help="Email you'd like to be notified")
    parser.add_argument('--mobile', type=int, help="Mobile number you'd like to be notified")

    return parser.parse_args()


def get_product_info(soupObject):
    product_title = soupObject.find('h4', attrs={'class': '_24849_2Ymhg'}).get_text()
    price = soupObject.find('div', attrs={'class': '_678e4_e6nqh'}).get_text()
    converted_price = float(''.join(price[1:].split(',')))
    return product_title, converted_price


def get_email():
    TempMail_API_Key = config.TempMail_API_KEY

    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"
    headers = {
        'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com",
        'x-rapidapi-key': TempMail_API_Key
    }
    response = requests.request("GET", url, headers=headers)

    domain_list = response.json()
    return 'pricetracker' + random.choice(domain_list)


def check_price(URL, target_price):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    _, product_price = get_product_info(soup)

    if product_price < target_price:
        print('...')

    print('\nCurrent Price:', '₦ ' + format(product_price, ','))
    print('Target Price:', '₦ ' + format(target_price, ',.2f'))

def send_email(email, link):
    pass


def main():
    args = parse_args()
    print('Starting to track prices...\n')

    URL = args.URL
    target_percent = args.set_target_percent
    while target_percent > 80:
        print('Set a target percentage between 1% - 80%')
        target_percent = float(input('Input new target percent: '))

    target_percent /= 100

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    product_info, product_price = get_product_info(soup)

    target_price = product_price * (1 - target_percent)

    print('Product Name:', product_info)
    print('Product Price:', '₦ '+format(product_price, ','))
    print('Target Price:', '₦ '+format(target_price, ',.2f'))


if __name__ == '__main__':
    main()