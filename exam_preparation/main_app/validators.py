from django.core.exceptions import ValidationError


def phone_validator(value):
    for i in value:
        if not value.isdigit():
            raise ValidationError('Phone number must be digits')

    return value