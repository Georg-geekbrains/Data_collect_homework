"""
Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и 
извлечь информацию о всех книгах на сайте во всех категориях:
название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
Затем сохранить эту информацию в JSON-файле.
"""


import requests
from bs4 import BeautifulSoup
import json
url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
def extract_book_info(url):
    
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').text.strip()
    price = float(soup.find('p', class_='price_color').text.strip('£'))

    availability = soup.find('p', class_='instock availability').text.strip()
    in_stock = int(availability.split('(')[1].split(' ')[0])

    description_element = soup.find('div', id='product_description')
    if description_element:
         description = description_element.find_next('p').text.strip()
    else:
         description = ''
         

    dictionary_ =  {'title': title,
                    'price': price,
                    'in_stock': in_stock,
                    'description': description}
    return dictionary_



def scrape_all_books():
    base_url = 'http://books.toscrape.com/'
    book_data = []

    category_urls = [base_url + 'catalogue/category/books_1/index.html']
    while category_urls:
        category_url = category_urls.pop(0)

        response = requests.get(url=category_url) 
        soup = BeautifulSoup(response.content, 'html.parser')
        
        book_links = [base_url + 'catalogue/' + link.find('a').get('href').lstrip("../") for link in soup.find_all('h3')]
        for book_link in book_links:
            book_data.append(extract_book_info(book_link))

        next_page = soup.find('li', class_='next')
        if next_page:
                next_url = base_url + 'catalogue/' + next_page.find('a')['href']
                category_urls.append(next_url)
        print(next_page)
        print(category_urls)
    
    return book_data

book_data = scrape_all_books()

with open('book_data.json', 'w', encoding='utf-8') as f:
    json.dump(book_data, f, ensure_ascii=False, indent=4)
    
