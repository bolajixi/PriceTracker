from bs4 import BeautifulSoup
import requests
import smtplib
import config
import random


def get_product_info(soupObject):
    product_title = soupObject.find('h4', attrs={'class': '_24849_2Ymhg'}).get_text()
    return product_title


def get_product_price(soupObject):
    price = soupObject.find('div', attrs={'class': '_678e4_e6nqh'}).get_text()
    converted_price = float(''.join(price[1:].split(',')))
    return converted_price


def get_email():
    TempMail_API_Key = config.TempMail_API_KEY

    url = "https://privatix-temp-mail-v1.p.rapidapi.com/request/domains/"
    headers = {
        'x-rapidapi-host': "privatix-temp-mail-v1.p.rapidapi.com",
        'x-rapidapi-key': TempMail_API_Key
    }
    response = requests.request("GET", url, headers=headers)

    domain_list = response.json()


def main():
    URL = 'https://www.konga.com/product/apple-iphone-11-128gb-rom-4gb-ram-ios-6-1-white-4823239'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_info = get_product_info(soup)
    product_price = get_product_price(soup)

    # if product_price < 300000:
    get_email()
    print(product_info)
    print(product_price)


if __name__ == '__main__':
    main()