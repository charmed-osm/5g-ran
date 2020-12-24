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
"""ue operator tests pod_spec"""

from typing import NoReturn
import unittest
import pod_spec


class TestPodSpec(unittest.TestCase):
    """Pod spec unit tests."""

    def test_make_pod_ports(self) -> NoReturn:
        """Testing make pod ports."""
        port = 22
        expected_result = [
            {
                "name": "ueport",
                "containerPort": port,
                "protocol": "TCP",
            }
        ]
        dictport = {"ssh_port": 22}
        pod_ports = pod_spec._make_pod_ports(dictport)
        self.assertListEqual(expected_result, pod_ports)

    def test_make_pod_privilege(self) -> NoReturn:
        """Teting make pod privilege."""
        expected_result = {
            "securityContext": {"capabilities": {"add": ["NET_ADMIN"]}},
        }
        pod_privilege = pod_spec._make_pod_privilege()
        self.assertDictEqual(expected_result, pod_privilege)

    def test_make_pod_command(self) -> NoReturn:
        """Teting make pod command."""
        expected_result = [
            "/bin/bash",
            "-ec",
            "while :; do service ssh restart; sleep 5 ; done",
        ]
        pod_command = pod_spec._make_pod_command()
        self.assertListEqual(expected_result, pod_command)

    def test_make_pod_podannotations(self) -> NoReturn:
        """Teting make pod privilege."""
        expected_result = {
            "annotations": {
                "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",'
                '\n"interface": "eth1",\n"ips": []\n}\n]'
            }
        }
        pod_podannotations = pod_spec._make_pod_podannotations()
        self.assertDictEqual(expected_result, pod_podannotations)

    def test_validate_config(self) -> NoReturn:
        """Testing config data exception scenario."""
        config = {"ssh_port": 1234}
        with self.assertRaises(ValueError):
            pod_spec._validate_config(config)

    def test_make_pod_spec(self) -> NoReturn:
        """Testing make pod spec."""
        image_info = {"upstream-source": "localhost:32000/ue:1.0"}
        config = {
            "ssh_port": 9999,
        }
        app_name = "udpnew"
        with self.assertRaises(ValueError):
            pod_spec.make_pod_spec(image_info, config, app_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
