from server.controllers.filter.FilterInterface import FilterInterface

class CostFilter(FilterInterface):
    """
    A filter that applies a cost range to a list of recipes.

    Attributes:
        min_cost (float): The minimum cost value to filter recipes by.
        max_cost (float): The maximum cost value to filter recipes by.
    """
     
    def __init__(self, parameters:list)->None:
        """
        Initializes the CostFilter with the provided cost parameters.

        Args:
            parameters (list): A list where:
                - parameters[0] is the minimum cost (float).
                - parameters[1] is the maximum cost (float).
        """
        self.min_cost = parameters[0]
        self.max_cost = parameters[1]

    def apply(self, recipeList:list)->list:
        """
        Filters the provided list of recipes by the cost range defined in the filter.

        Args:
            recipeList (list): A list of recipe dictionaries. Each recipe must contain a 'cost' key, 
                               representing the cost in cents.

        Returns:
            list: A list of recipes that fall within the cost range.
        """
        filteredRecipes=[]
        for recipe in recipeList:
            if self.min_cost <= (recipe['cost']/100) <= self.max_cost:
                filteredRecipes.append(recipe)
        return filteredRecipes
