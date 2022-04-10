import asyncio
import logging
import os
from asyncio import Queue
from typing import Iterable

from .delivary_generator import DeliveryGenerator
from .logist import Logist
from .pickup_box import PickupBox
from .pickup_box_queue import PickupBoxQueue
from .pickup_car import PickupCar
from .types import Package

logger = logging.getLogger(__name__)


def set_logging() -> None:
    logging.basicConfig(
        format='%(asctime)s(%(name)s)[%(levelname)s]: %(message)s',
        level=logging.INFO,
    )


async def packer(packages: Iterable[Package], pickup_box_queue: PickupBoxQueue) -> None:
    for package in packages:
        await pickup_box_queue.push_package(package)


async def redeliver(to_redeliver: Queue[PickupBox], pickup_box_queue: PickupBoxQueue) -> None:
    while True:
        box = await to_redeliver.get()
        await pickup_box_queue.push_box(box)


async def main(args: list[str]) -> None:
    set_logging()

    logger.info('setting up')
    delivery_generator = DeliveryGenerator()
    cars = [PickupCar() for _ in range(os.cpu_count() or 8)]

    pickup_box_queue = PickupBoxQueue()
    redeliver_queue = Queue()  # type: Queue[PickupBox]
    logist = Logist(to_deliver=pickup_box_queue, to_redeliver=redeliver_queue)
    workers = [
        packer(packages=delivery_generator, pickup_box_queue=pickup_box_queue),
        redeliver(to_redeliver=redeliver_queue, pickup_box_queue=pickup_box_queue),
        logist.process_deliveries(cars)
    ]
    logger.info('start running')
    try:
        await asyncio.gather(*workers)
    except KeyboardInterrupt:
        logger.info('got KeyboardInterrupt; shutting down')
        pickup_box_queue.close()
