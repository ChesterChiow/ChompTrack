from datetime import datetime

from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries
import requests
from typing import Optional


class MealPlanQueries(DatabaseQueries):
    def __init__(self):
        super().__init__()

    def insert_new_meal_plan(self, user_id: int, recipe_id: int,
                             date: str, mealType: str, completed: bool) -> int:
        """
        Inserts a new meal plan into the database and returns the meal plan ID.

        :param user_id: ID of the user
        :param recipe_id: ID of the recipe
        :param date: Date of meal plan
        :param mealType: Which meal it is of the meal plan
        :param completed: Status of the meal plan
        :return: ID of the newly inserted meal plan, or None if it already exists
        """

        # First, check if a meal plan already exists for the given user_id, date, and mealType
        check_query = """
        SELECT COUNT(*)
        FROM MealPlans
        WHERE user_id = %s AND date = %s AND meal_type = %s
        """

        try:
            # Execute the check query
            self.cursor.execute(check_query, (user_id, date, mealType))
            exists = self.cursor.fetchone()[0]  # Get the count from the query

            # If a meal plan already exists, return None
            if exists > 0:
                return 0

            # Proceed with the insert if no existing meal plan found
            insert_query = """
            INSERT INTO MealPlans (user_id, recipe_id, date, meal_type, completed)
            VALUES (%s, %s, %s, %s, %s)
            """

            # Execute the insert query
            self.cursor.execute(insert_query,
                                (user_id, recipe_id, date, mealType, completed))

            # Commit the transaction
            self.connection.commit()

            # Get the ID of the newly inserted meal plan
            return self.cursor.lastrowid

        except Exception as e:
            # Rollback the transaction in case of error
            self.connection.rollback()
            print("Error occurred while inserting meal plan:", e)
            return 0

    def set_completed(self, user_id: int, date: str,mealtype: str,completed: bool) -> None:
        """
        Updates the status of a meal plan to mark it as completed or not.

        :param user_id: ID of the user
        :param date: Date of the meal plan
        :param completed: New status of the meal plan (True for completed, False for not completed)
        """
        update_query = """
        UPDATE MealPlans
        SET completed = %s
        WHERE user_id = %s AND meal_type = %s AND date = %s
        """

        try:
            # Execute the update query
            self.cursor.execute(update_query, (completed, user_id, mealtype,date))

            # Commit the transaction
            self.connection.commit()

            print(f"Meal plan status updated for user_id={user_id} on date={date} to completed={completed}")

        except Exception as e:
            # Rollback the transaction in case of error
            self.connection.rollback()
            print("Error occurred while updating meal plan status:", e)

    def delete_inserted_meal_plan(self, user_id: int, date: str, meal_type: str) -> bool:
        """
        Deletes a meal plan from the database based on user ID, recipe ID, meal type, and date.

        :param user_id: ID of the user
        :param meal_type: Type of the meal ('breakfast', 'lunch', 'dinner', or 'snack')
        :param date: Date of the meal plan in 'YYYY-MM-DD' format
        :return: True if the meal plan was deleted successfully, False otherwise
        """
        delete_query = """
        DELETE FROM MealPlans 
        WHERE user_id = %s AND meal_type = %s AND date = %s
        """

        try:
            # Execute the delete query
            self.cursor.execute(delete_query, (user_id, meal_type, date))

            # Commit the transaction
            self.connection.commit()

            # Check if any rows were affected (deleted)
            return self.cursor.rowcount > 0

        except Exception as e:
            # Rollback the transaction in case of error
            self.connection.rollback()
            print("Error occurred while deleting meal plan:", e)
            return False

    def fetch_meal_plans_user_id_and_date(self, user_id: int, date: str, mealtype: str) -> dict:
        """
        Fetches a meal plan based on user ID, date, and meal type, along with recipe details.

        :param user_id: ID of the user
        :param date: Date of the meal plan in 'YYYY-MM-DD' format
        :param mealtype: Type of meal (e.g., 'breakfast', 'lunch', 'dinner', 'snack')
        :return: A dictionary containing meal plan and recipe details if found, an empty dictionary otherwise
        """
        select_query = """
        SELECT mp.meal_plan_id, mp.user_id, mp.recipe_id, mp.date, mp.completed,
               r.recipe_name, r.cuisine_type, r.total_price, r.cooking_time, r.image
        FROM MealPlans mp
        JOIN Recipes r ON mp.recipe_id = r.recipe_id
        WHERE mp.user_id = %s AND mp.date = %s AND mp.meal_type = %s
        """

        try:
            # Execute the select query
            self.cursor.execute(select_query, (user_id, date, mealtype))

            # Fetch the result
            meal_plan_row = self.cursor.fetchone()

            if meal_plan_row:
                price = meal_plan_row[7]
                meal_plan_data = {
                    'meal_plan_id': meal_plan_row[0],
                    'user_id': meal_plan_row[1],
                    'recipeID': meal_plan_row[2],
                    'date': meal_plan_row[3],
                    'completed': meal_plan_row[4],
                    'name': meal_plan_row[5],
                    'cuisine': meal_plan_row[6],
                    'cost': float(price) if price is not None else None,
                    'prepTime': meal_plan_row[8],
                    'image': meal_plan_row[9],
                }
                return meal_plan_data
            else:
                return {}  # Return empty dictionary if no meal plan found

        except Exception as e:
            print("Error occurred while fetching meal plan:", e)
            return {}

if __name__ == '__main__':
    db = MealPlanQueries()

    db.insert_new_meal_plan(123,1100990,"2024-11-03",'lunch',False)
    print(db.fetch_meal_plans_user_id_and_date(123,1100990,"2024-11-03",'lunch'))
    db.change_meal_plan_status(123,1100990,"2024-11-03",'lunch',True)
    db.delete_inserted_meal_plan(123,1100990,"2024-11-03",'lunch')