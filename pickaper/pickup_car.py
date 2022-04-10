
import asyncio
import logging
import random

from .pickup_box import PickupBox
from .types import CarBrokenError, IncorrectAddressError, Package


class PickupCar:

    logger = logging.getLogger(__name__)

    """
        A car can only pickup a box of packages and the driver will deliver them one by one
    """
    async def deliver_box(self, pickup_box: PickupBox) -> PickupBox | None:
        """
            Deliver box of packages
            :param pickup_box: box of packages to deliver
            :return: PickupBox with packages to be redelivered or None if all packages were delivered
        """
        to_be_redelivered = []

        while package := pickup_box.next_package():
            try:
                await self.__deliver_package(package)
                self.logger.info('package delivered! :)')
            except CarBrokenError:
                pickup_box.add_package(package)
                self.logger.error('car was broken :(')
                break
            except IncorrectAddressError:
                self.logger.error('incorrect address :(')
                to_be_redelivered.append(package)

        pickup_box.add_packages(to_be_redelivered)
        return pickup_box if pickup_box.size else None

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
