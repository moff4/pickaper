
import asyncio
from unittest import TestCase

from pickaper.pickup_box_queue import PickupBoxQueue
from pickaper.pickup_box import PickupBox
from pickaper.types import Package, PackingType


loop = asyncio.get_event_loop()


class PickupBoxQueueCase(TestCase):
    def test_ok_box(self):
        queue = PickupBoxQueue()
        package = Package(1, (1, 1, 1), 3, PackingType.BOX)
        box = PickupBox([package])

        loop.run_until_complete(queue.push_box(box))
        result = loop.run_until_complete(queue.pop())
        self.assertIs(box, result)

    def test_ok_package(self):
        queue = PickupBoxQueue()
        package = Package(1, (1, 1, 1), 3, PackingType.BOX)

        loop.run_until_complete(queue.push_package(package))
        box = loop.run_until_complete(queue.pop())  # type: PickupBox
        self.assertEqual(box.size, 1)
        self.assertEqual(box.next_package(), package)

    def test_ok_package_box(self):
        queue = PickupBoxQueue()
        package_1 = Package(1, (1, 1, 1), 3, PackingType.BOX)
        package_2 = Package(2, (1, 1, 1), 3, PackingType.BOX)
        box = PickupBox([package_1])

        loop.run_until_complete(queue.push_package(package_2))
        loop.run_until_complete(queue.push_box(box))
        box = loop.run_until_complete(queue.pop())  # type: PickupBox
        self.assertEqual(box.size, 2)
        self.assertTrue(any(p is package_1 for p in box.packages))
        self.assertTrue(any(p is package_2 for p in box.packages))
