from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries


class RecipeQueries(DatabaseQueries):
    def __init__(self):
        super().__init__()

    def fetch_one_recipe(self, exclude_list: list[int] = None) -> dict:
        if exclude_list is None:
            exclude_list = []

        # Prepare the SQL query to fetch one recipe, excluding those in the exclude_list
        exclude_ids = ', '.join(map(str, exclude_list)) if exclude_list else 'NULL'
        query = f"""
        SELECT r.recipe_id, r.recipe_name, r.image, r.cooking_time, r.total_price, 
               r.protein, r.fats, r.carbohydrates, r.calories, r.breakfast, 
               r.lunch, r.dinner, r.snack, r.cuisine_type, r.spoonacular_id, r.recipe_instructions
        FROM Recipes r
        WHERE r.recipe_id NOT IN ({exclude_ids})
        ORDER BY RAND() LIMIT 1;
        """

        self.cursor.execute(query)
        recipe_row = self.cursor.fetchone()

        if recipe_row:

            recipe_data = {
                'recipe_id': recipe_row[0],  # Assuming spoonacular_id is recipe_id
                'recipe_name': recipe_row[1],
                'image_link': recipe_row[2],
                'cookingMinutes': recipe_row[3],
                'recipe_link': recipe_row[15],  # Set this if you have a source URL
                'price': float(round(recipe_row[4], 2)),
                'calories': recipe_row[8],
                'protein': recipe_row[5],
                'carbohydrates': recipe_row[6],
                'fats': recipe_row[7],
                'breakfast': True if recipe_row[9] == 1 else False,
                'lunch': True if recipe_row[10] == 1 else False,
                'dinner': True if recipe_row[11] == 1 else False,
                'snack': True if recipe_row[12] == 1 else False,
                'cuisine_type': recipe_row[13],
                'ingredients': self.fetch_ingredients_for_recipe(recipe_row[0])  # Fetch ingredients

            }

        else:
            recipe_data = {}

        return recipe_data

    def fetch_ingredients_for_recipe(self, recipe_id: int) -> list[dict]:
        """
        Fetch the ingredients for a specific recipe from the database.

        :param recipe_id: The ID of the recipe.
        :return: A list of dictionaries containing ingredient details.
        """
        query = """
        SELECT i.ingredient_id, i.name, ri.quantity, ri.measurements
        FROM RecipesIngredients ri
        JOIN Ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE ri.recipe_id = %s;
        """
        self.cursor.execute(query, (recipe_id,))
        ingredients_rows = self.cursor.fetchall()

        ingredients = []
        for row in ingredients_rows:
            ingredient_data = {
                'ingredient_id': row[0],
                'name': row[1],
                'quantity': float(round(row[2],2)),
                'measurements': row[3]
            }
            ingredients.append(ingredient_data)

        return ingredients


    def insert_recipe(self, recipe_id: int, name: str, image: str, cuisine: str, breakfast: bool,
                      lunch: bool, dinner: bool, snack: bool, cooking_time: int, total_price: float,
                      protein: float, fats: float, carbohydrates: float, calories: float,
                      recipe_instructions: str, spoonacular_id: int) -> None:
        """
        Inserts a recipe into the Recipes table in the database.

        :param recipe_id: The unique identifier for the recipe.
        :param name: The name of the recipe.
        :param image: The URL of the recipe image.
        :param cuisine: The cuisine type of the recipe.
        :param breakfast: Whether the recipe is suitable for breakfast.
        :param lunch: Whether the recipe is suitable for lunch.
        :param dinner: Whether the recipe is suitable for dinner.
        :param snack: Whether the recipe is suitable for a snack.
        :param cooking_time: The cooking time in minutes.
        :param total_price: The total price of the ingredients.
        :param protein: The amount of protein in grams.
        :param fats: The amount of fats in grams.
        :param carbohydrates: The amount of carbohydrates in grams.
        :param calories: The total calories of the recipe.
        :param recipe_instructions: Instructions for preparing the recipe.
        :param spoonacular_id: The spoonacular API identifier for the recipe.
        :return: None
        """
        query = """
        INSERT INTO Recipes (recipe_id, recipe_name, image, cuisine_type, breakfast, lunch, dinner, snack,
                             cooking_time, total_price, protein, fats, carbohydrates, calories, recipe_instructions, spoonacular_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """


        # Create the values tuple directly from parameters
        values = (recipe_id, name, image, cuisine, breakfast, lunch, dinner, snack,
                  cooking_time, total_price, protein, fats, carbohydrates, calories, recipe_instructions, spoonacular_id)

        self.cursor.execute(query, values)
        self.connection.commit()  # Commit the transaction
        print("Recipe inserted successfully")

    def fetch_all_history(self, user_id: int) -> list[dict]:
        """
        Fetch all completed meal plans for a user, joining with the Recipes table
        and sorting by date in descending order.

        :param user_id: ID of the user
        :return: List of completed meal plans with recipe details in dictionary format
        """
        query = """
        SELECT 
            r.recipe_id, 
            r.recipe_name, 
            mp.date, 
            mp.meal_type, 
            r.cuisine_type, 
            r.total_price, 
            r.cooking_time, 
            r.image
        FROM MealPlans mp
        INNER JOIN Recipes r ON mp.recipe_id = r.recipe_id
        WHERE mp.user_id = %s AND mp.completed = TRUE
        ORDER BY mp.date DESC
        """
        try:
            self.cursor.execute(query, (user_id,))
            results = self.cursor.fetchall()

            # Prepare the list of dictionaries to return
            meal_history = []
            for row in results:
                meal_history.append({
                    "recipeID": row[0],
                    "name": row[1],
                    "dateUsed": row[2],
                    "mealCategory": row[3],
                    "cuisine": row[4],
                    "cost": float(row[5]),
                    "prepTime": float(row[6]),
                    "image": row[7],
                })

            return meal_history

        except Exception as e:
            print("Error occurred while fetching meal history:", e)
            return []

    def fetch_on_date_and_mealtype(self, user_id: int, date: str, mealtype: str) -> dict:
        query = """
        SELECT r.recipe_id, r.recipe_name, r.cuisine_type, r.breakfast, r.lunch, 
               r.dinner, r.snack, r.cooking_time, r.total_price, r.image,
               r.protein, r.carbohydrates, r.calories, r.fats
        FROM MealPlans mp
        JOIN Recipes r ON mp.recipe_id = r.recipe_id
        WHERE mp.user_id = %s AND mp.date = %s AND mp.meal_type = %s AND mp.completed = 1
        """

        try:
            # Execute the query with the provided parameters
            self.cursor.execute(query, (user_id, date, mealtype))
            results = self.cursor.fetchall()

            # Convert results to dictionary format
            recipe_data = {}
            for row in results:
                time = row[7]        # Access cooking_time using index
                price= row[8]
                recipe_id = row[0]  # Access recipe_id using index
                recipe_data[recipe_id] = {
                    'recipe_name': row[1],         # Access recipe_name using index
                    'cuisine_type': row[2],        # Access cuisine_type using index
                    'breakfast': bool(row[3]),           # Access breakfast using index
                    'lunch': bool(row[4]),               # Access lunch using index
                    'dinner':bool( row[5]),              # Access dinner using index
                    'snack': bool(row[6]),               # Access snack using index
                    'cooking_time': float(time),        # Access cooking_time using index
                    'total_price': float(price),         # Access total_price using index
                    'image': row[9],               # Access image using index
                    'protein': float(row[10]),            # Access protein using index
                    'carbohydrates': float(row[11]),
                    'calories': float(row[12]),           # Access calories using index
                    'fats': float(row[13])
                }

            return recipe_data

        except Exception as e:
            print("Error fetching recipes:", e)
            return {}
        