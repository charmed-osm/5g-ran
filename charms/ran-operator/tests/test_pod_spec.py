# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

from pydantic import ValidationError
from typing import NoReturn
import unittest
import pod_spec


class TestPodSpec(unittest.TestCase):
    """Pod spec unit tests."""

    def test_make_pod_ports(self) -> NoReturn:
        """Testing make pod ports."""
        sctp_port = 9999
        rest_port = 8888
        expected_result = [
            {
                "name": "ranport",
                "containerPort": sctp_port,
                "protocol": "TCP",
            },
            {
                "name": "ranport2",
                "containerPort": rest_port,
                "protocol": "TCP",
            },
        ]
        portdict = {
            "sctp_port": 9999,
            "rest_port": 8888,
        }
        pod_ports = pod_spec._make_pod_ports(portdict)
        self.assertListEqual(expected_result, pod_ports)

    def test_make_pod_envconfig(self) -> NoReturn:
        """Teting make pod envconfig configuration."""

        expected_result = {
            "ALLOW_ANONYMOUS_LOGIN": "yes",
            "MODEL": "rantest",
        }

        pod_envconfig = pod_spec._make_pod_envconfig("rantest")
        self.assertDictEqual(expected_result, pod_envconfig)

    def test_make_pod_privilege(self) -> NoReturn:
        """Teting make pod privilege"""
        expected_result = {
            "securityContext": {"privileged": True},
        }
        pod_privilege = pod_spec._make_pod_privilege()
        self.assertDictEqual(expected_result, pod_privilege)

    def test_make_pod_serviceaccount(self) -> NoReturn:
        """Teting make pod serviceaccount"""
        expected_result = {
            "automountServiceAccountToken": True,
            "roles": [
                {
                    "rules": [
                        {
                            "apiGroups": [""],
                            "resources": ["services"],
                            "verbs": ["get", "watch", "list"],
                        }
                    ]
                }
            ],
        }

        pod_serviceaccount = pod_spec._make_pod_serviceaccount()
        self.assertDictEqual(expected_result, pod_serviceaccount)

    def test_make_pod_customresourcedefinition(self) -> NoReturn:
        """Teting make pod customresourcedefinition"""
        expected_result = [
            {
                "name": "network-attachment-definitions.k8s.cni.cncf.io",
                "spec": {
                    "group": "k8s.cni.cncf.io",
                    "scope": "Namespaced",
                    "names": {
                        "kind": "NetworkAttachmentDefinition",
                        "singular": "network-attachment-definition",
                        "plural": "network-attachment-definitions",
                    },
                    "versions": [{"name": "v1", "served": True, "storage": True}],
                },
            }
        ]
        pod_customresourcedefinition = pod_spec._make_pod_customresourcedefinition()
        self.assertListEqual(expected_result, pod_customresourcedefinition)

    def test_make_pod_resource(self) -> NoReturn:
        """Teting make pod resource"""
        expected_result = {
            "network-attachment-definitions.k8s.cni.cncf.io": [
                {
                    "apiVersion": "k8s.cni.cncf.io/v1",
                    "kind": "NetworkAttachmentDefinition",
                    "metadata": {"name": "internet-network"},
                    "spec": {
                        "config": '{\n"cniVersion": "0.3.1",\n"name": "internet-network",\n"type": "macvlan",\n"master": "ens3",\n"mode": "bridge",\n"ipam": {\n"type": "host-local",\n"subnet": "60.60.0.0/16",\n"rangeStart": "60.60.0.50",\n"rangeEnd": "60.60.0.250",\n"gateway": "60.60.0.100"\n}\n}'  # noqa
                    },
                }
            ]
        }
        pod_resource = pod_spec._make_pod_resource()
        self.assertDictEqual(expected_result, pod_resource)

    def test_make_pod_podannotations(self) -> NoReturn:
        """Teting make pod privilege"""
        networks = '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.150"]\n}\n]' # noqa
        expected_result = {"annotations": {"k8s.v1.cni.cncf.io/networks": networks}}

        pod_podannotations = pod_spec._make_pod_podannotations()
        self.assertDictEqual(expected_result, pod_podannotations)

    def test_make_pod_services(self) -> NoReturn:
        """Teting make pod envconfig configuration."""
        appname = "udpnew"
        expected_result = [
            {
                "name": "udpnew-lb",
                "labels": {"juju-app": appname},
                "spec": {
                    "selector": {"juju-app": appname},
                    "ports": [
                        {
                            "protocol": "UDP",
                            "port": 8888,
                            "targetPort": 8888,
                        }
                    ],
                    "type": "LoadBalancer",
                },
            }
        ]
        portdict1 = {
            "gtp_port": 8888,
        }
        # test = "udpnew-lb"
        pod_services = pod_spec._make_pod_services(portdict1, appname)
        self.assertEqual(expected_result, pod_services)

    def test_make_pod_spec(self) -> NoReturn:
        """Testing make pod spec"""
        image_info = {"upstream-source": "10.45.5.100:4200/canonical/ran:v25.0"}
        config = {
            "sctp_port": 9999,
            "gtp_port": 8888,
            "rest_port": 7777,
        }
        model_name = "ran"
        app_name = "udpnew"

        with self.assertRaises(ValidationError):
            pod_spec.make_pod_spec(image_info, config, model_name, app_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
