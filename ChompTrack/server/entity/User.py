from server.DatabaseCtrl.DBFactory import DBFactory

class User:
    def __init__(self, user_id: int = None, username=None, email=None, gender=None,
                 activity_level=None, height=None, weight=None, age=None,
                 protein=None, fats=None, carbohydrates=None, calories=None) -> None:

        self.user_id: int = user_id
        self.username: str = username
        self.email: str = email
        self.gender: str = gender
        self.activity_level: str = activity_level
        self.height: int = height
        self.weight: int = weight
        self.age: int = age
        self.protein: float = protein
        self.fats: float = fats
        self.carbohydrates: float = carbohydrates
        self.calories: float = calories
        self.logged_in: bool = False
        self.register_complete: bool = False
        self.userQueries = DBFactory().create_db_connection("User")

    def complete_register(self):
        self.userQueries.update_completed(self.user_id)
        self.register_complete = True

    def get_register_complete(self) -> bool:
        if not self.user_id:
            print("User ID not set. Cannot load attributes.")
            return False

        self.register_complete = self.userQueries.fetch_completed_status(self.user_id)
        attributes = self.userQueries.logging_in_user(self.user_id)

        if attributes:
            self.username = attributes.get('username')
            self.gender = attributes.get('gender')
            self.activity_level = attributes.get('activity_level')
            self.height = attributes.get('height')
            self.weight = attributes.get('weight')
            self.age = attributes.get('age')
            self.protein = attributes.get('protein')
            self.fats = attributes.get('fats')
            self.carbohydrates = attributes.get('carbohydrates')
            self.calories = attributes.get('calories')
            self.register_complete = True
            print(f"Attributes loaded for user ID {self.user_id}")
        else:
            print("No attributes found for the specified user ID.")
        return self.register_complete

    def get_actual_intake(self, date: str) -> dict:
        intake = self.userQueries.get_user_intake(date, self.user_id)
        return {
            'protein': intake['protein'],
            'fats': intake['fats'],
            'carbohydrates': intake['carbohydrates'],
            'calories': intake['calories']
        }

    def is_logged_in(self) -> bool:
        return self.logged_in

    def login_user(self):
        self.logged_in = True

    def get_Basal_Metabolic_Rate(self) -> float:
        if self.gender == 'Male':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        elif self.gender == 'Female':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
        else:
            raise ValueError("Gender must be 'Male' or 'Female'")

    def get_TDEE(self) -> float:
        bmr = self.get_Basal_Metabolic_Rate()
        activity_multiplier = {
            'SedentaryActive': 1.2,
            'LightlyActive': 1.375,
            'ModeratelyActive': 1.55,
            'VeryActive': 1.6,
            'SuperActive': 1.9
        }
        multiplier = activity_multiplier.get(self.activity_level)
        if multiplier is None:
            raise ValueError("Invalid activity level.")
        return bmr * multiplier

    def get_protein_needs(self) -> float:
        weight_kg = self.weight
        if self.activity_level in ['SedentaryActive', 'LightlyActive']:
            protein_range = (1.0, 1.2)
        elif self.activity_level in ['ModeratelyActive', 'VeryActive', 'SuperActive']:
            protein_range = (1.4, 2.2)
        else:
            raise ValueError("Invalid activity level.")
        return round(weight_kg * sum(protein_range) / 2)

    def get_fat_needs(self) -> int:
        return round(self.weight * 1.0)

    def get_carbohydrate_needs(self) -> float:
        tdee = self.get_TDEE()
        carb_calories = (tdee * 0.45 + tdee * 0.65) / 2
        return round(carb_calories / 4)

    def update_all_attributes(self, user_id=None, username=None, email=None, gender=None,
                              activity_level=None, height=None, weight=None, age=None,
                              protein=None, fats=None, carbohydrates=None, calories=None, logged_in=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.gender = gender or self.gender
        self.activity_level = activity_level or self.activity_level
        self.height = height or self.height
        self.weight = weight or self.weight
        self.age = age or self.age
        self.protein = protein or self.protein
        self.fats = fats or self.fats
        self.carbohydrates = carbohydrates or self.carbohydrates
        self.calories = calories or self.calories
        self.logged_in = logged_in

    def any_fields_empty(self) -> bool:
        return any(
            attr is None for attr in [
                self.gender, self.activity_level, self.height,
                self.weight, self.age, self.protein, self.fats,
                self.carbohydrates, self.calories, self.logged_in
            ]
        )

    def __repr__(self) -> str:
        return (f"User(user_id={self.user_id}, username='{self.username}', email='{self.email}', "
                f"gender='{self.gender}', activity_level='{self.activity_level}', height={self.height}, "
                f"weight={self.weight}, age={self.age}, protein={self.protein}, fats={self.fats}, "
                f"carbohydrates={self.carbohydrates}, calories={self.calories}, logged_in={self.logged_in})")