import json
from clickhouse_driver import Client
import pandas as pd
import os

client = Client(host='localhost', port='9000')

client.execute('''
CREATE TABLE IF NOT EXISTS books (
    title String,
    price Float32,
    in_stock UInt16,
    description String
) ENGINE = MergeTree()
ORDER BY title
''')

script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'book_data.json')

with open(file_path, 'r') as file:
    data = json.load(file)

client.execute('INSERT INTO books (title, price, in_stock, description) VALUES', data)

print("Данные успешно загружены в ClickHouse.")

records = client.execute('SELECT * FROM books')
df_records = pd.DataFrame(records, columns=['title', 'price', 'in_stock', 'description'])
print(df_records.info())
