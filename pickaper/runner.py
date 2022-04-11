
import asyncio
import logging
from asyncio import Queue
from typing import Iterable

from .delivary_generator import DeliveryGenerator
from .logist import Logist
from .pickup_box import PickupBox
from .pickup_box_queue import PickupBoxQueue
from .pickup_car import PickupCar
from .types import Package

logger = logging.getLogger(__name__)


async def packer(packages: Iterable[Package], pickup_box_queue: PickupBoxQueue) -> None:
    """
        coroutine that consume package generator and produce to pickup_box_queue
        :param packages:
        :param pickup_box_queue:
        :return: None
    """
    for package in packages:
        await pickup_box_queue.push_package(package)


async def redeliver(to_redeliver: Queue[PickupBox], pickup_box_queue: PickupBoxQueue) -> None:
    """
        coroutine that consume undelivered package queue and produce to pickup_box_queue
        :param to_redeliver:
        :param pickup_box_queue:
        :return:
    """
    while True:
        box = await to_redeliver.get()
        await pickup_box_queue.push_box(box)


async def start_delivery(cars_count: int) -> None:
    """
        main start function, creates queues, package generator, cars and start delivery
        :param cars_count:
        :return: None
    """
    logger.info('setting up')
    delivery_generator = DeliveryGenerator()
    cars = [PickupCar() for _ in range(cars_count)]

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
