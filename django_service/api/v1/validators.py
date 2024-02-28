from django.core.exceptions import ValidationError


def name_validator(value: str) -> str | None:
    """Проверяет, что поле name состоит только из букв и/или пробелов."""
    if all(x.isalpha() or x.isspace() for x in value):
        return value
    else:
        raise ValidationError("Название посылки может содержать только буквы или пробелы!")
