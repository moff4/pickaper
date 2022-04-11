
import asyncio
import logging
from collections import deque

from .pickup_box import PickupBox
from .types import Package


class PickupBoxQueue:
    """
        Queue that has packages and boxes as input and only boxes as output
        (throwing packages into boxes)
    """

    logger = logging.getLogger(__name__)

    def __init__(self, max_size: int = 32) -> None:
        """
            :param max_size: max size of this queue
        """
        self._package_buffer = deque()  # type: deque[Package]
        self._queue = asyncio.Queue(maxsize=max_size)  # type: asyncio.Queue[PickupBox]

    def _buffer_to_box(self) -> PickupBox:
        """
            create box with packages from cls._package_buffer and clear cls._package_buffer
            :return: new box
        """
        box = PickupBox(packages=list(self._package_buffer))
        self._package_buffer.clear()
        return box

    async def push_package(self, package: Package) -> None:
        """
            push package to queue
            :param package:
            :return:
        """
        self.logger.debug('push package: queue=%d', self._queue.qsize())
        if len(self._package_buffer) >= PickupBox.max_size():
            box = self._buffer_to_box()
            await self._queue.put(box)
        self._package_buffer.append(package)

    async def push_box(self, box: PickupBox) -> None:
        """
            push box to queue
        :param box:
        :return:
        """
        self.logger.debug('push box: queue=%d', self._queue.qsize())
        if box.size < box.max_size() and self._package_buffer:
            box.add_packages(
                [
                    self._package_buffer.popleft()
                    for _ in range(min(box.max_size() - box.size, len(self._package_buffer)))
                ]
            )
        await self._queue.put(box)

    async def pop(self) -> PickupBox:
        """
            remove and return next box from queue
            if queue is empty, waits for next package
            :return:
        """
        self.logger.debug('pop box: queue=%d', self._queue.qsize())
        if self._queue.qsize():
            return await self._queue.get()

        if self._package_buffer:
            return self._buffer_to_box()

        return await self._queue.get()
