import requests
import pandas as pd
from telegram import *
from telegram.ext import *
from bs4 import BeautifulSoup
from bot_data import token, chat_id
import re

"""
Function that deletes emojis characters from strings
"""
def remove_emoji(string):
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
url = "https://xhobbies.co/collections"
categories = ["hogar-y-cocina", "mascotas", "deportes"]
categorias_productos = {}

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
    categorias_productos[category] = list_products



"""
Creating report with Xhobbies products data and sending it to a telegram chat
"""

bot = Bot(token)
for category, products in categorias_productos.items():
    final_message = 'Top 10 de productos más vendidos Xhobbies\nCategoría: {}\n\n'.format(category.upper())
    for product in products:
        name = product['product_name']
        original_price = product['product_original_price']
        sales_price = product['product_sales_price']
        if original_price == '$0.0':
            final_message += '-Producto: {} - Precio de venta: {}\n\n'.format(name, sales_price)
        else:
            final_message += '-Producto(oferta): {} - Precio antes: {} - Precio de venta: {}\n\n'.format(name, original_price, sales_price)
    print(final_message)

get_updates = bot.getUpdates()
print(get_updates)
print(dir(get_updates[0]))
print(get_updates[0].my_chat_member)
#bot.send_message(chat_id, text=final_message)