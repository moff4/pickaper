
import asyncio

from .pickup_box import PickupBox
from .pickup_box_queue import PickupBoxQueue
from .pickup_car import PickupCar


class Logist:
    def __init__(self, to_deliver: PickupBoxQueue, to_redeliver: asyncio.Queue[PickupBox]) -> None:
        self.to_deliver = to_deliver
        self.to_redeliver = to_redeliver

    async def personal_logic(self, car: PickupCar) -> None:
        while True:
            box = await self.to_deliver.pop()
            if undelivered_box := await car.deliver_box(box):
                await self.to_redeliver.put(undelivered_box)

    async def process_deliveries(self, cars: list[PickupCar]) -> None:
        await asyncio.gather(
            *[
                self.personal_logic(car)
                for car in cars
            ]
        )
