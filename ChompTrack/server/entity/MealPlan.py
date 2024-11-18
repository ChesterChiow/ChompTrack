from server.DatabaseCtrl.DBFactory import DBFactory


class MealPlan:
    """
    Represents a meal plan with its properties and database interaction methods.

    Attributes:
        user_id (int): The ID of the user associated with the meal plan.
        recipe_id (int): The ID of the recipe in the meal plan.
        date (str): The date of the meal.
        meal_type (str): The type of meal (e.g., breakfast, lunch, dinner).
        completed (bool): Indicates if the meal plan has been completed.
        db (MealPlanQueries): An instance of the MealPlanQueries class for database operations.
    """
    def __init__(self, user_id: int = 0, recipe_id: int = 0,
                 date: str = '', mealtype: str = '', completed: bool = True) -> None:
        """
        Initializes a MealPlan object with the given properties.

        Args:
            user_id (int, optional): The ID of the user associated with the meal plan. Defaults to 0.
            recipe_id (int, optional): The ID of the recipe in the meal plan. Defaults to 0.
            date (str, optional): The date of the meal. Defaults to an empty string.
            mealtype (str, optional): The type of meal (e.g., breakfast, lunch, dinner). Defaults to an empty string.
            completed (bool, optional): Indicates if the meal plan has been completed. Defaults to True.
        """
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.date = date
        self.meal_type = mealtype
        self.completed = completed
        self.db = DBFactory().create_db_connection("MealPlan")

    def fetch_meal_plan_from_db(self, user_id: int, date: str, meal_type: str) -> dict:
        """
        Fetches a meal plan from the database for a specific user, date, and meal type.

        Args:
            user_id (int): The ID of the user for whom to fetch the meal plan.
            date (str): The date of the meal plan.
            meal_type (str): The type of meal (e.g., breakfast, lunch, dinner).

        Returns:
            MealPlan: The fetched meal plan as a MealPlan object.
        """
        data = self.db.fetch_meal_plans_user_id_and_date(user_id, date, meal_type)
        return data

    def create_new_meal_plan(self, user_id: int, recipe_id:int, date: str, meal_type: str) -> object:
        """
        Creates a new meal plan and inserts it into the database.

        Args:
            user_id (int): The ID of the user associated with the meal plan.
            recipe_id (int): The ID of the recipe in the meal plan.
            date (str): The date of the meal plan.
            meal_type (str): The type of meal (e.g., breakfast, lunch, dinner).

        Returns:
            MealPlan or None: The created MealPlan object, or None if the insertion failed.
        """
        id = self.db.insert_new_meal_plan(user_id, recipe_id, date, meal_type, False)
        print(id, type(id))
        if id == 0:
            return None

        else:
            self.user_id = user_id
            self.recipe_id = recipe_id
            self.date = date
            self.meal_type = meal_type
            self.completed = False
            return self

    def change_meal_plan_status(self, user_id: int, date: str, meal_type: str,
                                completed: bool) -> object:
        """
        Updates the completion status of a meal plan in the database.

        Args:
            user_id (int): The ID of the user associated with the meal plan.
            date (str): The date of the meal plan.
            meal_type (str): The type of meal (e.g., breakfast, lunch, dinner).
            completed (bool): The new completion status.

        Returns:
            MealPlan: The updated MealPlan object.
        """
        self.db.set_completed(user_id, date, meal_type, completed)
        self.user_id = user_id
        self.date = date
        self.meal_type = meal_type
        self.completed = completed

        return self

    def delete_meal_plan(self, user_id: int, date: str, meal_type: str) -> None:
        """
        Deletes a meal plan from the database.

        Args:
            user_id (int): The ID of the user associated with the meal plan.
            date (str): The date of the meal plan.
            meal_type (str): The type of meal (e.g., breakfast, lunch, dinner).

        Returns:
            None
        """
        self.db.delete_inserted_meal_plan(user_id, date, meal_type)
