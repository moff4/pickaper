
import asyncio

from .pickup_box import PickupBox
from .pickup_box_queue import PickupBoxQueue
from .pickup_car import PickupCar


class Logist:
    """
        PickupBoxQueue consumer;
        routes PickupBoxes to PickupCars
    """
    def __init__(self, to_deliver: PickupBoxQueue, to_redeliver: asyncio.Queue[PickupBox]) -> None:
        self.to_deliver = to_deliver
        self.to_redeliver = to_redeliver

    async def _personal_logic(self, car: PickupCar) -> None:
        """
            aka single PickupCar consumer;
            consume boxes from queue and pass to the car
            :param car: PickupCar to be used for delivery
            :return:
        """
        while box := await self.to_deliver.pop():
            if undelivered_box := await car.deliver_box(box):
                await self.to_redeliver.put(undelivered_box)

    async def process_deliveries(self, cars: list[PickupCar]) -> None:
        """
            start consuming and routing
            :param cars: PickupCars that'll be used for routing
            :return:
        """
        await asyncio.gather(
            *[
                self._personal_logic(car)
                for car in cars
            ]
        )
