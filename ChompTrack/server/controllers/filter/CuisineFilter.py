from server.controllers.filter.FilterInterface import FilterInterface

class CuisineFilter(FilterInterface):
    """
    A filter that applies a cuisine filter to a list of recipes.

    Attributes:
        selectedCuisines (list): A list of selected cuisines to filter recipes by.
                                  Each element should be a string representing a cuisine, such as 'Italian',
                                  'Chinese', 'Indian', etc.
    """

    def __init__(self, selectedCuisines:list):
        """
        Initializes the CuisineFilter with the selected cuisines.

        Args:
            selectedCuisines (list): A list of cuisines to filter recipes by. Each element
                                      should be a string representing a cuisine type, such as 'Italian',
                                      'Chinese', 'Mexican', etc.
        """
        self.selectedCuisines = selectedCuisines

    def apply(self, recipeList: list) -> list:
        """
        Filters the provided list of recipes by the selected cuisines.

        Args:
            recipeList (list): A list of recipe dictionaries. Each recipe should contain a key 'cuisine' 
                               with a value representing the cuisine type (e.g., 'Italian', 'Chinese').

        Returns:
            list: A list of recipes that match one of the selected cuisines.
        """
        filteredRecipes=[]
        for recipe in recipeList:
            if recipe['cuisine'] in self.selectedCuisines:
                filteredRecipes.append(recipe)
        return filteredRecipes