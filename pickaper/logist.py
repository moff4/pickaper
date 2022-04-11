# pylint: disable=logging-fstring-interpolation
import asyncio
import logging

from .pickup_box import PickupBox
from .pickup_box_queue import PickupBoxQueue
from .pickup_car import PickupCar, DeliveryStatus


class Logist:
    """
        PickupBoxQueue consumer;
        routes PickupBoxes to PickupCars
    """

    logger = logging.getLogger(__name__)

    def __init__(self, to_deliver: PickupBoxQueue, to_redeliver: asyncio.Queue[PickupBox]) -> None:
        self.to_deliver = to_deliver
        self.to_redeliver = to_redeliver

    async def process_status(self, status: DeliveryStatus) -> None:
        """

        :param status:
        :return:
        """
        if status.car_was_broken:
            if status.to_be_redelivered:
                self.logger.warning(f'car was broken; gonna redeliver {status.to_be_redelivered.size} packages')
                await self.to_redeliver.put(status.to_be_redelivered)
            else:
                self.logger.warning('car was broken; nothing to redeliver')

        for package in status.incorrect_address:
            self.logger.error(f'Package[{package.idx}] has incorrect address')

        for package in status.delivered:
            self.logger.info(f'Package[{package.idx}] delivered')

    async def _personal_logic(self, car: PickupCar) -> None:
        """
            aka single PickupCar consumer;
            consume boxes from queue and pass to the car
            :param car: PickupCar to be used for delivery
            :return:
        """
        while box := await self.to_deliver.pop():
            status = await car.deliver_box(box)
            await self.process_status(status)

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
