# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

import unittest

from typing import NoReturn
from ops.testing import Harness
from charm import UeCharm

from ops.model import BlockedStatus


class TestCharm(unittest.TestCase):
    def setUp(self) -> NoReturn:
        """Test setup"""
        self.harness = Harness(UeCharm)
        self.harness.set_leader(is_leader=True)
        self.harness.begin()

    def test_config_changed(self) -> NoReturn:
        """Test installation without any relation."""
        self.harness.charm.on.start.emit()
        expected_result = {
            "version": 3,
            "containers": [
                {
                    "name": "ue",
                    "imageDetails": self.harness.charm.image.fetch(),
                    "imagePullPolicy": "Always",
                    "ports": [
                        {
                            "name": "ueport",
                            "containerPort": 22,
                            "protocol": "TCP",
                        },
                    ],
                    "command": [
                        "/bin/bash",
                        "-ec",
                        "while :; do service ssh restart; sleep 5 ; done",
                    ],
                    "kubernetes": {
                        "securityContext": {"capabilities": {"add": ["NET_ADMIN"]}}
                    },
                }
            ],
            "kubernetesResources": {
                "pod": {
                    "annotations": {
                        "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.114"]\n}\n]'  # noqa
                    }
                },
            },
        }

        # Verifying status
        self.assertNotIsInstance(self.harness.charm.unit.status, BlockedStatus)

        pod_spec, kubernetesResources = self.harness.get_pod_spec()
        self.assertDictEqual(expected_result, pod_spec)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        self.assertFalse(self.harness.charm.unit.status.message.endswith(" relations"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
