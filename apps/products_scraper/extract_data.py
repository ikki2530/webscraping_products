import requests
import datetime
import pandas as pd
from telegram import *
from telegram.ext import *
from bs4 import BeautifulSoup
# from bot_data import token, chat_id
# CREATE DATABASE ecommerce_db WITH OWNER ecommerce_user;
# CREATE USER ecommerce_user WITH ENCRYPTED PASSWORD 'ecommerce123';
# GRANT SELECT ON ALL TABLES IN  ecommerce_db public TO ecommerce_user;
# GRANT ALL PRIVILEGES  ON DATABASE ecommerce_user TO novokikes;
# DROP DATABASE IF EXISTS ecommerce_db;
import re

from apps.products_scraper.models import Product

"""
Function that deletes emojis characters from strings
"""
def remove_emoji(string: str):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


"""
Extracting data from Xhobbies
"""

def extract_data(url: str, categories):
    
    categories_products = {}

    for category in categories:
        url_query = "{}/{}?sort_by={}".format(url, category, "best-selling")
        r = requests.get(url_query)
        soup = BeautifulSoup(r.content, 'html.parser')
        header_title = soup.find_all(id='shopify-section-collection-header')
        title = header_title[0].find_all("h1", class_='section-header__title')[0].getText()
        title_spaces = title.strip('\n ')
        last_title = remove_emoji(title_spaces)
        products_section = soup.find("div", {'id': 'CollectionAjaxContent'})
        products_section = products_section.find_all("div", class_='grid--uniform')
        products = products_section[0].find_all("div", class_='grid__item')
        if len(products) > 10:
            products = products[0:10]
        list_products = []
        for product in products:
            product_dict = {}
            product_content = product.find("div", {'class': 'grid-product__content'})
            product_content_link = product_content.find("a", {'class': 'grid-product__link'})
            product_content_meta = product_content_link.find('div', {'class': 'grid-product__meta'})
            product_title = product_content_meta.find('div', {'class': 'grid-product__title'}).getText()
            product_price_content = product_content_meta.find('div', {'class': 'grid-product__price'})
            if len(product_price_content) > 1:
                price_original = product_price_content.find('del', {'class': 'grid-product__price--original'}).getText()
                price_sales = product_price_content.find('span', {'class': 'sale-price'}).getText()
            elif len(product_price_content) == 1:
                price_original = "$0.0"
                price_sales = product_price_content.find('span').getText()
            product_dict['product_name'] = product_title.strip()
            product_dict['product_original_price'] = price_original.strip()
            product_dict['product_sales_price'] = price_sales.strip()
            list_products.append(product_dict)
        categories_products[category] = list_products
    print("categories_products", categories_products)
    return categories_products


def create_products(categories_products):
    products_list = []
    for category, products in categories_products.items():
        for product in products:
            name = product['product_name']
            original_price = product['product_original_price']
            sale_price = product['product_sales_price']
            original_price = re.sub('[^0-9]', "", original_price)
            sale_price = re.sub('[^0-9]', "", sale_price)
            print("original_price", float(original_price))
            print("sale_price", float(sale_price))
            new_product = Product()
            new_product.name = name
            new_product.original_price = float(original_price)
            new_product.sale_price = float(sale_price)
            new_product.date = datetime.date.today()
            products_list.append(new_product)
    Product.objects.bulk_create(products_list)


def main_products():
    url = "https://xhobbies.co/collections"
    categories = ["hogar-y-cocina", "mascotas", "deportes"]
    products = extract_data(url, categories)
    # create_products(products)
