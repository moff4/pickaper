
import asyncio
import logging
from collections import deque

from .pickup_box import PickupBox
from .types import Package


class PickupBoxQueue:
    logger = logging.getLogger(__name__)

    def __init__(self, max_size: int = 32) -> None:
        self._package_buffer = deque()  # type: deque[Package]
        self._queue = asyncio.Queue(maxsize=max_size)  # type: asyncio.Queue[PickupBox]
        self._closing = False

    def close(self) -> None:
        self._closing = True

    async def push_package(self, package: Package) -> None:
        self.logger.info('push package: queue=%d', self._queue.qsize())
        if len(self._package_buffer) >= PickupBox.max_size():
            box = PickupBox(packages=list(self._package_buffer))
            self._package_buffer.clear()
            await self._queue.put(box)
        self._package_buffer.append(package)

    async def push_box(self, box: PickupBox) -> None:
        self.logger.info('push box: queue=%d', self._queue.qsize())
        if box.size < box.max_size() and self._package_buffer:
            box.add_packages(
                [
                    self._package_buffer.popleft()
                    for _ in range(min(box.max_size() - box.size, len(self._package_buffer)))
                ]
            )
        await self._queue.put(box)

    async def pop(self) -> PickupBox:
        self.logger.info('pop box: queue=%d', self._queue.qsize())
        return await self._queue.get()
