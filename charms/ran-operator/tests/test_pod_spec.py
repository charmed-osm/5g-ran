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
"""ran operator tests pod_spec"""

from typing import NoReturn
import json
import unittest
import pod_spec


class TestPodSpec(unittest.TestCase):
    """Pod spec unit tests."""

    def test_make_pod_ports(self) -> NoReturn:
        """Testing make pod ports."""
        sctp_port = 9999
        rest_port = 8081
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
        """Teting make pod privilege."""
        expected_result = {
            "securityContext": {"privileged": True},
        }
        pod_privilege = pod_spec._make_pod_privilege()
        self.assertDictEqual(expected_result, pod_privilege)

    def test_make_pod_serviceaccount(self) -> NoReturn:
        """Teting make pod serviceaccount."""
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
        """Teting make pod customresourcedefinition."""
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
        """Teting make pod resource."""
        config = {
            "sctp_port": 1234,
            "pdn_subnet": "60.60.0.0/16",
            "pdn_ip_range_start": "60.60.0.50",
            "pdn_ip_range_end": "60.60.0.250",
            "pdn_gateway_ip": "60.60.0.100",
        }
        pdn_subnet = "60.60.0.0/16"
        pdn_ip_range_start = "60.60.0.50"
        pdn_ip_range_end = "60.60.0.250"
        pdn_gateway_ip = "60.60.0.100"
        pod_resource = pod_spec._make_pod_resource(config)
        ipam_body = {
            "type": "host-local",
            "subnet": pdn_subnet,
            "rangeStart": pdn_ip_range_start,
            "rangeEnd": pdn_ip_range_end,
            "gateway": pdn_gateway_ip,
        }
        config_body = {
            "cniVersion": "0.3.1",
            "name": "internet-network",
            "type": "macvlan",
            "master": "ens3",
            "mode": "bridge",
            "ipam": ipam_body,
        }
        expected_result = {
            "network-attachment-definitions.k8s.cni.cncf.io": [
                {
                    "apiVersion": "k8s.cni.cncf.io/v1",
                    "kind": "NetworkAttachmentDefinition",
                    "metadata": {"name": "internet-network"},
                    "spec": {"config": json.dumps(config_body)},
                }
            ]
        }
        self.assertDictEqual(expected_result, pod_resource)

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
                            "port": 2152,
                            "targetPort": 2152,
                        }
                    ],
                    "type": "LoadBalancer",
                },
            }
        ]
        pod_services = pod_spec._make_pod_services(appname)
        self.assertEqual(expected_result, pod_services)

    def test_validate_config(self) -> NoReturn:
        """Testing config data exception scenario."""
        config = {
            "sctp_port": 1234,
            "pdn_subnet": "-60.60.0.0/16",
            "pdn_ip_range_start": "-60.60.0.50",
            "pdn_ip_range_end": "-60.60.0.250",
            "pdn_gateway_ip": "-60.60.0.100",
        }
        with self.assertRaises(ValueError):
            pod_spec._validate_config(config)

    def test_make_pod_spec(self) -> NoReturn:
        """Testing make pod spec."""
        image_info = {"upstream-source": "localhost:32000/ran:1.0"}
        config = {
            "sctp_port": -9999,
            "pdn_subnet": "-60.60.0.0/16",
            "pdn_ip_range_start": "-60.60.0.50",
            "pdn_ip_range_end": "-60.60.0.250",
            "pdn_gateway_ip": "-60.60.0.100",
        }
        model_name = "ran"
        app_name = "udpnew"

        with self.assertRaises(ValueError):
            pod_spec.make_pod_spec(image_info, config, model_name, app_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
