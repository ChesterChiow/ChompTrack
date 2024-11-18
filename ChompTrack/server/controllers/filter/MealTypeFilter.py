from server.controllers.filter.FilterInterface import FilterInterface

class MealTypeFilter(FilterInterface):
    """
    A filter that applies a meal type filter to a list of recipes.

    Attributes:
        selected_meal_types (list): A list of selected meal types to filter recipes by.
                                    This could include values like 'Breakfast', 'Lunch', 'Dinner', 'Snack'.
    """
    def __init__(self, selected_meal_types:list)->None:
        """
        Initializes the MealTypeFilter with the selected meal types.

        Args:
            selected_meal_types (list): A list of meal types to filter recipes by. Each element
                                        should be a string representing a meal type, such as 'Breakfast',
                                        'Lunch', 'Dinner', or 'Snacks'.
        """
        self.selected_meal_types = selected_meal_types

    def apply(self, recipeList:list)->list:
        """
        Filters the provided list of recipes by the selected meal types.

        Args:
            recipeList (list): A list of recipe dictionaries. Each recipe must contain keys like
                               'Breakfast', 'Lunch', 'Dinner', and 'Snack', which are boolean values
                               indicating whether the recipe belongs to that meal type.

        Returns:
            list: A list of recipes that match the selected meal types.
        """
        filteredRecipes=[]
        for recipe in recipeList:
            if recipe['Breakfast'] and 'Breakfast' in self.selected_meal_types:
                filteredRecipes.append(recipe)
            elif recipe['Lunch'] and 'Lunch' in self.selected_meal_types:
                filteredRecipes.append(recipe)
            elif recipe['Dinner'] and 'Dinner' in self.selected_meal_types:
                filteredRecipes.append(recipe)
            elif recipe['Snack'] and 'Snacks' in self.selected_meal_types:
                filteredRecipes.append(recipe)
        return filteredRecipes