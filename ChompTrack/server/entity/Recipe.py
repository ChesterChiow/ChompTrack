
from server.DatabaseCtrl.DBFactory import DBFactory

class Recipe:
    """
    A class representing a Recipe with attributes for meal types, nutrition, and cooking details.

    Attributes:
        recipe_id (int): Unique identifier for the recipe.
        recipe_name (str): Name of the recipe.
        image_link (str): URL to the image of the recipe.
        cuisine_type (str): Type of cuisine for the recipe.
        breakfast (bool): True if suitable for breakfast, False otherwise.
        lunch (bool): True if suitable for lunch, False otherwise.
        dinner (bool): True if suitable for dinner, False otherwise.
        snack (bool): True if suitable for snack, False otherwise.
        cooking_time (int): Time in minutes required to cook the recipe.
        total_price (float): Total price for the recipe in dollars.
        protein (int): Amount of protein in the recipe (grams).
        fats (int): Amount of fat in the recipe (grams).
        carbohydrates (int): Amount of carbohydrates in the recipe (grams).
        calories (int): Amount of calories in the recipe.
        recipe_instructions (str): Step-by-step cooking instructions.
        ingredients (list): List of ingredients for the recipe.
    """

    def __init__(self, recipe_id: int = None, recipe_name: str = None, image_link: str = None, cuisine_type: str = None,
                 breakfast: bool = False, lunch: bool = False, dinner: bool = False, snack: bool = False,
                 cooking_time: int = 0, total_price: float = 0.00, protein: int = 0, fats: int = 0,
                 carbohydrates: int = 0, calories: int = 0, recipe_instructions: str = "",
                 ingredients=None) -> None:
        """
        Initializes a Recipe instance with the provided details.

        Args:
            recipe_id (int, optional): Unique identifier for the recipe.
            recipe_name (str, optional): Name of the recipe.
            image_link (str, optional): URL to the image of the recipe.
            cuisine_type (str, optional): Type of cuisine for the recipe.
            breakfast (bool, optional): True if the recipe is suitable for breakfast.
            lunch (bool, optional): True if the recipe is suitable for lunch.
            dinner (bool, optional): True if the recipe is suitable for dinner.
            snack (bool, optional): True if the recipe is suitable for a snack.
            cooking_time (int, optional): Time required to cook the recipe (in minutes).
            total_price (float, optional): Total price for the recipe in dollars.
            protein (int, optional): Amount of protein in the recipe (grams).
            fats (int, optional): Amount of fat in the recipe (grams).
            carbohydrates (int, optional): Amount of carbohydrates in the recipe (grams).
            calories (int, optional): Amount of calories in the recipe.
            recipe_instructions (str, optional): Step-by-step cooking instructions.
            ingredients (list, optional): Ingredients for the recipe.
        """
        self.recipe_id = recipe_id
        self.recipe_name = recipe_name
        self.image_link = image_link
        self.cuisine_type = cuisine_type
        self.breakfast = breakfast
        self.lunch = lunch
        self.dinner = dinner
        self.snack = snack
        self.cooking_time = cooking_time
        self.total_price = total_price
        self.protein = protein
        self.fats = fats
        self.carbohydrates = carbohydrates
        self.calories = calories
        self.recipe_instructions = recipe_instructions
        self.ingredients = ingredients
        self.recipeQueries = DBFactory().create_db_connection("Recipe")

    def new_recipe_from_db(self, exclude_ids: list[int]) -> "Recipe":
        """
        Fetches a new recipe from the database that is not in the provided list of excluded IDs.

        Args:
            exclude_ids (list[int]): List of recipe IDs to exclude.

        Returns:
            Recipe: The fetched Recipe object with updated attributes.
        """
        data = self.recipeQueries.fetch_one_recipe(exclude_ids)

        if data:
            self.recipe_id = data.get('recipe_id')
            self.recipe_name = data.get('recipe_name')
            self.image_link = data.get('image_link')
            self.cuisine_type = data.get('cuisine_type')
            self.breakfast = data.get('breakfast')
            self.lunch = data.get('lunch')
            self.dinner = data.get('dinner')
            self.snack = data.get('snack')
            self.carbohydrates = data.get('carbohydrates')
            self.calories = data.get('calories')
            self.recipe_instructions = data.get('recipe_instructions')
            self.ingredients = data.get('ingredients')
            self.cooking_time = data.get('cookingMinutes')
            self.total_price = data.get('price')

        return self

    def insert_into_database(self) -> None:
        """
        Inserts the current recipe instance into the database using RecipeQueries.

        Returns:
            None
        """

        print("Inserting recipe into the database...")

        self.recipeQueries.insert_recipe(
            recipe_id=self.recipe_id,
            name=self.recipe_name,
            image=self.image_link,
            cuisine=self.cuisine_type,
            breakfast=self.breakfast,
            lunch=self.lunch,
            dinner=self.dinner,
            snack=self.snack,
            cooking_time=self.cooking_time,
            total_price=self.total_price,
            protein=self.protein,
            fats=self.fats,
            carbohydrates=self.carbohydrates,
            calories=self.calories,
            recipe_instructions=self.recipe_instructions,
            spoonacular_id=self.recipe_id  # Ensure this is the correct spoonacular ID
        )
        print("Recipe inserted successfully")

    def get_full_history(self, user_id: int) -> dict:
        """
        Retrieves the full recipe history for a specific user.

        Args:
            user_id (int): The ID of the user for whom to fetch the recipe history.

        Returns:
            dict: A dictionary containing the user's recipe history.
        """
        fullHistory = self.recipeQueries.fetch_all_history(user_id)
        history = {index: data for index, data in enumerate(fullHistory, start=1)}
        return history

    def get_nutrients(self, user_id: int, date: str, mealtype: str) -> dict:
        """
        Fetches the nutritional information for a specific user's meal on a given date and meal type.

        Args:
            user_id (int): The ID of the user.
            date (str): The date of the meal.
            mealtype (str): The type of meal (e.g., breakfast, lunch, dinner).

        Returns:
            dict: A dictionary containing the nutritional information for the meal.
        """
        data = self.recipeQueries.fetch_on_date_and_mealtype(user_id, date, mealtype)
        return data