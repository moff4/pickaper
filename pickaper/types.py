
from dataclasses import dataclass
from enum import IntEnum


class CarBrokenError(Exception):
    pass


class IncorrectAddressError(Exception):
    pass


class PackingType(IntEnum):
    ENVELOPE = 0
    BOX = 1
    TUBE = 2
    ROLL = 3


@dataclass
class Package:
    idx: int  # Unique identifier of a package
    dimensions: tuple[int, int, int]  # Length, width, height in cm
    weight: float  # Weight in kg
    type: PackingType
