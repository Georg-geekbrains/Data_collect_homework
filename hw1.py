import requests
import json

import requests
import json

def get_foursquare_categories():
    
    client_id = "__"
    client_secret = "__"

    base_url = "https://api.foursquare.com/v3/places/search"
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        
    }

    headers = {
        "Accept": "application/json",
        "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }

    response = requests.get(url=base_url, params=params, headers=headers)
    print(response.status_code)
    data = json.loads(response.text)
    results = data.get("results", [])
    categories_names = []
    for result in results:
        if 'categories' in result:
            for category in result['categories']:
                if 'name' in category:
                    categories_names.append(category['name'])
    print(categories_names)
    return categories_names


def get_foursquare_data(city, category_id):

    client_id = "__"
    client_secret = "__"


    endpoint = "https://api.foursquare.com/v3/places/search"
    
    params = {
        'client_id': client_id,
        'cletnt_secret': client_secret,
        'near': city,
        'query': category_id,
    }

    headers = {
    "Accept": "application/json",
    "Authorization": "fsq3V3AFHzvqod5PVkb9j5ptfec29VfLTGG2XbHrQEGC8bI="
    }
    response = requests.get(url=endpoint, params=params, headers=headers)
    if response.status_code == 200:
        print(f'Успешный запрос')
        data = json.loads(response.text)
        return data.get("results", [])
        


def main():
    city = input("Enter city's name: ")
    categories = get_foursquare_categories()  

    print("Available categories:")
    for i, category in enumerate(categories):  
        print(f"{i + 1}. {category}")  

    selected_category_index = int(input("Enter the number of the category you want to search for: ")) - 1
   
    selected_category = categories[selected_category_index]
    print(selected_category)

    data = get_foursquare_data(city, selected_category)

    for venue in data:
        name = venue["name"]
        address = venue.get('location', {}).get('formatted_address', 'none')
        print(f"Name: {name}")
        print(f"Address: {address}")
        print()

if __name__ == "__main__":
    main()