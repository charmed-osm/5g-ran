# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.
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
        # pylint:disable=W0212
        pod_ports = pod_spec._make_pod_ports(dictport)
        self.assertListEqual(expected_result, pod_ports)

    def test_make_pod_privilege(self) -> NoReturn:
        """Teting make pod privilege"""
        expected_result = {
            "securityContext": {"capabilities": {"add": ["NET_ADMIN"]}},
        }
        # pylint:disable=W0212
        pod_privilege = pod_spec._make_pod_privilege()
        self.assertDictEqual(expected_result, pod_privilege)

    def test_make_pod_command(self) -> NoReturn:
        """Teting make pod command"""
        expected_result = [
            "/bin/bash",
            "-ec",
            "while :; do service ssh restart; sleep 5 ; done",
        ]
        # pylint:disable=W0212
        pod_command = pod_spec._make_pod_command()
        self.assertListEqual(expected_result, pod_command)

    def test_make_pod_podannotations(self) -> NoReturn:
        """Teting make pod privilege"""
        # pylint:disable=line-too-long
        networks = '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.114"]\n}\n]'  # noqa
        expected_result = {"annotations": {"k8s.v1.cni.cncf.io/networks": networks}}
        # pylint:disable=W0212
        pod_podannotations = pod_spec._make_pod_podannotations()
        self.assertDictEqual(expected_result, pod_podannotations)

    def test_make_pod_spec(self) -> NoReturn:
        """Testing make pod spec"""
        image_info = {"upstream-source": "localhost:32000/ue:1.0"}
        config = {
            "ssh_port": 9999,
        }
        app_name = "udpnew"
        with self.assertRaises(ValueError):
            pod_spec.make_pod_spec(image_info, config, app_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
