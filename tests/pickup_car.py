
from unittest import TestCase
import asyncio

from pickaper.pickup_car import PickupCar
from pickaper.pickup_box import PickupBox
from pickaper.types import Package, PackingType, CarBrokenError, IncorrectAddressError

from .tools import Mock

loop = asyncio.get_event_loop()


class PickupCarCase(TestCase):
    def test_ok(self) -> None:
        async def always_deliver(package):
            return package

        car = PickupCar()
        with Mock(car, '_PickupCar__deliver_package', always_deliver):
            coro = car.deliver_box(
                PickupBox(
                    [
                        Package(i, (1, 1, 1), 3, PackingType.BOX)
                        for i in range(5)
                    ]
                )
            )
            result = loop.run_until_complete(coro)

        self.assertIsNone(result)

    def test_car_broken(self) -> None:
        counter = 0

        async def car_broken_after_3(package):
            nonlocal counter
            counter += 1
            if counter == 3:
                raise CarBrokenError()
            return package

        car = PickupCar()
        with Mock(car, '_PickupCar__deliver_package', car_broken_after_3):
            coro = car.deliver_box(
                PickupBox(
                    [
                        Package(i, (1, 1, 1), 3, PackingType.BOX)
                        for i in range(5)
                    ]
                )
            )
            result = loop.run_until_complete(coro)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 3)

    def test_invalid_address(self) -> None:
        counter = 0

        async def incorrect_address_on_2(package):
            nonlocal counter
            counter += 1
            if counter == 2:
                raise IncorrectAddressError()
            return package

        car = PickupCar()
        with Mock(car, '_PickupCar__deliver_package', incorrect_address_on_2):
            coro = car.deliver_box(
                PickupBox(
                    [
                        Package(i, (1, 1, 1), 3, PackingType.BOX)
                        for i in range(5)
                    ]
                )
            )
            result = loop.run_until_complete(coro)

        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.packages[0].idx, 1)  # id of 2nd package is 1

