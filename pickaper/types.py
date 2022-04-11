
from dataclasses import dataclass
from enum import IntEnum


class CarBrokenError(Exception):
    """
        error to be thrown when pickupCar breaks
    """


class IncorrectAddressError(Exception):
    """
        error to be thrown when pickupCar gets package with incorrect address
    """


class PackingType(IntEnum):
    """
        class for package.type
    """
    ENVELOPE = 0
    BOX = 1
    TUBE = 2
    ROLL = 3


@dataclass
class Package:
    """
        dataclass for package
    """
    idx: int  # Unique identifier of a package
    dimensions: tuple[int, int, int]  # Length, width, height in cm
    weight: float  # Weight in kg
    type: PackingType
