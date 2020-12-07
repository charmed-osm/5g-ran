# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

import unittest

from typing import NoReturn
from ops.testing import Harness
from charm import UeCharm

# from ops.model import BlockedStatus


class TestCharm(unittest.TestCase):
    def setUp(self) -> NoReturn:
        """Test setup"""
        self.harness = Harness(UeCharm)
        self.harness.set_leader(is_leader=True)
        self.harness.begin()

    def test_config_changed(self) -> NoReturn:
        harness = Harness(UeCharm)
        self.addCleanup(harness.cleanup)
        harness.begin()
        """Test installation without any relation."""
        self.harness.charm.on.start.emit()

        # Verifying status
        # self.assertIsInstance(self.harness.charm.unit.status, BlockedStatus)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        # self.assertTrue(self.harness.charm.unit.status.message.endswith(" relations"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
