"""
Taken from
https://github.com/mahenzon/ri-sdk-python-wrapper/blob/master/ri_sdk_codegen/utils/case_converter.py
"""
import uuid
from enum import Enum


def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    """
    chars = []
    for c_idx, char in enumerate(input_str):
        if c_idx and char.isupper():
            nxt_idx = c_idx + 1
            # idea of the flag is to separate abbreviations
            # as new words, show them in lower case
            flag = nxt_idx >= len(input_str) or input_str[nxt_idx].isupper()
            prev_char = input_str[c_idx - 1]
            if prev_char.isupper() and flag:
                pass
            else:
                chars.append("_")
        chars.append(char.lower())
    return "".join(chars)


def generate_uuid():
    return str(uuid.uuid4())


class UserRoleEnum(Enum):
    ADMIN = "admin"
    USER = "user"
    BARMAN = "barmen"


class ItemEnum(Enum):
    LITER = "L"
    KILOGRAMS = "KG"
    QUANTITY = "Q"


class IngredientUnitEnum(Enum):
    LITER = "L"
    MILLILITER = "ML"
    KILOGRAMS = "KG"
    GRAM = "G"
    QUANTITY = "Q"


class SizeEnum(Enum):
    SMALL = "samll"
    MEDIUM = "medium"
    LARGE = "large"


class ColorEnum(Enum):
    RED = "red"
    BLUE = "blue"
    GREY = "grey"
    YELLOW = "yellow"
    PINK = "pink"
