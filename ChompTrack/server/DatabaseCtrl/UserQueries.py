import mysql.connector

from server.DatabaseCtrl.credentials import SQL_CREDENTIALS
from server.DatabaseCtrl.DatabaseQueries import DatabaseQueries
from server.entity.User import User
from server.enums.Intolerances import Intolerances
from server.enums.DietaryRestrictions import Restrictions
from server.enums.Gender import Gender
from server.enums.ActivityLevel import ActivityLevel
import sys


class UserQueries(DatabaseQueries):

    def __init__(self):
        # Initialize the connection
        super().__init__()

    def close_connection(self):
        # Close cursor and connection
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed")

    def update_completed(self, user_id):
        sql_update_query = """UPDATE Users SET completed = TRUE WHERE user_id = %s"""

        # Use a tuple to pass the parameters correctly
        self.cursor.execute(sql_update_query, (user_id,))  # Note the comma here
        self.connection.commit()

    def fetch_completed_status(self, user_id:int)-> bool:
        """Fetch the completed status of a user."""
        sql_select_query = """SELECT completed FROM Users WHERE user_id = %s"""
        self.cursor.execute(sql_select_query, (user_id,))
        result = self.cursor.fetchone()  # Fetch the first row
        print("here" + str(result))
        if result is not None:

            completed_status = result[0]  # This will be an integer (0 or 1)
            return bool(completed_status)  # Convert to boolean
        else:
            return None  # If no user is found

    def does_username_or_email_exist(self, username: str, email: str) -> bool:
        """
        Checks if the username/email exists in the system.
        :param username: username to check
        :param email: email to check
        :return: True if either exists in the system, False otherwise.
        """
        insert_query = """
        SELECT user_id FROM Users 
        WHERE 
            (username = %s OR email = %s) 
        """
        self.cursor.execute(insert_query, (username, email))
        result = self.cursor.fetchone()  # Fetch the result

        # Ensure all results are fetched
        self.cursor.fetchall()  # Clear any unread results

        return result is not None  # Return True if found, False otherwise

    def insert_new_user(self, username: str, email: str, password: str) -> int:
        """
        Insert new user info into the Users table.
        :param username: username of new user
        :param email: email of the new user
        :param password: password of the new user
        :return: user_id of new user, 0 if unsuccessful.
        """
        if not self.does_username_or_email_exist(username, email):
            insert_query = """
            INSERT INTO Users(username, email, password)
            VALUES (%s, %s, %s)
            """
            # Use the .value attribute of the enums to pass the string value
            self.cursor.execute(insert_query, (username, email, password))
            self.connection.commit()
            # Return the ID of the newly inserted user
            return self.cursor.lastrowid
        else:
            return 0

    def logging_in_user(self, user_id:int)-> dict:
        """
        called only when user is logged in from existing user.
        :param user_id: user_id that successfully logged in
        :return: user object data without password
        """
        query = """
            SELECT username ,email ,gender, activityLevel, height, weight, age, protein, fats, carbohydrates, calories 
            FROM Users 
            WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()

        if result:
            print(result)
            height = result[4]
            weight = result[5]
            user_data = {
                'user_id': user_id,
                'username': result[0],
                'email': result[1],
                'gender': result[2],
                'activity_level': result[3],
                'height': float(height) if height else None,
                'weight': float(weight) if weight else None,
                'age': result[6],
                'protein': result[7],
                'fats': result[8],
                'carbohydrates': result[9],
                'calories': result[10],
                'logged_in': True

            }

            return user_data
        else:
            print("User not found.")
            return None

    def get_all_attributes(self, user_id: int) -> dict:
        """
        Get all user attributes for the specified user_id.

        :param user_id: ID of the user
        :return: A dictionary containing all user attributes
        """
        query = """
            SELECT gender, activityLevel, height, weight, age, protein, fats, carbohydrates, calories 
            FROM Users 
            WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()

        if result:
            return {
                'gender': result[0],
                'activity_level': result[1],
                'height': result[2],
                'weight': result[3],
                'age': result[4],
                'protein': result[5],
                'fats': result[6],
                'carbohydrates': result[7],
                'calories': result[8]
            }
        else:
            print("User not found.")
            return None

    def update_all_attributes(self, user_id: int, gender: Gender = None,
                              activity_level: ActivityLevel = None,
                              height: float = None, weight: float = None,
                              age: int = None, protein: int = None,
                              fats: int = None, carbohydrates: int = None,
                              calories: int = None) -> bool:
        """
        Update all user attributes for the specified user_id.

        :param user_id: ID of the user
        :param gender: New gender value (Enum) or None to keep the existing
        :param activity_level: New activity level value (Enum) or None to keep the existing
        :param height: New height value or None to keep the existing
        :param weight: New weight value or None to keep the existing
        :param age: New age value or None to keep the existing
        :param protein: New protein intake value or None to keep the existing
        :param fats: New fats intake value or None to keep the existing
        :param carbohydrates: New carbohydrates intake value or None to keep the existing
        :param calories: New calories intake value or None to keep the existing
        :return: True if update is successful, False otherwise
        """
        # Fetch current attributes first
        current_attributes = self.get_all_attributes(user_id)
        if not current_attributes:
            return False  # User does not exist, update fails

        # Set new values or keep existing ones
        new_gender = gender if gender else current_attributes['gender']
        new_activity_level = activity_level if activity_level else current_attributes['activity_level']
        new_height = height if height is not None else current_attributes['height']
        new_weight = weight if weight is not None else current_attributes['weight']
        new_age = age if age is not None else current_attributes['age']
        new_protein = protein if protein is not None else current_attributes['protein']
        new_fats = fats if fats is not None else current_attributes['fats']
        new_carbohydrates = carbohydrates if carbohydrates is not None else current_attributes['carbohydrates']
        new_calories = calories if calories is not None else current_attributes['calories']

        # Update user attributes in Users table
        update_user_query = """
            UPDATE Users
            SET gender = %s, activityLevel = %s
            WHERE user_id = %s
        """
        self.cursor.execute(update_user_query, (new_gender, new_activity_level, user_id))

        # Update user attributes in UserAttributes table
        update_attributes_query = """
            UPDATE Users
            SET height = %s, weight = %s, age = %s
            WHERE user_id = %s
        """
        self.cursor.execute(update_attributes_query, (new_height, new_weight, new_age, user_id))

        # Update user intakes in UserIntakes table
        # Debugging to check types
        new_protein = new_protein # Extract the first element of the tuple
        new_carbohydrates = new_carbohydrates # Extract the first element of the tuple
        print(type(new_protein), type(new_fats), type(new_carbohydrates), type(new_calories), type(user_id))
        update_intakes_query = """
            UPDATE Users
            SET protein = %s, fats = %s, carbohydrates = %s, calories = %s
            WHERE user_id = %s
        """
        self.cursor.execute(update_intakes_query, (new_protein, new_fats, new_carbohydrates, new_calories, user_id))

        self.connection.commit()
        return True  # Update was successful

    def find_user_id(self, username: str, email: str, password: str) -> int:
        """
        Find existing user data.
        :param username: username of existing user
        :param email: email of existing user
        :param password: password of existing user
        :return: user_id if found, None otherwise
        """
        insert_query = """
        SELECT user_id FROM Users 
        WHERE 
            (username = %s OR email = %s) 
            AND password = %s 
        """
        self.cursor.execute(insert_query, (username, email, password))
        result = self.cursor.fetchone()  # Fetch the result

        # Ensure all results are fetched
        self.cursor.fetchall()  # Clear any unread results

        return result[0] if result else None  # Return user_id if found

    def delete_user(self, username: str, email: str, password: str) -> bool:
        """
        Delete a user from the Users table.
        :param username: username of the user to be deleted
        :param email: email of the user to be deleted
        :param password: password of the user to be deleted
        :return: True if user was deleted successfully, False otherwise.
        """
        # Verify the user's credentials
        user_id = self.find_user_id(username, email, password)
        if user_id is not None:
            delete_query = """
            DELETE FROM Users 
            WHERE user_id = %s
            """
            self.cursor.execute(delete_query, (user_id,))
            self.connection.commit()
            return True  # User deleted successfully
        return False  # User not found or credentials invalid

    def add_User_Intolerances(self, user_id: int, intolerances: list[Intolerances]):
        """
        Add user intolerances to the database.

        :param user_id: The ID of the user.
        :param intolerances: A list of Intolerances Enum members.
        """
        for intolerance in intolerances:
            # Check if the intolerance already exists for the user
            check_query = """
            SELECT * FROM UserIntolerances 
            WHERE user_id = %s AND intolerance_name = %s
            """
            self.cursor.execute(check_query, (user_id, intolerance.name))  # Use .name for ENUM
            exists = self.cursor.fetchone()

            if exists is None:  # No existing record found
                insert_query = """
                INSERT INTO UserIntolerances (user_id, intolerance_name) 
                VALUES (%s, %s)
                """
                self.cursor.execute(insert_query, (user_id, intolerance.name))

        # Commit the transaction
        self.connection.commit()

    def get_user_intolerances(self, user_id: int) -> dict:
        """
        Retrieve intolerances for a specific user from the UserIntolerances table and return as a dictionary.
        :param user_id: ID of the user for whom to retrieve intolerances.
        :return: Dictionary with intolerance names as keys and their enum representation as values.
        """
        query = "SELECT intolerance_name FROM UserIntolerances WHERE user_id = %s"

        # Execute the query with the user_id parameter
        self.cursor.execute(query, (user_id,))

        # Fetch all results
        results = self.cursor.fetchall()
        intolerances_dict = {}
        if results:
            intolerances_list = [Intolerances[row[0].replace(' ', '_').upper()].value for row in results]
            intolerances_dict = {
                'user_id': user_id,
                'Intolerances': intolerances_list
            }
        return intolerances_dict

    def remove_User_intolerances(self, user_id: int, to_be_removed_intolerances: list[Intolerances]) -> bool:
        """
        Remove specified restrictions for a user from the UserIntolerances table.
        :param user_id: ID of the user from whom to remove intolerances.
        :param to_be_removed_intolerances: List of intolerances to be removed.
        :return: True if all restrictions were successfully removed, False otherwise.
        """
        if not to_be_removed_intolerances:
            return False  # Nothing to remove

        delete_query = """
        DELETE FROM UserIntolerances WHERE user_id = %s AND intolerance_name = %s
        """

        for intolerance in to_be_removed_intolerances:
            # Execute the delete query for each restriction
            self.cursor.execute(delete_query, (user_id, intolerance.value))

        # Commit the changes
        self.connection.commit()
        return True  # All specified restrictions were successfully removed

    def add_User_Restrictions(self, user_id: int, restrictions: list[Restrictions]):
        """
        Add user intolerances to the database.

        :param user_id: The ID of the user.
        :param restrictions: A list of Intolerances Enum members.
        """
        for restriction in restrictions:
            # Check if the intolerance already exists for the user
            check_query = """
            SELECT * FROM UserDietaryRestrictions 
            WHERE user_id = %s AND restriction_name = %s
            """
            self.cursor.execute(check_query, (user_id, restriction.name))  # Use .name for ENUM
            exists = self.cursor.fetchone()

            if exists is None:  # No existing record found
                insert_query = """
                INSERT INTO UserDietaryRestrictions (user_id, restriction_name) 
                VALUES (%s, %s)
                """
                self.cursor.execute(insert_query, (user_id, restriction.name))

        # Commit the transaction
        self.connection.commit()

    def get_user_restrictions(self, user_id: int) -> dict:
        """
        Retrieve restrictions for a specific user from the UserRestrictions table and return as a dictionary.
        :param user_id: ID of the user for whom to retrieve restrictions.
        :return: Dictionary with restriction names as keys and their enum representation as values.
        """
        query = "SELECT restriction_name FROM UserDietaryRestrictions WHERE user_id = %s"

        # Execute the query with the user_id parameter
        self.cursor.execute(query, (user_id,))

        # Fetch all results
        results = self.cursor.fetchall()
        restrictions_dict = {}
        if results:
            restrictions_list = [Restrictions[row[0].replace(' ', '_').upper()].value for row in results]
            restrictions_dict = {
                'user_id': user_id,
                'Restrictions': restrictions_list
            }
        return restrictions_dict

    def remove_User_Restrictions(self, user_id: int, to_be_removed_restrictions: list[Restrictions]) -> bool:
        """
        Remove specified restrictions for a user from the UserDietaryRestrictions table.
        :param user_id: ID of the user from whom to remove restrictions.
        :param to_be_removed_restrictions: List of restrictions to be removed.
        :return: True if all restrictions were successfully removed, False otherwise.
        """
        if not to_be_removed_restrictions:
            return False  # Nothing to remove

        delete_query = """
        DELETE FROM UserDietaryRestrictions WHERE user_id = %s AND restriction_name = %s
        """

        for restriction in to_be_removed_restrictions:
            # Execute the delete query for each restriction
            self.cursor.execute(delete_query, (user_id, restriction.value))

        # Commit the changes
        self.connection.commit()
        return True  # All specified restrictions were successfully removed

    def get_user_intake(self, date: str, user_id: int) -> dict:
        """
        Retrieves the total intake of protein, fats, carbohydrates, and calories for the given user on a specified date.

        :param date: The date for which the intake is requested, in 'dd-mm-yyyy' format.
        :param user_id: The user ID to retrieve intake data for.
        :return: A dictionary containing the total intake of 'protein', 'fats', 'carbohydrates', and 'calories'.
        """
        query = """
            SELECT 
                SUM(r.protein) AS total_protein,
                SUM(r.fats) AS total_fats,
                SUM(r.carbohydrates) AS total_carbohydrates,
                SUM(r.calories) AS total_calories
            FROM 
                MealPlans mp
            JOIN 
                Recipes r ON mp.recipe_id = r.recipe_id
            WHERE 
                mp.user_id = %s 
                AND DATE_FORMAT(mp.date, '%%d-%%m-%%Y') = %s
                AND mp.completed = TRUE;
            """
        try:
            self.cursor.execute(query, (user_id, date))
            result = self.cursor.fetchone()
            return {
                'protein': result['total_protein'] or 0,
                'fats': result['total_fats'] or 0,
                'carbohydrates': result['total_carbohydrates'] or 0,
                'calories': result['total_calories'] or 0
            }
        except mysql.connector.Error as err:
            print("Error: {}".format(err))
            return {'protein': 0, 'fats': 0, 'carbohydrates': 0, 'calories': 0}
        finally:
            self.cursor.close()
            self.connection.close()

    def run_tests(self):
        def terminate_program(message: str):
            """Print error message and terminate the program."""
            print(message)

            sys.exit(1)  # Exit with a status code of 1 (indicating an error)

        db = UserQueries()

        if not db.connection.is_connected():
            terminate_program("Failed to connect to the database")
        else:
            print("Successfully connected to the database")

        # Test Case 1: Add a new user
        print("Expected: Add successively and return user_id: ")
        result = db.insert_new_user('test1', 'test1@example.com', 'password')
        if result == 0:
            terminate_program("Failed to add new user")
        else:
            print(f"User ID of added user: {result}")

        # Test Case 2: Attempt to add the same user again
        print("Expected: Do not add and returns 0")
        result = db.insert_new_user('test1', 'test1@example.com', 'password')
        if result != 0:
            terminate_program("Should have returned 0 for not adding duplicate")
        else:
            print("     Successful.")

        # Test Case 3: Find user ID of the user
        print("Expected: Returns user_id of test1")
        user_id = db.find_user_id("test1", "test1@example.com", "password")
        if user_id is None:
            terminate_program("Should have returned user_id of test1")
        else:
            print("     Successful.")

        # Test Case 4: Adding intolerances with duplicates, should only add 4
        print("Expected: Adds only 4 intolerances to user")
        intolerances_to_add = [
            Intolerances.DAIRY,
            Intolerances.EGG,
            Intolerances.GLUTEN
        ]
        db.add_User_Intolerances(user_id, intolerances_to_add)
        intolerances_to_add = [
            Intolerances.DAIRY,
            Intolerances.EGG,
            Intolerances.SOY
        ]
        db.add_User_Intolerances(user_id, intolerances_to_add)

        if not (len(db.get_user_intolerances(user_id).get('Intolerances')) == 4):
            terminate_program("Length should be 4")
        else:
            print("     Successful.")

        # Test Case 5: Remove Intolerances
        print("Expected: removes 3 intolerances")
        intolerances_to_remove = [
            Intolerances.DAIRY,
            Intolerances.EGG,
            Intolerances.SOY,
            Intolerances.PEANUT
        ]

        db.remove_User_intolerances(user_id, intolerances_to_remove)
        if not (len(db.get_user_intolerances(user_id).get('Intolerances')) == 1):
            terminate_program("Length should be 1")
        else:
            print("     Successful.")

        # Test Case 6: Adding restrictions with duplicates, should only add 4

        print("Expected: Adds only 4 restrictions to user")
        restrictions_to_add = [
            Restrictions.PALEO,
            Restrictions.GLUTEN_FREE,
            Restrictions.PRIMAL
        ]
        db.add_User_Restrictions(user_id, restrictions_to_add)
        restrictions_to_add = [
            Restrictions.PALEO,
            Restrictions.GLUTEN_FREE,
            Restrictions.PESCETARIAN
        ]
        db.add_User_Restrictions(user_id, restrictions_to_add)

        if not (len(db.get_user_restrictions(user_id).get('Restrictions')) == 4):
            terminate_program("Length should be 4")
        else:
            print("     Successful.")

        # Test Case 7: Remove restrictions

        restrictions_to_remove = [
            Restrictions.PALEO,
            Restrictions.GLUTEN_FREE,
            Restrictions.PESCETARIAN,
            Restrictions.WHOLE30
        ]
        print("Expected: removes 3 restrictions")
        db.remove_User_Restrictions(user_id, restrictions_to_remove)
        if not (len(db.get_user_restrictions(user_id).get('Restrictions')) == 1):
            terminate_program("Length should be 4")
        else:
            print("     Successful.")

        # Test Case 8: Find user ID with wrong password
        print("Expected: Returns None for wrong password")
        user_id = db.find_user_id("test1", "test1@example.com", "wrongPassword")
        if user_id:
            terminate_program("Should have returned None for wrong password")
        else:
            print("     Successful.")

        # Test Case 9: Attempt to delete a user with incorrect password
        print("Expected: returns False for unsuccessful delete")
        result = db.delete_user('test1', 'test1@example.com', 'wrongPassword')
        if result is not False:
            terminate_program("Delete operation should have failed")
        else:
            print("     Successful.")

        # Test Case 10: Successfully delete the user
        print("Expected: returns True for successful delete")
        result = db.delete_user('test1', 'test1@example.com', 'password')
        if result is not True:
            terminate_program("Delete operation should have succeeded")
        else:
            print("     Successful.")

        # Verify the user is deleted
        print("Expected: Should return None after deletion")
        user_id = db.find_user_id("test1", "test1@example.com", "password")
        if user_id is not None:
            terminate_program("User should not exist after deletion.")
        else:
            print("     Successful.")

        db.close_connection()

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user's details by their user_id and return a User object.

        :param user_id: ID of the user to retrieve.
        :return: A User object containing user details, or None if the user is not found.
        """
        query = """
            SELECT username, email, gender, activityLevel, height, weight, age, protein, fats, carbohydrates, calories 
            FROM Users 
            WHERE user_id = %s
        """
        self.cursor.execute(query, (user_id,))
        result = self.cursor.fetchone()

        if result:
            return User(
                user_id=user_id,
                username=result[0],
                email=result[1],
                gender=result[2],
                activity_level=result[3],
                height=result[4],
                weight=result[5],
                age=result[6],
                protein=result[7],
                fats=result[8],
                carbohydrates=result[9],
                calories=result[10]
            )
        else:
            print("User not found.")
            return None


if __name__ == '__main__':
    db = UserQueries()
    db.run_tests()
