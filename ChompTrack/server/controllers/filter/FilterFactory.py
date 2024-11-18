from server.controllers.filter.CuisineFilter import CuisineFilter
from server.controllers.filter.MealTypeFilter import MealTypeFilter
from server.controllers.filter.CostFilter import CostFilter
from server.controllers.filter.TimeFilter import TimeFilter

class FilterFactory:
    """
    A factory class for creating filter objects based on filter type.

    The FilterFactory class provides a static method to create and return the appropriate
    filter object for a given filter type. Each filter object can be used to apply a specific
    filtering criterion to a list of recipes.
    """
    @staticmethod
    def get_filter(filter_type:str, filter_parameter:list) -> object:
        """
        Creates and returns a filter object based on the specified filter type.

        Args:
            filter_type (str): The type of filter to create. Options include 'cuisine', 'mealType', 'cost', and 'time'.
            filterParameter (list): The parameters required by the specified filter type.

        Returns:
            object: An instance of a filterInterface class (e.g., `CuisineFilter`, `MealTypeFilter`, `CostFilter`, or `TimeFilter`).

        Raises:
            ValueError: If the specified filter type is not recognized.
        """
        if filter_type == 'cuisine':
            return CuisineFilter(filter_parameter)
        elif filter_type == 'mealType':
            return MealTypeFilter(filter_parameter)
        elif filter_type == 'cost':
            return CostFilter(filter_parameter)
        elif filter_type == 'time':
            return TimeFilter(filter_parameter)
        else:
            raise ValueError(f"Unknown filter type: {filter_type}")