
import random
from typing import Iterator

from .types import Package, PackingType


class DeliveryGenerator:
    """
    Generates new packages for delivery
    """
    def __iter__(self) -> Iterator[Package]:
        return self.__generate()

    @staticmethod
    def __generate() -> Iterator[Package]:
        idx = 0
        while True:
            package_type = random.choice(list(PackingType))
            dimensions = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 10))
            weight = random.random() * 100
            package = Package(idx=idx, dimensions=dimensions, weight=weight, type=package_type)
            idx += 1
            yield package
