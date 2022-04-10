
from collections import deque

from .types import Package


class PickupBox:
    """
        Represents a box of packages to deliver
    """
    _max_packages = 64

    def __init__(self, packages: list[Package] | None = None) -> None:
        self.__packages = deque(maxlen=self._max_packages)  # type: deque[Package]
        if packages:
            self.add_packages(packages)

    def __len__(self) -> int:
        return len(self.__packages)

    @property
    def size(self) -> int:
        return len(self)

    @classmethod
    def max_size(cls) -> int:
        return cls._max_packages

    @property
    def can_append(self) -> int:
        return self.max_size() - self.size

    @property
    def packages(self) -> list[Package]:
        return list(self.__packages)

    def add_package(self, package: Package) -> None:
        if self.can_append < 1:
            raise ValueError('Too many packages for pick up one more')
        self.__packages.append(package)

    def add_packages(self, packages: list[Package]) -> None:
        if self.can_append < len(packages):
            raise ValueError(f'Too many packages for pick up more: {len(packages)}')
        self.__packages.extend(packages)

    def next_package(self) -> Package | None:
        if self.__packages:
            return self.__packages.popleft()
