class FilterCtrl:
    """
    A controller class that applies multiple filters to a list of recipes.

    Attributes:
        recipeList (list): A list of recipes to be filtered. Each recipe is expected to be a dictionary containing
                            various attributes, such as 'cost', 'prepTime', 'cuisine', etc.
        filters (list): A list of filter objects that will be applied to the recipe list.
    """
    def __init__(self, recipeList:list) -> None:
        """
        Initializes the FilterCtrl with the given recipe list.

        Args:
            recipeList (list): A list of recipes to be filtered. Each recipe should be a dictionary containing
                                various attributes such as 'cost', 'prepTime', 'cuisine', etc.
        """
        self.recipeList = recipeList
        self.filters =[]

    def add_filter(self, filter_obj:object) -> None:
        """
        Adds a filter object to the list of filters.

        Args:
            filter_obj (object): A filterInterface object that should implement an 'apply' method.
                                  This can be any filterInterface class (e.g., CostFilter, TimeFilter, etc.).
        """
        self.filters.append(filter_obj)

    def apply_filters(self) -> list:
        """
        Applies all filters to the recipe list and returns the filtered list.

        Iterates over the list of filters and applies each filter to the recipe list in sequence.
        The final filtered recipe list is returned.

        Returns:
            dict: A dictionary containing the filtered recipe list under the key 'filteredRecipeList'.
        """
        filteredRecipeList = self.recipeList
        for filter_obj in self.filters:
            filteredRecipeList = filter_obj.apply(filteredRecipeList)
            print(filteredRecipeList)
        return {'filteredRecipeList': filteredRecipeList}


