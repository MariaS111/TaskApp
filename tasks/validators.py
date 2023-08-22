from django.core.exceptions import ValidationError


def validate_not_main_board(value):
    if value == "Main board":
        raise ValidationError("This title is not allowed.")

