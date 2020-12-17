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
"""ran operator pod_spec"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


GTP_PORT = 2152
REST_PORT = 8081


def _make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate pod ports details.
    Args:
        port (int): port to expose.
    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    if config["sctp_port"] > 0:
        return [
            {
                "name": "ranport",
                "containerPort": config["sctp_port"],
                "protocol": "TCP",
            },
            {"name": "ranport2", "containerPort": REST_PORT, "protocol": "TCP"},
        ]
    # else:
    raise ValueError("Invalid sctp port number")


def _make_pod_envconfig(model_name: str) -> Dict[str, Any]:
    """Generate pod environment configuration.
    Args:
        config (Dict[str, Any]): configuration information.
        relation_state (Dict[str, Any]): relation state information.
    Returns:
        Dict[str, Any]: pod environment configuration.
    """
    envconfig = {
        # General configuration
        "ALLOW_ANONYMOUS_LOGIN": "yes",
        "MODEL": model_name,
    }

    return envconfig


def _make_pod_privilege() -> Dict[str, Any]:
    """Generate pod privileges.
    Args:
        config (Dict[str, Any]): configuration information.
    Returns:
        Dict[str, Any]: pod privilege.
    """
    privil = {"securityContext": {"privileged": True}}
    return privil


def _make_pod_serviceaccount() -> Dict[str, Any]:
    serviceacc = {
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
    return serviceacc


def _make_pod_customresourcedefinition() -> List[Dict[str, Any]]:
    custom_def = [
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

    return custom_def


def _make_pod_resource() -> Dict[str, Any]:
    resource = {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {"name": "internet-network"},
                # pylint:disable=line-too-long
                "spec": {
                    "config": '{\n"cniVersion": "0.3.1",\n"name": "internet-network",\n"type": "macvlan",\n"master": "ens3",\n"mode": "bridge",\n"ipam": {\n"type": "host-local",\n"subnet": "60.60.0.0/16",\n"rangeStart": "60.60.0.50",\n"rangeEnd": "60.60.0.250",\n"gateway": "60.60.0.100"\n}\n}'  # noqa
                },
            }
        ]
    }

    return resource


def _make_pod_podannotations() -> Dict[str, Any]:
    # pylint:disable=line-too-long
    networks = '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.150"]\n}\n]'  # noqa
    annot = {"annotations": {"k8s.v1.cni.cncf.io/networks": networks}}

    return annot


def _make_pod_services(app_name: str):
    return [
        {
            "name": "udpnew-lb",
            "labels": {"juju-app": app_name},
            "spec": {
                "selector": {"juju-app": app_name},
                "ports": [
                    {
                        "protocol": "UDP",
                        "port": GTP_PORT,
                        "targetPort": GTP_PORT,
                    }
                ],
                "type": "LoadBalancer",
            },
        }
    ]


def make_pod_spec(
    image_info: Dict[str, str],
    config: Dict[str, Any],
    model_name: str,
    app_name: str,
) -> Dict[str, Any]:
    """Generate the pod spec information.
    Args:
        image_info (Dict[str, str]): Object provided by
                                     OCIImageResource("image").fetch().
        config (Dict[str, Any]): Configuration information.
        relation_state (Dict[str, Any]): Relation state information.
        app_name (str, optional): Application name. Defaults to "pol".
        port (int, optional): Port for the container. Defaults to 80.
    Returns:
        Dict[str, Any]: Pod spec dictionary for the charm.
    """
    if not image_info:
        return None

    ports = _make_pod_ports(config)
    env_config = _make_pod_envconfig(model_name)
    kubernetes = _make_pod_privilege()
    serviceaccount = _make_pod_serviceaccount()
    customdef = _make_pod_customresourcedefinition()
    customresource = _make_pod_resource()
    podannotations = _make_pod_podannotations()
    services = _make_pod_services(app_name)
    return {
        "version": 3,
        "containers": [
            {
                "name": app_name,
                "imageDetails": image_info,
                "imagePullPolicy": "Always",
                "ports": ports,
                "envConfig": env_config,
                "kubernetes": kubernetes,
            }
        ],
        "serviceaccount": serviceaccount,
        "kubernetesResources": {
            "customResourceDefinitions": customdef,
            "customResources": customresource,
            "pod": podannotations,
            "services": services,
        },
    }
