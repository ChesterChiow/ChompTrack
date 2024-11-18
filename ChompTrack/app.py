from server.controllers.IngredientsCtrl import IngredientsCtrl
from server.controllers.MealPlanCtrl import MealPlanCtrl
from server.controllers.RecipeCtrl import RecipeCtrl
from server.controllers.FilterCtrl import FilterCtrl
from server.controllers.filter.FilterFactory import FilterFactory
from server.DatabaseCtrl.credentials import SPOONACULAR_API_KEY
from server.DatabaseCtrl.UserQueries import UserQueries
from server.controllers.UserCtrl import UserCtrl
from server.entity.User import User
from server.enums.DietaryRestrictions import Restrictions
from server.enums.Intolerances import Intolerances
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

import requests


app = Flask(__name__,
            template_folder='client/src/pages',
            static_folder='client/src/static')

CORS(app)

user_queries = UserQueries()
user = User()
user_ctrl = UserCtrl(user)


requested_ids = []


@app.route('/', methods=['GET'])
def home():
    """
    Home route that checks if the user is logged in.
    Redirects to the user plan if logged in, otherwise shows the home page.

    Returns:
        Response: A rendered home page or a redirect.
    """
    global user
    if user is None:
        user = User()
    if user.is_logged_in():
        return redirect(url_for('show_myplan'))
    else:
        return render_template('index.html')

@app.route('/navbar')
def navbar():
    """
    This route serves the navbar HTML to be injected into the page dynamically.

    Returns:
        HTML: The navbar HTML content rendered by the 'navbar.html' template.
    """
    return render_template('navbar.html')

@app.route('/register', methods=['GET'])
def show_register():
    """
    Display the registration page.

    This route renders the 'loginRegister/register.html' template.
    Users visit this route to view the registration form.

    Returns:
        Response: The rendered HTML template for the registration page.
    """
    return render_template('loginRegister/register.html')


@app.route('/login', methods=['GET'])
def show_login():
    """
    Display the login page.

    This route renders the 'loginRegister/login.html' template.
    Users visit this route to view the login form.

    Returns:
        Response: The rendered HTML template for the login page.
    """
    return render_template('loginRegister/login.html')


@app.route('/profile-creation', methods=['GET'])
def show_profile_creation():
    """
    Display the profile creation page.

    This route checks if the user is logged in before displaying the
    'loginRegister/profileCreation.html' template. If the user is not logged
    in, they are redirected to the home page.

    Returns:
        Response: The rendered HTML template for the profile creation page,
        or a redirect to the home page if the user is not logged in.
    """
    global user
    if user.logged_in:
        return render_template('loginRegister/profileCreation.html')
    else:
        return redirect(url_for('home'))


@app.route('/suggested-intake', methods=['GET'])
def show_intake():
    """
    Display the suggested intake page.

    This route checks if the user is logged in before displaying the
    'loginRegister/suggestedIntake.html' template. If the user is not logged
    in, they are redirected to the home page.

    Returns:
        Response: The rendered HTML template for the suggested intake page,
        or a redirect to the home page if the user is not logged in.
    """
    global user
    if user.is_logged_in():
        return render_template('loginRegister/suggestedIntake.html')
    else:
        return redirect(url_for('home'))


@app.route('/my-plan', methods=['GET'])
def show_myplan():
    """
    Display the user's plan page.

    This route checks if the user is logged in before displaying the 'myplan.html'
    template. If the user is not logged in, they are redirected to the home page.

    Returns:
        Response: The rendered HTML template for the user's plan page, or a
        redirect to the home page if the user is not logged in.
    """
    if user.is_logged_in():
        return render_template('myplan.html')
    else:
        return redirect(url_for('home'))


@app.route('/grocery-list', methods=['GET'])
def show_grocerylist():
    """
    Display the grocery list page.

    This route checks if the user is logged in before displaying the
    'grocerylist.html' template. If the user is not logged in, they are
    redirected to the home page.

    Returns:
        Response: The rendered HTML template for the grocery list page, or a
        redirect to the home page if the user is not logged in.
    """
    if user.is_logged_in():
        return render_template('grocerylist.html')
    else:
        return redirect(url_for('home'))


@app.route('/history', methods=['GET'])
def show_history():
    """
    Display the user's history page.

    This route checks if the user is logged in before rendering the 'history.html'
    template. If the user is not logged in, they are redirected to the home page.

    Returns:
        Response: The rendered HTML template for the history page, or a redirect
        to the home page if the user is not logged in.
    """
    if user.is_logged_in():
        return render_template('history.html')
    else:
        return redirect(url_for('home'))


@app.route('/recipe', methods=['GET'])
def show_recipe():
    """
    Display a recipe page.

    This route checks if the user is logged in before displaying the 'recipe.html'
    template. It retrieves a recipe ID from the query parameters and passes it to
    the template. If the user is not logged in, they are redirected to the home page.

    Args:
        request.args.get('id'): The recipe ID passed as a query parameter.

    Returns:
        Response: The rendered HTML template for the recipe page with the recipe ID,
        or a redirect to the home page if the user is not logged in.
    """
    if user.is_logged_in():
        recipeID = request.args.get('id')
        return render_template('recipe.html', id=recipeID)
    else:
        return redirect(url_for('home'))


@app.route('/discover', methods=['GET'])
def show_discover():
    """
    Display the discover page.

    This route checks if the user is logged in before rendering the 'discover.html'
    template. If the user is not logged in, they are redirected to the home page.

    Returns:
        Response: The rendered HTML template for the discover page, or a redirect
        to the home page if the user is not logged in.
    """
    if user.is_logged_in():
        return render_template('discover.html')
    else:
        return redirect(url_for('home'))


@app.route('/logout', methods=['GET'])
def logout():
    """
    Log out the user.

    This route logs out the user by setting their `logged_in` status to `False`
    and clearing their user object. After logging out, the user is redirected
    to the home page.

    Returns:
        Response: A redirect to the home page after logging out.
    """
    global user
    user.logged_in = False
    user = None
    return redirect(url_for('home'))


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    This route accepts JSON data for username, email, and password, and attempts
    to register a new user. It checks if the username or email is already taken,
    and if not, inserts the new user into the database. If the registration is successful,
    it returns a success response. Otherwise, it returns an error message.

    Args:
        request.get_json(): JSON payload containing the username, email, and password.

    Returns:
        Response: A JSON response indicating whether the registration was successful
        or failed, including an appropriate status code.
    """
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if user_queries.does_username_or_email_exist(username, email):
        return jsonify({"error": "Registration failed. Username or email already exists."}), 400

    result = user_queries.insert_new_user(username, email, password)

    if result != 0:  # Successful insertion
        global user
        user.update_all_attributes(user_id=result, username=username, email=email, logged_in=True)
        return jsonify({"success": "Registration successful.", "userID": result}), 201

    return jsonify({"error": "Failed to register user."}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Handles the login functionality for a user. This route accepts a POST request with a JSON payload
    containing the username and password, verifies the user's credentials, and returns the appropriate
    response.

    Parameters:
        - username (str): The username of the user attempting to log in.
        - password (str): The password of the user attempting to log in.

    Returns:
        - JSON response:
            - If login is successful, returns the userID and a URL for redirection:
                {
                    "userID": userID,
                    "redirect_url": URL of the next page (either 'myplan' or 'profile_creation')
                }
            - If the username or password is incorrect, returns:
                {
                    "error": "Invalid username or password."
                }
            - If there is an internal server error, returns:
                {
                    "error": "An error occurred while processing your request."
                }

    Exceptions:
        - Handles general exceptions, logs the error, and returns a 500 Internal Server Error response
          with a generic error message.
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    try:
        userID = user_queries.find_user_id(username, "", password)

        if userID:
            global user
            user.user_id = userID
            user.login_user()
            print(user.get_register_complete())

            if user.height:
                print("line 152" + str(user.get_register_complete()))
                return jsonify({"userID": userID, "redirect_url": url_for('show_myplan')}), 200  # Redirect to my p

            else:
                user.username = username

                return jsonify({"redirect_url": url_for('show_profile_creation')}), 201  # Redirect to profile creat

        else:
            return jsonify({"error": "Invalid username or password."}), 401  # Unauthorized
    except Exception as e:
        # Log the error (optional, depending on your logging setup)
        print(f"Error during login: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request."}), 500  # Internal Server Error


@app.route('/updateProfile', methods=['POST'])
def updateProfile():
    """
    Updates the user's profile with new information such as gender, age, height, weight,
    activity level, diet type, and allergies.

    This route allows the user to update their profile by providing new values for
    various user attributes. If any of the provided values correspond to a restriction or
    intolerance, these will be updated as well. The user's nutrition profile will be
    recalculated based on the updated attributes.

    Args:
        request (JSON): The request body should contain the following keys:
            - `gender`: The user's gender (e.g., "Male", "Female").
            - `age`: The user's age (e.g., 25).
            - `height`: The user's height (e.g., 175 cm).
            - `weight`: The user's weight (e.g., 70 kg).
            - `activityLevel`: The user's activity level (e.g., "Low", "Medium", "High").
            - `dietType`: List of dietary restrictions (e.g., ["Vegetarian", "Vegan"]).
            - `allergy`: List of allergies (e.g., ["Dairy", "Gluten"]).
            Example input:
            {
                "gender": "Male",
                "age": 25,
                "height": 175,
                "weight": 70,
                "activityLevel": "Medium",
                "dietType": ["Vegetarian"],
                "allergy": ["Dairy"]
            }

    Returns:
        JSON response:
            - On success: A JSON object with a success message indicating
              that the user profile was updated successfully.
            - On failure: A JSON object containing an error message if
              the user profile update failed.

    Example:
        {
            "success": "User profile updated successfully!"
        }

        or
        {
            "error": "Failed to update user profile."
        }

    Raises:
        Exception: Any exception that may occur during the profile update process
                  will be captured and returned as an error response.
    """
    data = request.get_json()
    global user
    user_id = user.user_id

    # Retrieve user data from the database
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_ctrl = UserCtrl(user)  # Create an instance of UserCtrl

    # Update user attributes
    user_ctrl.update_gender(data.get('gender'))
    user_ctrl.update_age(data.get('age'))
    user_ctrl.update_height(data.get('height'))
    user_ctrl.update_weight(data.get('weight'))

    activity_level = data.get('activityLevel')
    user_ctrl.update_activity_level(activity_level)

    dietType = list(data.get('dietType'))
    allergy = list(data.get('allergy'))
    user_ctrl.recalculate_nutrition()

    if 'Anything' not in dietType:
        dietType_enums = []
        for diet in dietType:
            matched_enum = next(
                (restriction for restriction in Restrictions if restriction.value == diet),
                None
            )
            if matched_enum:
                dietType_enums.append(matched_enum)
        user_queries.add_User_Restrictions(user_id, dietType_enums)

    if 'None' not in allergy:
        allergy_enums = []
        for a in allergy:
            matched_enum = next(
                (intolerance for intolerance in Intolerances if intolerance.value == a),
                None
            )
            if matched_enum:
                allergy_enums.append(matched_enum)
        user_queries.add_User_Intolerances(user_id, allergy_enums)

    # Recalculate nutrition based on updated attributes
    user_ctrl.recalculate_nutrition()

    updateResult = user_queries.update_all_attributes(user_id, user_ctrl.user.gender,
                                                      user_ctrl.user.activity_level,
                                                      user_ctrl.user.height,
                                                      user_ctrl.user.weight,
                                                      user_ctrl.user.age,
                                                      user_ctrl.user.protein,
                                                      user_ctrl.user.fats,
                                                      user_ctrl.user.carbohydrates,
                                                      user_ctrl.user.calories)
    user.complete_register()
    if updateResult:  # Successful update
        return jsonify({"success": "User profile updated successfully!"}), 201
    else:
        return jsonify({"error": "Failed to update user profile."}), 500


@app.route('/getNutritions', methods=['POST'])
def getNutrition():
    """
    Retrieves the user's nutritional information including calories, carbohydrates,
    protein, and fats.

    This route returns the user's nutritional data based on their current profile.
    If the user profile is found, it returns the user's calorie, carbohydrate, protein,
    and fat values. If no user data is found, an error message is returned.

    Args:
        None: This route does not require any input parameters. It directly uses the
              global `user` object to fetch the nutritional data.

    Returns:
        JSON response:
            - On success: A JSON object containing the user's nutritional information
              (calories, carbohydrates, protein, and fats).
            - On failure: A JSON object with an error message if the user is not found.

    Example:
        {
            "calories": 2500,
            "carbohydrates": 300,
            "protein": 120,
            "fats": 80
        }

        or
        {
            "error": "User not found"
        }

    Raises:
        None: No exceptions are raised as the route relies on the global `user` object
              to provide nutritional data.
    """
    nutritions = {
        "calories": user.calories,
        "carbohydrates": user.carbohydrates,
        "protein": user.protein,
        "fats": user.fats,
    }

    if nutritions:
        return jsonify(nutritions), 200
    else:
        return jsonify({"error": "User not found"}), 404



@app.route('/getCurrentUser', methods=['POST'])
def get_current_user():
    """
    Retrieves the currently logged-in user's username.

    This route checks if the user is logged in and returns the username. If the user
    is not logged in, an error message is returned.

    Args:
        None: This route does not require any input parameters. It uses the global `user`
              object to determine the logged-in status and retrieve the username.

    Returns:
        JSON response:
            - On success: A JSON object containing the username of the logged-in user.
            - On failure: A JSON object with an error message if the user is not logged in.

    Example:
        {
            "username": "johndoe"
        }

        or
        {
            "error": "User not logged in."
        }

    Raises:
        None: No exceptions are raised as the route relies on the global `user` object
              for logged-in status.
    """
    if user.is_logged_in():
        return jsonify({"username": user.username}), 200
    else:
        return jsonify({"error": "User not logged in."}), 404


@app.route('/getDailyProgress', methods=['POST'])
def get_daily_progress():
    """
    Retrieves the user's daily nutrient progress (calories, fats, protein, carbohydrates)
    and calculates the percentage of each nutrient compared to the user's daily goal.

    This route calculates the daily progress of the user in terms of calories, fats, protein,
    and carbohydrates, and returns the percentage of the daily target achieved for each of these
    nutrients, capped at 100%.

    Args:
        None: This route expects a JSON payload containing the 'date' for which to fetch
              the progress (e.g., {'date': '2024-11-08'}).

    Returns:
        JSON response:
            - On success: A JSON object containing the daily progress data with percentages
              for calories, fats, protein, and carbohydrates.
            - On failure: A JSON object with an error message if the user's daily progress cannot be retrieved.

    Example:
        {
            "calories": 80,
            "fats": 60,
            "protein": 50,
            "carbohydrates": 70
        }

        or
        {
            "error": "Unable to fetch daily progress."
        }

    Raises:
        None: The route assumes that the `RecipeCtrl().get_nutrients_of_day()` method will handle
              any necessary exceptions related to data retrieval.
    """
    ctrl = RecipeCtrl()
    data = request.get_json()
    date = data.get('date')

    daily_progress = ctrl.get_nutrients_of_day(user.user_id, date)

    # Initialize percentage calculations
    cal_percentage = daily_progress["calories"] / user.calories * 100 if user.calories > 0 else 0
    fats_percentage = daily_progress["fats"] / user.fats * 100 if user.fats > 0 else 0
    protein_percentage = daily_progress["protein"] / user.protein * 100 if user.protein > 0 else 0
    carbs_percentage = daily_progress["carbohydrates"] / user.carbohydrates * 100 if user.carbohydrates > 0 else 0

    # Update daily progress with percentages capped at 100
    daily_progress["calories"] = round(min(cal_percentage, 100))
    daily_progress["fats"] = round(min(fats_percentage, 100))
    daily_progress["protein"] = round(min(protein_percentage, 100))
    daily_progress["carbohydrates"] = round(min(carbs_percentage, 100))

    return jsonify(daily_progress), 200




@app.route('/getMealPlans', methods=['POST'])
def getMealPlans():
    """
    Retrieves all meal plans for a user on a specific date.

    This route allows the user to retrieve all their meal plans for a specific date.

    Args:
        request (JSON): The request body should contain the following key:
            - `date`: The date for which to fetch the meal plans.
            Example input:
            {
                "date": "2024-11-01"
            }

    Returns:
        JSON response:
            - On success: A JSON array of meal plans for the specified date.
            - On failure: A JSON object containing an error message if no meal plans
              are found for the specified date.

    Example:
        {
            "mealPlans": [
                {"recipeID": 1234, "mealType": "lunch", "date": "2024-11-01"},
                {"recipeID": 5678, "mealType": "dinner", "date": "2024-11-01"}
            ]
        }

        or
        {
            "error": "No meal plans"
        }

    Raises:
        Exception: Any exception that may occur during the retrieval process will
                  be captured and returned as an error response.
    """
    ctrl = MealPlanCtrl()
    data = request.get_json()
    date = data.get('date')
    print(date)

    allMealPlans = ctrl.get_all_plans_for_date(user.user_id, date)

    if allMealPlans:
        return jsonify(allMealPlans), 200
    else:
        return jsonify({"error": "No meal plans"}), 404


@app.route('/addMealPlans', methods=['POST'])
def addMealPlans():
    """
    Adds a new meal plan for a user for a specific date and meal type.

    This route allows the user to add a new meal plan for a specific date and meal type
    (e.g., breakfast, lunch, dinner). It checks if a meal plan already exists for the
    specified date and meal type, and prevents duplicate meal plans.

    Args:
        request (JSON): The request body should contain the following keys:
            - `recipeID`: The ID of the recipe to add to the meal plan.
            - `selectedMealPlanDate`: The date for which to add the meal plan.
            - `mealType`: The type of meal (e.g., breakfast, lunch, dinner).
            Example input:
            {
                "recipeID": 1234,
                "selectedMealPlanDate": "2024-11-01",
                "mealType": "lunch"
            }

    Returns:
        JSON response:
            - On success: A JSON object containing a success message indicating
              that the meal plan was added successfully.
            - On failure: A JSON object containing an error message if a meal
              plan already exists for the specified date and meal type.

    Example:
        {
            "message": "Meal plan added successfully!"
        }

        or
        {
            "error": "Meal Plan for this date and course exists!"
        }

    Raises:
        Exception: Any exception that may occur during the adding process will
                  be captured and returned as an error response.
    """
    ctrl = MealPlanCtrl()
    data = request.get_json()
    recipeID = data.get('recipeID')
    date = data.get('selectedMealPlanDate')
    meal_type = data.get('mealType')
    if ctrl.create_meal_plan(user.user_id, recipeID, date, meal_type) is None:
        print("none")
        return jsonify({"error": "Meal Plan for this date and course exists!"}), 409

    return jsonify({"message": "Meal plan added successfully!"}), 201  # Success response


@app.route('/removeMealPlan', methods=['POST'])
def removeMealPlan():
    """
    Removes a meal plan for a user on a specific date and meal type.

    This route allows the user to remove a meal plan for a specific date and
    meal type (e.g., breakfast, lunch, dinner). The specified meal plan will
    be deleted from the user's records.

    Args:
        request (JSON): The request body should contain the following keys:
            - `date`: The date of the meal plan to remove.
            - `mealType`: The type of meal (e.g., breakfast, lunch, dinner).
            Example input:
            {
                "date": "2024-11-01",
                "mealType": "lunch"
            }

    Returns:
        JSON response:
            - On success: A JSON object with a success message indicating that
              the meal plan has been removed.
            - On failure: A JSON object containing an error message if the
              meal plan could not be removed.

    Example:
        {
            "success": "meal removed"
        }

    Raises:
        Exception: Any exception that may occur during the removal process
                  will be captured and returned as an error response.
    """
    ctrl = MealPlanCtrl()
    data = request.get_json()
    date = data.get('date')
    mealType = data.get('mealType')
    ctrl.delete_meal_plan(user.user_id, date, mealType)

    if True:
        return jsonify({"success": "meal removed"}), 200
    else:
        return jsonify({"error": "No meal plans"}), 404



@app.route('/completeMealPlan', methods=['POST'])
def completeMealPlan():
    """
    Marks a meal plan as completed or incomplete for a user on a specific date.

    This route allows the user to update the status of a meal plan by marking
    it as completed or not completed based on the specified date and meal type.

    Args:
        request (JSON): The request body should contain the following keys:
            - `date`: The date of the meal plan to update.
            - `mealType`: The type of meal (e.g., breakfast, lunch, dinner).
            - `completed`: A boolean value indicating whether the meal plan
              is marked as completed (`True`) or not (`False`).
            Example input:
            {
                "date": "2024-11-01",
                "mealType": "lunch",
                "completed": true
            }

    Returns:
        JSON response:
            - On success: A JSON object with a success message indicating that
              the meal status has been updated.
            - On failure: A JSON object containing an error message if the
              meal plan could not be updated.

    Example:
        {
            "success": "meal status"
        }

    Raises:
        Exception: Any exception that may occur during the updating process
                  will be captured and returned as an error response.
    """
    ctrl = MealPlanCtrl()
    data = request.get_json()
    date = data.get('date')
    mealType = data.get('mealType')
    completed = data.get('completed')
    ctrl.change_meal_plan_status(user.user_id, date, mealType, completed)

    if True:
        return jsonify({"success": "meal status"}), 200
    else:
        return jsonify({"error": "No meal plans"}), 404



@app.route('/getGroceryList', methods=['POST'])
def getGroceryList():
    """
    Retrieves the grocery list for a user based on the specified date range.

    This route fetches a list of grocery items that the user needs based on
    meal plans within a specified date range. It returns the grocery list
    for the given start and end dates.

    Args:
        request (JSON): The request body should contain the `startDate` and
                        `endDate` to filter the grocery list.
                        Example input:
                        {
                            "startDate": "2024-11-01",
                            "endDate": "2024-11-07"
                        }

    Returns:
        JSON response:
            - On success: A JSON array containing the grocery list for the
              specified date range.
            - On failure: A JSON object containing an error message if no
              grocery list is found or an issue occurs.

    Example:
        {
            "error": "No recipes"
        }

    Raises:
        Exception: Any exception that may occur during the fetching of the
                  grocery list will be captured and returned as an error
                  response.
    """
    ctrl = IngredientsCtrl()
    data = request.get_json()
    startDate = data.get('startDate')
    endDate = data.get('endDate')
    print(startDate)
    print(endDate)
    grocery_list = ctrl.get_grocery_list(user.user_id, startDate, endDate)

    print(grocery_list)
    if grocery_list:
        return jsonify(grocery_list), 200
    else:
        return jsonify({"error": "No recipes"}), 404



@app.route('/loadRecipes', methods=['POST'])
def loadRecipes():
    """
    Fetches random recipes from the database, excluding specified recipes.

    This route retrieves a list of random recipes from the database while
    excluding any recipes specified by their IDs. The number of recipes
    fetched is limited to 5.

    Args:
        request (JSON): The request body should contain a list of recipe IDs
                        to exclude from the response.
                        Example input:
                        {
                            "allRecipeIDs": [1, 2, 3]
                        }

    Returns:
        JSON response:
            - On success: A JSON array containing up to 5 random recipes
              excluding the ones specified.
            - On failure: A JSON object containing an error message if no
              recipes are found or an issue occurs.

    Example:
        {
            "error": "No recipes"
        }

    Raises:
        Exception: Any exception that may occur during the fetching of recipes
                  will be captured and returned as an error response.
    """
    data = request.get_json()
    excludedRecipeIDs = data.get('allRecipeIDs')

    recipeCtrl = RecipeCtrl()

    allRecipes = recipeCtrl.fetch_random_recipes_from_db(5, excludedRecipeIDs)

    if allRecipes:
        return jsonify(allRecipes), 200
    else:
        return jsonify({"error": "No recipes"}), 404

@app.route('/filterRecipes', methods=['POST'])
def filterRecipes():
    """
    Filter a list of recipes based on specified criteria.

    This route receives a JSON payload containing a list of recipes and filtering
    criteria, applies the relevant filters using the FilterCtrl and FilterFactory classes,
    and returns the filtered list of recipes.

    Args:
    request (JSON):
        "recipesShown": list,      # List of recipes to be filtered
        "criterias": dict          # Dictionary of filter criteria, with keys as filter types
                                   # and values as filter parameters.

    Returns:
        JSON response:
            - On success: Returns a JSON object with the filtered list of recipes under the key "filteredRecipeList".
            - On failure: Returns a JSON object with an error message if no recipes match the criteria.
    """
    data = request.get_json()
    recipeList= data.get('recipesShown')
    criterias = data.get('criterias')
    print(criterias)

    ctrl = FilterCtrl(recipeList)
    factory = FilterFactory()

    for key, value in criterias.items():
        if value:
            filter_obj = factory.get_filter(key,value)
            ctrl.add_filter(filter_obj)

    filteredRecipeList = ctrl.apply_filters()
    print("owvowev")
    print(filteredRecipeList)
    if filteredRecipeList:
        return jsonify(filteredRecipeList), 200
    else:
        return jsonify({"error": "No recipes"}), 404



@app.route('/loadHistory', methods=['POST'])
def loadHistory():
    """
    Retrieves the user's recipe history.

    This route fetches all the recipes previously accessed or saved by the
    user from the database. It returns a list of recipes associated with
    the user's account.

    Args:
        None: The function uses the current logged-in user's ID to fetch
              the recipe history.

    Returns:
        JSON response:
            - On success: A JSON array containing the list of recipes from
              the user's history.
            - On failure: A JSON object containing an error message if no
              recipes are found.

    Example:
        {
            "error": "No recipes for history"
        }

    Raises:
        Exception: Any exception that might occur during the database
                  query will be captured and returned in the error response.
    """
    ctrl = RecipeCtrl()
    allRecipes = ctrl.get_History(user.user_id)
    print(allRecipes)

    if allRecipes:
        return jsonify(allRecipes), 200
    else:
        return jsonify({"error": "No recipes for history"}), 404


@app.route('/getRecipe/<recipe_id>', methods=['GET'])
def getRecipe(recipe_id):
    """
    A route to fetch a recipe based on the recipe_id provided in the URL.

    Args:
        recipe_id (str): The unique identifier for the recipe in the URL path.

    Returns:
        Response: A JSON response containing the recipe data.
    """
    try:
        ctrl = RecipeCtrl()  # Create an instance of RecipeCtrl to handle the API call
        data = ctrl.get_recipe(recipe_id)  # Get the data from the API
        print(recipe_id)
        return jsonify(data)  # Return the recipe data as JSON in the response

    except Exception as e:
        # Return a generic error message if something goes wrong
        return jsonify({"error": "Unable to fetch recipe", "message": str(e)}), 500

app.run(debug=True, port=5000)
