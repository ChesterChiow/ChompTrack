class DBFactory():
    def __init__(self) -> None:
        self.db = None

    def create_db_connection(self, type: str) -> object:
        from server.DatabaseCtrl.MealPlanQueries import MealPlanQueries
        from server.DatabaseCtrl.RecipeQueries import RecipeQueries
        from server.DatabaseCtrl.UserQueries import UserQueries
        from server.DatabaseCtrl.IngredientQueries import IngredientQueries
        """
        Create a database connection based on types provided
        Args:
            type: string of the type of connection required. Ingredient, Recipe, MealPlan and User.

        Returns: Connection Object with queries to db.

        """
        if type == "Ingredient":
            return IngredientQueries()
        elif type == "Recipe":
            return RecipeQueries()
        elif type == "MealPlan":
            return MealPlanQueries()
        elif type == "User":
            return UserQueries()
        else:
            return None
