import aiml
import requests

# Initialize AIML kernel
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("LOAD AIML B")
# Replace with your Spoonacular API key\g

BASE_URL = 'https://api.spoonacular.com/recipes'
API_KEY = 'bdf93e0f01ea4e8e88713289d1c79abf'

def get_recipe_details(recipe_id):
    try:
        response = requests.get(f"{BASE_URL}/{recipe_id}/information", params={
            'apiKey': API_KEY
        })
        data = response.json()
        ingredients = data.get('extendedIngredients', [])
        ingredient_list = [f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}" for ingredient in ingredients]
        ingredients_text = "\n".join(ingredient_list)
        return ingredients_text
    except Exception as e:
        return f"An error occurred: {e}"

def get_recipe(query):
    try:
        response = requests.get(f"{BASE_URL}/search", params={
            'query': query,
            'apiKey': API_KEY,
            'number': 1
        })
        data = response.json()
        if data['results']:
            recipe = data['results'][0]
            recipe_id = recipe['id']
            ingredients_text = get_recipe_details(recipe_id)
            return (f"Here's a recipe for {query}: {recipe['title']}. More details: {recipe['sourceUrl']}\n\n"
                    f"Ingredients:\n{ingredients_text}")
        else:
            return "Sorry, I couldn't find any recipes for that query."
    except Exception as e:
        return f"An error occurred: {e}"

while True:
    input_text = input(">Human: ").strip().lower()
    if 'recipe' in input_text:
        query = input_text.replace('recipe', '').strip()
        recipe_info = get_recipe(query)
        print(f">Bot: {recipe_info}")
    else:
        response = kernel.respond(input_text)
        print(f">Bot: {response}")