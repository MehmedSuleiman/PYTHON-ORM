from django.core.exceptions import ValidationError


def name_validator(value):
        for ch in value:
            if not (ch.isalpha() or ch == " "):
                raise ValidationError(message="Name can only contain letters and spaces")
