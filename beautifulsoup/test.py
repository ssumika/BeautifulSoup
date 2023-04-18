import requests
from bs4 import BeautifulSoup
import MeCab

m = MeCab.Tagger('-Owakati')

url = "https://cookpad.com/recipe/2221374"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

recipe_title = soup.find('h1', class_='recipe-title').text.strip()
print(recipe_title)

ingredients_list = []
for ingredient in soup.find_all('div', class_='ingredient_row'):
    ingredient_quantity = ingredient.find('div', class_='ingredient_quantity')
    ingredient_name = ingredient.find('div', class_='ingredient_name')
    if ingredient_quantity is not None:
        ingredient_quantity = ingredient_quantity.text.strip()
        parsed_ingredient_quantity = m.parse(ingredient_quantity).rstrip('\n')
    else:
        parsed_ingredient_quantity = None
        
    if ingredient_name is not None:
        ingredient_name = ingredient_name.text.strip()
        parsed_ingredient_name = m.parse(ingredient_name).rstrip('\n')
    else:
        parsed_ingredient_name = None

    ingredients_list.append({'name': parsed_ingredient_name, 'quantity': parsed_ingredient_quantity})

print(ingredients_list)
