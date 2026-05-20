"""
Tests for Device:
- Device is an abstract base class (subclass of abc.ABC)
"""

import unittest
from abc import ABC

from energy.models.device import Device


class TestDevice(unittest.TestCase):
    def test_is_abc(self):
        self.assertTrue(issubclass(Device, ABC))


if __name__ == "__main__":
    unittest.main()
