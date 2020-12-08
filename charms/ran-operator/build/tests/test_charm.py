# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

import unittest

from typing import NoReturn
from ops.testing import Harness
from charm import RanCharm

from ops.model import BlockedStatus


class TestCharm(unittest.TestCase):
    def setUp(self) -> NoReturn:
        """Test setup"""
        self.harness = Harness(RanCharm)
        self.harness.set_leader(is_leader=True)
        self.harness.begin()

    def test_config_changed(self) -> NoReturn:
        """Test installation without any relation."""
        self.harness.charm.on.start.emit()
        expected_result = {
            "version": 3,
            "containers": [
                {
                    "name": "ran",
                    "imageDetails": self.harness.charm.image.fetch(),
                    "imagePullPolicy": "Always",
                    "ports": [
                        {
                            "name": "ranport",
                            "containerPort": 9487,
                            "protocol": "TCP",
                        },
                        {
                            "name": "ranport2",
                            "containerPort": 8081,
                            "protocol": "TCP",
                        },
                    ],
                    "envConfig": {"ALLOW_ANONYMOUS_LOGIN": "yes", "MODEL": None},
                    "kubernetes": {"securityContext": {"privileged": True}},
                }
            ],
            "serviceaccount": {
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
            },
            "kubernetesResources": {
                "customResourceDefinitions": [
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
                            "versions": [
                                {"name": "v1", "served": True, "storage": True}
                            ],
                        },
                    }
                ],
                "customResources": {
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
                },
                "pod": {
                    "annotations": {
                        "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.150"]\n}\n]' # noqa
                    }
                },
                "services": [
                    {
                        "name": "udpnew-lb",
                        "labels": {"juju-app": "ran"},
                        "spec": {
                            "selector": {"juju-app": "ran"},
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
                ],
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
