
from unittest import TestCase
import asyncio

from pickaper.pickup_car import PickupCar, DeliveryStatus
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
            result = loop.run_until_complete(coro)  # type: DeliveryStatus

        self.assertFalse(result.car_was_broken)
        self.assertEqual(len(result.delivered), 5)
        self.assertEqual(len(result.incorrect_address), 0)
        self.assertIsNone(result.to_be_redelivered)

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
            result = loop.run_until_complete(coro)  # type: DeliveryStatus

        self.assertTrue(result.car_was_broken)
        self.assertEqual(len(result.delivered), 2)
        self.assertEqual(len(result.incorrect_address), 0)
        self.assertIsNotNone(result.to_be_redelivered)
        self.assertEqual(len(result.to_be_redelivered.packages), 3)

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
            result = loop.run_until_complete(coro)  # type: DeliveryStatus

        self.assertFalse(result.car_was_broken)
        self.assertEqual(len(result.delivered), 4)
        self.assertEqual(len(result.incorrect_address), 1)
        self.assertEqual(result.incorrect_address[0].idx, 1)  # id of 2nd package is 1
        self.assertIsNone(result.to_be_redelivered)

