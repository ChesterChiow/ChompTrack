from server.DatabaseCtrl.DBFactory import DBFactory


class Ingredient:
    """
   Represents an ingredient with its properties and database interaction methods.

   Attributes:
       name (str): The name of the ingredient.
       priceperunit (float): The price per unit of the ingredient.
       amount (float): The quantity of the ingredient.
       measurement (str): The unit of measurement for the ingredient.
   """

    def __init__(self, name: str = None, price: float = None, amount: float = None, unit: str = None) -> None:
        """
        Initializes an Ingredient object with the given properties.

        Args:
            name (str, optional): The name of the ingredient. Defaults to None.
            price (float, optional): The price per unit of the ingredient. Defaults to None.
            amount (float, optional): The quantity of the ingredient. Defaults to None.
            unit (str, optional): The unit of measurement for the ingredient. Defaults to None.
        """
        self.name = name
        self.priceperunit = price
        self.amount = amount
        self.measurement = unit
        self.IngredientQueries = DBFactory().create_db_connection("Ingredient")

    def save(self, recipe_id: int) -> None:
        """
        Saves the ingredient to the database associated with a specific recipe ID.

        Args:
            recipe_id (int): The ID of the recipe to associate this ingredient with.
        """

        self.IngredientQueries.save_ingredient_into_db(self.name, price=self.priceperunit,
                                                       amount=self.amount, measurement=self.measurement,
                                                       recipe_id=recipe_id)

    def get_grocery_ingredients(self, user_id: int, start_date: str, end_date: str) -> dict:
        """
        Retrieves a grocery list of ingredients for a user within a specified date range.

        Args:
            user_id (int): The ID of the user requesting the grocery list.
            start_date (str): The start date of the period for which the grocery list is needed.
            end_date (str): The end date of the period for which the grocery list is needed.

        Returns:
            dict: A dictionary containing the grocery ingredients.
        """

        return self.IngredientQueries.get_ingredients(user_id, start_date, end_date)
