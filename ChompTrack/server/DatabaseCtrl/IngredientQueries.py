from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries

class IngredientQueries(DatabaseQueries):
    def __init__(self):
        super().__init__()

    def link_ingredient_to_id(self, recipe_id:int, ingredient_id:int, amount:float, measurement:str)->None:
        """
        Links an ingredient to a recipe in the RecipesIngredients table.

        Args:
            recipe_id (int): ID of the recipe.
            ingredient_id (int): ID of the ingredient.
            amount (float): Quantity of the ingredient.
            measurement (str): Unit of measurement.
        """
        query = """
        INSERT INTO RecipesIngredients (recipe_id, ingredient_id, quantity, measurements)
        VALUES (%s, %s, %s, %s)
        """
        params = (recipe_id, ingredient_id, amount, measurement)
        self.cursor.execute(query, params)
        self.connection.commit()

    def does_ingredient_exist_in_db(self, name:str):
        """
        Checks if an ingredient exists in the database by name.

        Args:
            name (str): Name of the ingredient.

        Returns:
            int: ID of the ingredient if it exists, 0 if it doesn't.
        """
        query = "SELECT ingredient_id FROM Ingredients WHERE name = %s"
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def save_ingredient_into_db(self, name:str, price:float, recipe_id:int, amount:float, measurement:str):
        """
        Saves an ingredient into the database if it doesn't exist, and links it to a recipe.

        Args:
            name (str): Name of the ingredient.
            price (float z): Price per unit of the ingredient.
            recipe_id (int): ID of the recipe to link to.
            amount (float): Quantity of the ingredient.
            measurement (str): Unit of measurement.
        """
        try:
            ingredient_id = self.does_ingredient_exist_in_db(name)
            print(ingredient_id)
            if ingredient_id == 0:
                print("here")
            ingredient_id = self.insert_ingredient_into_db(name, price)

            self.link_ingredient_to_id(recipe_id, ingredient_id, amount, measurement)
            self.connection.commit()

        except Exception as e:
            pass



    def insert_ingredient_into_db(self, name:str, price:float):
        """
        Inserts a new ingredient into the Ingredients table.

        Args:
            name (str): Name of the ingredient.
            price (decimal): Price per unit of the ingredient.

        Returns:
            int: ID of the ingredient inserted into the database.
        """
        query = """
        INSERT INTO Ingredients (name, price_per_unit)
        VALUES (%s, %s)
        """

        self.cursor.execute(query, (name, price))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_ingredients(self, user_id: int, start_date: str, end_date: str) -> dict:
        query = """
        SELECT i. name AS ingredient_name, ri.quantity, ri.measurements, i.price_per_unit AS price, COUNT(*) AS quantity
        FROM MealPlans mp
        JOIN RecipesIngredients ri ON mp.recipe_id = ri.recipe_id
        JOIN Ingredients i ON ri.ingredient_id = i.ingredient_id
        WHERE mp.user_id = %s  
        AND mp.date BETWEEN %s AND %s
        GROUP BY i.name, ri.quantity, ri.measurements, i.price_per_unit
        """

        try:
            # Execute the query with the provided parameters
            self.cursor.execute(query, (user_id, start_date, end_date))
            results = self.cursor.fetchall()

            return results

        except Exception as e:
            print("Error fetching grocery list:", e)
            return {}


if __name__ == '__main__':
    db = IngredientQueries()
    db.save_ingredient_into_db("chicken",25.00,13,15,'g')