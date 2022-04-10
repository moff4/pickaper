
from unittest import TestCase

from pickaper.pickup_box import PickupBox
from pickaper.types import Package, PackingType


class PickupBoxCase(TestCase):
    def test_ok(self):
        package = Package(1, (1, 1, 1), 3, PackingType.BOX)

        box = PickupBox()
        self.assertEqual(box.size, 0)
        self.assertEqual(len(box.packages), 0)

        can_append_1 = box.can_append

        box.add_package(package)
        can_append_2 = box.can_append
        self.assertEqual(box.size, 1)
        self.assertEqual(len(box.packages), 1)
        self.assertEqual(can_append_1 - can_append_2, 1)

        box.add_packages([package] * 3)
        can_append_3 = box.can_append
        self.assertEqual(can_append_1 - can_append_3, 4)
        self.assertEqual(box.size, 4)
        self.assertEqual(len(box.packages), 4)
