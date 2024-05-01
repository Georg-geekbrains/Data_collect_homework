import os
import csv
import requests
from lxml import html

def write_to_csv(data, filename='movies_data.csv'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, filename)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    tree = html.fromstring(response.content)

    movie_elements = tree.xpath('//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div')

    movie_data = []
    for movie_element in movie_elements:
        name = movie_element.xpath('.//div[2]/a/h3/text()')
        year = movie_element.xpath('.//div[3]/span[1]/text()')
        rating = movie_element.xpath('.//span/div/span/@aria-label')

        if name and year and rating:
            movie_dict = {
                'Name': name[0].strip(),
                'Year': year[0].strip(),
                'Rating': rating[0].strip()
            }

            movie_data.append(movie_dict)
        else:
            print("Не удалось извлечь данные для фильма.")

    write_to_csv(movie_data, filename='movies_data.csv')
else:
    print('Не удалось получить данные: Код статуса', response.status_code)

