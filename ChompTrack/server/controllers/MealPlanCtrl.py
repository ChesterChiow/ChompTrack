from server.entity.MealPlan import MealPlan

class MealPlanCtrl:
    """
    A class to control the creation, deletion, and modification of meal plans for users.
    """

    def create_meal_plan(self, user_id: int, recipe_id: int, date: str, meal_type: str) -> MealPlan:
        """
        Creates a new meal plan for a user.

        Args:
            user_id (int): The ID of the user for whom the meal plan is created.
            recipe_id (int): The ID of the recipe to be included in the meal plan.
            date (str): The date the meal plan is scheduled for, in YYYY-MM-DD format.
            meal_type (str): The type of meal (e.g., 'breakfast', 'lunch', 'dinner', 'snack').

        Returns:
            MealPlan: The created MealPlan object.
        """
        meal = MealPlan().create_new_meal_plan(user_id, recipe_id, date, meal_type)
        return meal

    def delete_meal_plan(self, user_id: int, date: str, meal_type: str) -> None:
        """
        Deletes a meal plan for a user.

        Args:
            user_id (int): The ID of the user whose meal plan will be deleted.
            date (str): The date of the meal plan to delete, in YYYY-MM-DD format.
            meal_type (str): The type of meal to delete (e.g., 'breakfast', 'lunch', 'dinner', 'snack').

        Returns:
            None
        """
        MealPlan().delete_meal_plan(user_id, date, meal_type)

    def change_meal_plan_status(self, user_id: int, date: str, meal_type: str, completed: bool) -> None:
        """
        Changes the completion status of a meal plan for a user.

        Args:
            user_id (int): The ID of the user whose meal plan status will be updated.
            date (str): The date of the meal plan to update, in YYYY-MM-DD format.
            meal_type (str): The type of meal to update (e.g., 'breakfast', 'lunch', 'dinner', 'snack').
            completed (bool): The new status of the meal plan, True if completed, False otherwise.

        Returns:
            None
        """
        MealPlan().change_meal_plan_status(user_id, date, meal_type, completed)

    def get_all_plans_for_date(self, user_id: int, date: str) -> dict:
        """
        Fetches all meal plans for a given date.

        Args:
            user_id (int): The ID of the user whose meal plans will be fetched.
            date (str): The date for which the meal plans are being fetched, in YYYY-MM-DD format.

        Returns:
            dict: A dictionary with meal types as keys ('breakfast', 'lunch', 'dinner', 'snack')
                  and corresponding MealPlan objects as values.
        """
        meal_plans_dict = {}
        for mealtype in ['breakfast', 'dinner', 'lunch', 'snack']:
            meal = MealPlan().fetch_meal_plan_from_db(user_id, date, mealtype)
            meal_plans_dict[mealtype] = meal

        return meal_plans_dict
