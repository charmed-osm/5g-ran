#!/usr/bin/env python3
# Copyright 2020 Tata Elxsi
#
# Licensed under the Apache License, Version 2.0 (the License); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# For those usages not covered by the Apache License, Version 2.0 please
# contact: canonical@tataelxsi.onmicrosoft.com
#
# To get in touch with the maintainers, please contact:
# canonical@tataelxsi.onmicrosoft.com
##
""" ue operator tests charm"""

import unittest

from typing import NoReturn
from ops.testing import Harness
from ops.model import BlockedStatus
from charm import UeCharm


class TestCharm(unittest.TestCase):
    """Test Charm"""

    def setUp(self) -> NoReturn:
        """Test setup"""
        self.harness = Harness(UeCharm)
        self.harness.set_leader(is_leader=True)
        self.harness.begin()

    def test_on_start_without_relations(self) -> NoReturn:
        """Test installation without any relation."""
        self.harness.charm.on.config_changed.emit()

        # Verifying status
        self.assertIsInstance(self.harness.charm.unit.status, BlockedStatus)

        # Verifying status message
        self.assertGreater(len(self.harness.charm.unit.status.message), 0)
        self.assertTrue(
            self.harness.charm.unit.status.message.startswith("Waiting for")
        )

    def test_on_start_with_relations(self) -> NoReturn:
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
                    "envConfig": {
                        "ALLOW_ANONYMOUS_LOGIN": "yes",
                        "RELATION": "ran",
                    },
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
                        "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",'
                        '\n"interface": "eth1",\n"ips": []\n}\n]'
                    }
                },
            },
        }

        self.assertIsNone(self.harness.charm.state.ran_host)
        ran_relation_id = self.harness.add_relation("ran", "ran")
        self.harness.add_relation_unit(ran_relation_id, "ran/0")
        self.harness.update_relation_data(ran_relation_id, "ran", {"hostname": "ran"})

        # Checking if nrf data is stored
        self.assertEqual(self.harness.charm.state.ran_host, "ran")

        # Verifying status
        self.assertNotIsInstance(self.harness.charm.unit.status, BlockedStatus)

        pod_spec, _ = self.harness.get_pod_spec()
        self.assertDictEqual(expected_result, pod_spec)


if __name__ == "__main__":
    unittest.main(verbosity=2)
