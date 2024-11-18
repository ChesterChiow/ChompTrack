import requests
from server.entity.Recipe import Recipe
from server.DatabaseCtrl.credentials import SPOONACULAR_API_KEY as api_key
from server.controllers.IngredientsCtrl import IngredientsCtrl
from server.DatabaseCtrl.RecipeQueries import RecipeQueries


class RecipeCtrl:
    def Spoonacular_GetFullRecipeInfo_Count(self, count: int, exclude_tags: list[str] = '') -> dict:
        """
        Fetch detailed recipe information from Spoonacular API.

        :param count: int
            Number of recipes to retrieve.

        :param exclude_tags: list[str], optional
            Tags to exclude (e.g., dietary restrictions like 'vegetarian').

        :return: dict
            Dictionary of recipes with keys:
            - spoonacular_id (int): Recipe ID on Spoonacular.
            - name (str): Recipe title.
            - image (str): URL to recipe image.
            - cookingMinutes (int): Cooking time in minutes.
            - recipe_link (str): URL to full recipe.
            - price (float): Price per serving in USD.
            - nutrition: Nutrition information (calories, protein, etc.).
            - meal suitability flags (bool): Breakfast, lunch, dinner, snack suitability.
            - cuisine (str): Primary cuisine type.
            - ingredients (list[dict]): Ingredients with names and quantities.
        """
        def get_recipe_ingredients_and_price(recipe_id: int) -> dict:
            api_url = f"https://api.spoonacular.com/recipes/{recipe_id}/priceBreakdownWidget.json"
            conditions = {'apiKey': api_key}
            response = requests.get(api_url, params=conditions)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching recipes: {response.status_code}")
                return {}

        def get_random_recipes(conditions: dict) -> dict:
            api_url = "https://api.spoonacular.com/recipes/random"
            conditions['apiKey'] = api_key
            response = requests.get(api_url, params=conditions)

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching recipes: {response.status_code}")
                return {}

        params = {
            'number': count,
            'exclude-tags': exclude_tags,
            'includeNutrition': True,
            'includePrice': True
        }

        result = get_random_recipes(params)
        allrecipes = result.get('recipes', [])
        parsed_recipes = []

        for recipe in allrecipes:
            spoonacular_id = recipe.get('id')
            title = recipe.get('title')
            image = recipe.get('image')
            cookingMinutes = recipe.get('readyInMinutes') or 50

            source_url = recipe.get('sourceUrl')
            price = recipe.get('pricePerServing')
            nutrition = recipe.get('nutrition', {})
            nutrients = nutrition.get('nutrients', [])

            # Default values
            calories = protein = carbohydrates = fats = 0

            for nutrient in nutrients:
                name = nutrient.get('name')
                if name == 'Calories':
                    calories = nutrient.get('amount')
                elif name == 'Carbohydrates':
                    carbohydrates = nutrient.get('amount')
                elif name == 'Fat':
                    fats = nutrient.get('amount')
                elif name == 'Protein':
                    protein = nutrient.get('amount')

            cuisines = recipe.get('cuisines', [''])

            print(cuisines)
            if cuisines != []:
                cuisines = cuisines[0]

            else:
                cuisines = ''


            dishTypes = recipe.get('dishTypes', [])
            breakfast, lunch, dinner, snack = (
                'breakfast' in dishTypes, 'lunch' in dishTypes, 'dinner' in dishTypes, 'snack' in dishTypes
            )

            result = get_recipe_ingredients_and_price(spoonacular_id)
            ingredients = result.get('ingredients', [])

            recipe_data = {
                'recipe_id': spoonacular_id,
                'recipe_name': title,
                'image_link': image,
                'cooking_time': cookingMinutes,
                'recipe_instructions': source_url,
                'total_price': price,
                'calories': calories,
                'protein': protein,
                'carbohydrates': carbohydrates,
                'fats': fats,
                'breakfast': breakfast,
                'lunch': lunch,
                'dinner': dinner,
                'snack': snack,
                'cuisine_type': cuisines,
                'ingredients': ingredients
            }

            recipe = Recipe(**recipe_data)
            recipe.insert_into_database()
            ctrl = IngredientsCtrl()
            ctrl.save_ingredients_with_recipe(recipe.recipe_id, ingredients)

            parsed_recipes.append(recipe_data)

        return parsed_recipes

    def fetch_random_recipes_from_db(self, count: int, exclude_ids: list[int], exclude_tags: list[str] = '') -> dict:
        """
        Fetch random recipes from the database, excluding specified recipe IDs.

        :param count: int
            Number of recipes to fetch.
        :param exclude_ids: list[int]
            Recipe IDs to exclude from the results.
        :param exclude_tags: list[str], optional
            Tags to exclude from recipes.

        :return: dict
            Dictionary of recipes with keys (index-based):
            - recipeID (int): Recipe ID.
            - name (str): Recipe name.
            - Breakfast, Lunch, Dinner, Snack (bool): Meal type suitability.
            - cuisine (str): Cuisine type.
            - cost (float): Price per serving.
            - prepTime (int): Preparation time.
            - image (str): URL to recipe image.
        """
        unused_recipes = []
        recipe = None
        for i in range(count):
            recipe = Recipe().new_recipe_from_db(exclude_ids)
            if recipe.recipe_id:
                unused_recipes.append(recipe)
            else:
                recipe = Recipe(**self.Spoonacular_GetFullRecipeInfo_Count(1, exclude_tags)[0])
                unused_recipes.append(recipe)
            exclude_ids.append(recipe.recipe_id)

        if recipe.cooking_time is None:
            recipe.cooking_time = 50

        final_recipes = {
            index: {
                "recipeID": recipe.recipe_id,
                "name": recipe.recipe_name,
                "Breakfast": recipe.breakfast,
                "Lunch": recipe.lunch,
                "Dinner": recipe.dinner,
                "Snack": recipe.snack,
                "cuisine": recipe.cuisine_type,
                "cost": recipe.total_price,
                "prepTime": recipe.cooking_time,
                "image": recipe.image_link
            }
            for index, recipe in enumerate(unused_recipes, start=1)
        }

        return final_recipes

    def get_History(self, user_id: int) -> list[dict]:
        """
        Retrieve the full recipe history for a given user.

        :param user_id: int
            ID of the user.

        :return: list[dict]
            List of dictionaries representing the user's recipe history.
        """
        return Recipe().get_full_history(user_id)

    def get_nutrients_of_day(self, user_id: int, date: str) -> dict:
        """
        Retrieve total nutrient intake for a user on a specific date.

        :param user_id: int
            ID of the user.
        :param date: str
            Date in 'DD-MM-YYYY' format.

        :return: dict
            Dictionary of total nutrient intake with keys:
            - calories (int): Total calorie intake.
            - fats (int): Total fat intake.
            - protein (int): Total protein intake.
            - carbohydrates (int): Total carbohydrate intake.
        """
        daily_progress = {
            "calories": 0,
            "fats": 0,
            "protein": 0,
            "carbohydrates": 0
        }

        for mealtype in ['breakfast', 'lunch', 'dinner', 'snack']:
            recipe = Recipe().get_nutrients(user_id, date, mealtype)
            if recipe:
                for recipe_data in recipe.values():
                    daily_progress["calories"] += recipe_data.get("calories", 0)
                    daily_progress["fats"] += recipe_data.get("fats", 0)
                    daily_progress["protein"] += recipe_data.get("protein", 0)
                    daily_progress["carbohydrates"] += recipe_data.get("carbohydrates", 0)

        return daily_progress
    
    def get_recipe(self, recipe_id: str):
        """
        Fetches recipe information from the Spoonacular API using the provided recipe_id.

        Args:
            recipe_id (str): The unique identifier for the recipe.

        Returns:
            dict: Parsed JSON data of the recipe, including details like ingredients, nutrition, etc.

        Raises:
            HTTPError: If the API request fails (non-2xx status code).
        """
        try:
            print(recipe_id)
            # Call the external API to get recipe information
            response = requests.get(
                f'https://api.spoonacular.com/recipes/{recipe_id}/information',
                params={'apiKey': api_key, 'includeNutrition': True}
            )

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching recipes: {response.status_code}")
                return {}

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")  # Log HTTP error
            raise  # Re-raise the exception after logging

        except requests.exceptions.RequestException as req_err:
            print(f"Error with the request: {req_err}")  # Log network/connection error
            raise  # Re-raise the exception after logging

        except Exception as err:
            print(f"An unexpected error occurred: {err}")  # Log any other errors
            raise  # Re-raise the exception after logging


if __name__ == '__main__':
    recipeCtrl = RecipeCtrl()
    print(recipeCtrl.fetch_random_recipes_from_db(5, [13]))