import json
from pymongo import MongoClient
import os


client = MongoClient('mongodb://localhost:27017/')
db = client['book']
collection =db['data']

script_dir = os.path.dirname(os.path.abspath(__file__))
print(script_dir)
file_path = os.path.join(script_dir, 'book_data.json')
print(file_path)

with open(file_path, 'r') as file:
    books_data = json.load(file)

collection.insert_many(books_data)