from bs4 import BeautifulSoup
import requests
import smtplib
import config
import random
import argparse


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


def main():
    args = parse_args()
    URL = args.URL

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40'}

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    product_info, product_price = get_product_info(soup)

    print('Starting to track prices\n')
    # target_price = input('What is your target price: ')
    target_price = args.set_target
    if target_price >= product_price:
        print('Target Price cannot be same or greater than product price '+'(₦ '+format(product_price, ',')+')')
        target_price = input('Input a new target price: ')
    elif product_price < target_price:
        send_email()


    print('Product Name:',product_info)
    print('Product Price:', '₦ '+format(product_price, ','))
    print('Target Price:', '₦ '+format(target_price, ',.2f'))


if __name__ == '__main__':
    main()