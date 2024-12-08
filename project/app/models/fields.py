"""pydantic fields that may be reused"""

from enum import Enum
from typing import NamedTuple
from functools import partial

from sqlalchemy import Column
from sqlmodel import Field


# These are useful to set the values in one place
# where they can also be used by unit testing
class Range(NamedTuple):
    """
    Represents the min and max value for a validation constant
    """

    min: int | float
    max: int | float


class ValidationConstant(Enum):
    """
    This enumeration holds validation constants useful when setting
    ge and le (etc.) values in Pydantic models. Having this as a class
    also makes it available for unit tests.
    """

    STRING_10 = Range(min=0, max=10)
    STRING_20 = Range(min=0, max=20)
    STRING_24 = Range(min=0, max=24)
    STRING_30 = Range(min=0, max=30)
    STRING_40 = Range(min=0, max=40)
    STRING_60 = Range(min=0, max=60)
    STRING_70 = Range(min=0, max=70)
    STRING_80 = Range(min=0, max=80)
    STRING_120 = Range(min=0, max=120)
    STRING_160 = Range(min=0, max=160)
    STRING_200 = Range(min=0, max=200)
    STRING_220 = Range(min=0, max=220)


def create_string_field(
    validation_constant: ValidationConstant,
    default: str = "",
    nullable: bool = True,
    title: str = "",
    description: str = "",
    mapped_name: str = "",
) -> Field:
    """
    Factory function to create string fields with specific validation constraints
    """
    return Field(
        default=default,
        min_length=validation_constant.value.min,
        max_length=validation_constant.value.max,
        title=title,
        description=description,
        sa_column=Column(mapped_name, nullable=nullable),
    )


# Create partial functions for specific field types
String10Field = partial(create_string_field, ValidationConstant.STRING_10)
String20Field = partial(create_string_field, ValidationConstant.STRING_20)
String24Field = partial(create_string_field, ValidationConstant.STRING_24)
String30Field = partial(create_string_field, ValidationConstant.STRING_30)
String40Field = partial(create_string_field, ValidationConstant.STRING_40)
String60Field = partial(create_string_field, ValidationConstant.STRING_60)
String70Field = partial(create_string_field, ValidationConstant.STRING_70)
String80Field = partial(create_string_field, ValidationConstant.STRING_80)
String120Field = partial(create_string_field, ValidationConstant.STRING_120)
String160Field = partial(create_string_field, ValidationConstant.STRING_160)
String200Field = partial(create_string_field, ValidationConstant.STRING_200)
String220Field = partial(create_string_field, ValidationConstant.STRING_220)
