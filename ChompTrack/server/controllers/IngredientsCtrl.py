from server.entity.Ingredient import Ingredient

class IngredientsCtrl:
    def save_ingredients_with_recipe(self, recipe_id: int, ingredients: list[dict]) -> None:
        """
        Save ingredients associated with a recipe.

        :param recipe_id: The ID of the recipe to which ingredients belong.
        :param ingredients: A list of ingredient dictionaries containing details.
        """
        for ingredient in ingredients:
            ingredient_data = {
                'name': ingredient.get('name'),
                'price': ingredient.get('price'),
                'amount': ingredient.get('amount', {}).get('metric', {}).get('value'),
                'unit': ingredient.get('amount', {}).get('metric', {}).get('unit')
            }
            print(ingredient_data)

            ingredient_instance = Ingredient(**ingredient_data)
            print(ingredient_instance.name, ingredient_instance.priceperunit, ingredient_instance.amount, ingredient_instance.measurement)

            ingredient_instance.save(recipe_id)

    def get_grocery_list(self, user_id: int, start_date: str, end_date: str) -> dict:
        """
        Get a grocery list of ingredients for a user within a specified date range.

        :param user_id: The ID of the user requesting the grocery list.
        :param start_date: The start date for the grocery list in DD-MM-YYYY format.
        :param end_date: The end date for the grocery list in DD-MM-YYYY format.
        :return: A dictionary representing the grocery list.
        """
        results = Ingredient().get_grocery_ingredients(user_id, start_date, end_date)
        grocery_list = {}

        print(results)
        for index, row in enumerate(results, start=1):
            ingredient_name = row[0]
            amount = float(row[1])
            measurement = row[2]
            price = float(row[3]) / 100  # Convert price to appropriate format
            quantity = row[4]

            grocery_list[index] = {
                "name": ingredient_name,
                "amount": amount,
                "measurement": measurement,
                "quantity": quantity,
                "price": price
            }

        return grocery_list


if __name__ == '__main__':
    ingredientsCtrl = IngredientsCtrl()
    ingredientsCtrl.save_ingredients_with_recipe(
        recipe_id=1,
        ingredients=[{'name': 'carrot', 'image': 'sliced-carrot.png', 'price': 33.71,
                      'amount': {'metric': {'value': 192.0, 'unit': 'g'},
                                 'us': {'value': 1.5, 'unit': 'cup'}}}]
    )