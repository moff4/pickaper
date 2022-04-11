
import asyncio
import logging
import random
from dataclasses import dataclass

from .pickup_box import PickupBox
from .types import CarBrokenError, IncorrectAddressError, Package


@dataclass
class DeliveryStatus:
    """
        status of delivery one PickupBox
    """
    car_was_broken: bool
    delivered: list[Package]
    incorrect_address: list[Package]
    to_be_redelivered: PickupBox | None


class PickupCar:
    """
        A car can only pickup a box of packages and the driver will deliver them one by one
    """

    logger = logging.getLogger(__name__)

    async def deliver_box(self, pickup_box: PickupBox) -> DeliveryStatus:
        """
            Deliver box of packages
            :param pickup_box: box of packages to deliver
            :return: PickupBox with packages to be redelivered or None if all packages were delivered
        """
        car_was_broken = False
        delivered = []
        incorrect_address = []

        while package := pickup_box.next_package():
            try:
                await self.__deliver_package(package)
                delivered.append(package)
            except CarBrokenError:
                car_was_broken = True
                pickup_box.add_package(package)
                break
            except IncorrectAddressError:
                incorrect_address.append(package)

        return DeliveryStatus(
            car_was_broken=car_was_broken,
            delivered=delivered,
            incorrect_address=incorrect_address,
            to_be_redelivered=pickup_box if pickup_box.size else None,
        )

    async def __deliver_package(self, package: Package) -> Package:
        """
            Deliver one package
            :param package: package to deliver
            :return: package if the delivery was successful
            :raises:
                - CarBrokenError
                - IncorrectAddressError
        """
        rnd = random.random()
        match rnd:
            case rnd if 0.95 < rnd <= 1:
                raise CarBrokenError()
            case rnd if 0.98 < rnd <= 0.99:
                raise IncorrectAddressError()
            case _:
                await asyncio.sleep(0.01)
                return package
