from server.controllers.filter.FilterInterface import FilterInterface

class TimeFilter(FilterInterface):
    """
    A filter that applies a time range to a list of recipes.

    Attributes:
        min_time (int): The minimum preparation time to filter recipes by (in minutes).
        max_time (int): The maximum preparation time to filter recipes by (in minutes).
    """
    def __init__(self, parameters:list)->None:
        """
        Initializes the TimeFilter with the provided time parameters.

        Args:
            parameters (list): A list where:
                - parameters[0] is the minimum preparation time (int).
                - parameters[1] is the maximum preparation time (int).
        """
        print(parameters)
        self.min_time = parameters[0]
        self.max_time = parameters[1]

    def apply(self, recipeList: list)->list:
        """
        Filters the provided list of recipes by the preparation time range.

        Args:
            recipeList (list): A list of recipe dictionaries. Each recipe must contain a 'prepTime' key,
                               representing the preparation time in minutes.

        Returns:
            list: A list of recipes that have preparation times within the defined range.
        """
        filteredRecipes=[]
        for recipe in recipeList:
            if self.min_time <= recipe['prepTime'] <= self.max_time:
                filteredRecipes.append(recipe)
        return filteredRecipes