from server.entity.User import User

class UserCtrl:
    def __init__(self, user: User) -> None:
        """
        Initialize UserCtrl with a User instance.

        :param user: The User instance to manage.
        """
        self.user = user

    def update_username(self, username: str) -> None:
        """Update the user's username."""
        self.user.username = username

    def update_name(self, name: str) -> None:
        """Update the user's name."""
        self.user.name = name

    def update_email(self, email: str) -> None:
        """Update the user's email address."""
        self.user.email = email

    def update_gender(self, gender: str) -> None:
        """
        Update the user's gender. Must be 'Male' or 'Female'.

        :raises ValueError: If the gender is not 'Male' or 'Female'.
        """
        if gender not in ['Male', 'Female']:
            raise ValueError("Gender must be 'Male' or 'Female'")
        self.user.gender = gender

    def update_activity_level(self, activity_level: str) -> None:
        """
        Update the user's activity level.
        Adds 'Active' suffix and checks if it's valid.

        :raises ValueError: If the activity level is not one of the allowed levels.
        """
        valid_activity_levels = ['SedentaryActive', 'LightlyActive', 'ModeratelyActive', 'VeryActive', 'SuperActive']
        full_activity_level = activity_level + 'Active'
        if full_activity_level not in valid_activity_levels:
            raise ValueError("Invalid activity level.")
        self.user.activity_level = full_activity_level

    def update_height(self, height: float) -> None:
        """Update the user's height."""
        self.user.height = height

    def update_weight(self, weight: float) -> None:
        """Update the user's weight."""
        self.user.weight = weight

    def update_age(self, age: int) -> None:
        """Update the user's age."""
        self.user.age = age

    def recalculate_nutrition(self) -> None:
        """Recalculate nutrition values based on updated user attributes."""
        self.user.protein = self.user.get_protein_needs()
        self.user.fats = self.user.get_fat_needs()
        self.user.carbohydrates = self.user.get_carbohydrate_needs()
        self.user.calories = self.user.get_TDEE()

    def update_user_details(self, **kwargs: dict) -> None:
        """
        Update multiple user attributes at once.

        :raises ValueError: If an attribute does not exist on the user.
        """
        for key, value in kwargs.items():
            if hasattr(self.user, key):
                setattr(self.user, key, value)
            else:
                raise ValueError(f"User has no attribute '{key}'")

        # Recalculate nutrition after updating details
        self.recalculate_nutrition()

    def get_user_info(self) -> str:
        """Get a string representation of the user."""
        return str(self.user)

    def get_user_intakes(self, date: str) -> dict:
        """
        Get the user's actual intake for a specified date.

        :param date: Date in DD-MM-YYYY format.
        :return: Intake details for the specified date.
        """
        return self.user.get_intakes(date)