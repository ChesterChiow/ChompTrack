
drop TABLE RecipeIntolerance;
drop TABLE RecipeRestrictions;
drop TABLE MealPlans;
drop TABLE UserIntolerances;
drop TABLE UserDietaryRestrictions;
drop TABLE RecipesIngredients;
drop TABLE Ingredients;
drop TABLE Recipes;
drop TABLE Users;

USE ChompTrack;

CREATE TABLE IF NOT EXISTS Users (
     user_id INT PRIMARY KEY AUTO_INCREMENT,
     username VARCHAR(50) NOT NULL UNIQUE,
     name VARCHAR(50),
     email VARCHAR(100) NOT NULL UNIQUE,
     password VARCHAR(100) NOT NULL,
     gender ENUM('Male', 'Female'),
     activityLevel ENUM('SedentaryActive', 'LightlyActive', 'ModeratelyActive', 'VeryActive','SuperActive'),

-- User attributes
     height DECIMAL(5, 2),  -- Example: height of the user in cm
     weight DECIMAL(5, 2),  -- Example: weight of the user in kg
     age INT,

-- User intake
     protein INT,
     fats INT,
     carbohydrates INT,
     calories INT,

    completed BOOLEAN DEFAULT FALSE
);




CREATE TABLE IF NOT EXISTS UserDietaryRestrictions (
    user_id INT NOT NULL,
    restriction_name enum(
        'Gluten_free','Ketogenic', 'Vegan',
        'Vegetarian', 'Pescetarian', 'Paleo',
        'Primal', 'Low_FODMAP', 'Whole30'
        ),
    PRIMARY KEY (user_id, restriction_name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS UserIntolerances (
    user_id INT NOT NULL ,
    intolerance_name enum (
        'Dairy', 'Egg', 'Gluten',
        'Grain', 'Peanut', 'Seafood',
        'Sesame','Shellfish', 'Soy',
        'Sulfite', 'Tree Nut', 'Wheat'
        ),
    PRIMARY KEY (user_id, intolerance_name),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS Recipes (
    recipe_id INT PRIMARY KEY,
    recipe_name VARCHAR(100) NOT NULL,

    cuisine_type VARCHAR(100),

    breakfast BOOLEAN,
    lunch BOOLEAN,
    dinner BOOLEAN,
    snack BOOLEAN,
    cooking_time INT, -- in minutes
    total_price DECIMAL (10,2) NOT NULL,
    image LINESTRING,
    protein INT,
    fats INT,
    carbohydrates INT,
    calories INT,
    recipe_instructions LINESTRING NOT NULL
);

CREATE TABLE IF NOT EXISTS RecipeIntolerance (
    recipe_id INT NOT NULL,
    intolerance_name ENUM (
    'Dairy', 'Egg', 'Gluten',
    'Grain', 'Peanut', 'Seafood',
    'Sesame', 'Shellfish', 'Soy',
    'Sulfite', 'Tree Nut', 'Wheat'
    ) NOT NULL,
    PRIMARY KEY (recipe_id, intolerance_name),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS RecipeRestrictions (
    recipe_id INT NOT NULL,
    restriction_name ENUM (
    'Gluten_free', 'Ketogenic',
    'Vegetarian', 'Vegan', 'Pescetarian', 'Paleo',
    'Primal', 'Low_FODMAP', 'Whole30'
    ) NOT NULL,
    PRIMARY KEY (recipe_id, restriction_name),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS Ingredients ( -- all ingredients
   ingredient_id INT PRIMARY KEY AUTO_INCREMENT,
   name VARCHAR(100) NOT NULL,
   price_per_unit DECIMAL(10, 2) NOT NULL
);



CREATE TABLE IF NOT EXISTS RecipesIngredients ( -- links ingredients to recipes
    recipe_id INT,
    ingredient_id INT,
    quantity DECIMAL(10,2) NOT NULL,
    measurements LINESTRING,
    PRIMARY KEY (recipe_id,ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id) ON DELETE CASCADE
);


-- Create MealPlans Table

CREATE TABLE IF NOT EXISTS MealPlans (
    meal_plan_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    date DATE NOT NULL,
    completed BOOLEAN NOT NULL,  
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE

);

ALTER TABLE Recipes ADD COLUMN spoonacular_id INT UNIQUE;
ALTER TABLE Recipes MODIFY image VARCHAR(300);
ALTER TABLE Recipes MODIFY recipe_instructions VARCHAR(300);
ALTER TABLE RecipesIngredients MODIFY measurements VARCHAR(20);
ALTER TABLE MealPlans
    ADD COLUMN meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL;