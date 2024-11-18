class FilterInterface:
    """
    An abstract interface class for recipe filters.

    This interface defines the structure for filters that can be applied to a list of recipes.
    Any filter class inheriting from FilterInterface must implement the `apply` method.
    """
    def apply(self, recipeList:list) -> list:
        """
        Applies a filtering criterion to a list of recipes.

        This method must be implemented by subclasses. It should take a list of recipes as input,
        apply a specific filtering criterion, and return the filtered list.

        Args:
            recipeList (list): A list of recipes to filter.

        Returns:
            list: The filtered list of recipes.

        Raises:
            NotImplementedError: If a subclass does not implement this method.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")