from enum import IntEnum, Enum


__all__ = [
    "PydanticIntEnum",
    "PydanticStringEnum",
]


class PydanticIntEnum(IntEnum):
    """Version of Int enum which can be validated through Pydantic

    by int as "value"
    > > > SomeEnum(1)
    <SomeEnum.red: 1>

    by str as "name"
    > > > SomeEnum['red']
    <SomeEnum.RED: 1>
    """

    # ===== methods for Pydantic validations =====
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, var: object):
        if isinstance(var, str):
            return cls[var]
        elif isinstance(var, int):
            # noinspection PyArgumentList
            return cls(var)
        elif issubclass(var.__class__, cls):
            return var
        else:
            raise ValueError(f'Value must be "int" or "str", not {var.__class__}')


class PydanticStringEnum(str, Enum):
    """Version of String enum which can be validated through Pydantic

    by str as name or value of enum fields
    > > > SomeEnum['red']
    <SomeEnum.RED: 1>

    > > > SomeEnum('red')
    <SomeEnum.RED: 1>
    """

    # ===== methods for Pydantic validations =====
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, var: object):
        if isinstance(var, str):
            # noinspection PyArgumentList
            return cls(var)
        elif issubclass(var.__class__, cls):
            return var
        else:
            raise ValueError(f'Value must "str", not {var.__class__}')


def test_pydantic_validation():
    from pydantic import BaseModel

    class IntColors(PydanticIntEnum):
        blue = 1
        red = 2

    class StringColors(PydanticStringEnum):
        blue = "blue"
        red = "red"

    assert IntColors(1).value == 1, "Error getting int value enum using __call__()"
    assert IntColors["red"].value == 2, "Error getting int value enum using __getitem__()"

    assert StringColors("blue").value == "blue", "Error getting string value enum using __call__()"
    assert StringColors["red"].value == "red", "Error getting string value enum using __getitem__()"

    class Palette(BaseModel):
        class Config:
            validate_assignment = True

        id: int
        primary_color: IntColors
        second_color: StringColors

    primitive_palette = Palette(id=1, primary_color=1, second_color="red")
    assert primitive_palette.primary_color == IntColors.blue and primitive_palette.second_color == StringColors.red

    enums_palette = Palette(id=2, primary_color=IntColors.blue, second_color=StringColors.red)
    assert enums_palette.primary_color == IntColors.blue and enums_palette.second_color == StringColors.red
