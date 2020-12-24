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
import json
from typing import Any, Dict, List
from IPy import IP

logger = logging.getLogger(__name__)


GTP_PORT = 2152
REST_PORT = 8081


def _make_pod_ports(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate pod ports details.

    Args:
        config(Dict[str, Any]): Configuration information.

    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    return [
        {
            "name": "ranport",
            "containerPort": config["sctp_port"],
            "protocol": "TCP",
        },
        {"name": "ranport2", "containerPort": REST_PORT, "protocol": "TCP"},
    ]


def _make_pod_envconfig(model_name: str) -> Dict[str, Any]:
    """Generate pod environment configuration.

    Args:
         model_name(str):pod environment congiguration.

    Returns:
        Dict[str, Any]: pod environment configuration.
    """
    return {
        # General configuration
        "ALLOW_ANONYMOUS_LOGIN": "yes",
        "MODEL": model_name,
    }


def _make_pod_privilege() -> Dict[str, Any]:
    """Generate pod privileges.

    Returns:
        Dict[str, Any]: pod privilege.
    """
    privil = {"securityContext": {"privileged": True}}
    return privil


def _make_pod_serviceaccount() -> Dict[str, Any]:
    """Generating pod service account.

    Returns:
        Dict[str, Any]: pod service account.
    """
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
    """Generate pod custom resource definition.

    Returns:
        List[Dict[str, Any]: pod custom resource definition.
    """
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


def _make_pod_resource(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate pod resource.

    Args:
        config(Dict[str, Any]):pod resource.

    Returns:
        Dict[str, Any]: pod resource.
    """
    ipam_body = {
        "type": "host-local",
        "subnet": config["pdn_subnet"],
        "rangeStart": config["pdn_ip_range_start"],
        "rangeEnd": config["pdn_ip_range_end"],
        "gateway": config["pdn_gateway_ip"],
    }
    config_body = {
        "cniVersion": "0.3.1",
        "name": "internet-network",
        "type": "macvlan",
        "master": "ens3",
        "mode": "bridge",
        "ipam": ipam_body,
    }
    resource = {
        "network-attachment-definitions.k8s.cni.cncf.io": [
            {
                "apiVersion": "k8s.cni.cncf.io/v1",
                "kind": "NetworkAttachmentDefinition",
                "metadata": {"name": "internet-network"},
                "spec": {"config": json.dumps(config_body)},
            }
        ]
    }

    return resource


def _make_pod_podannotations() -> Dict[str, Any]:
    """Generate pod annotation.

    Returns:
        Dict[str, Any]: pod annotations.
    """
    annot = {
        "annotations": {
            "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",'
            '\n"interface": "eth1",\n"ips": []\n}\n]'
        }
    }

    return annot


def _make_pod_services(app_name: str):
    """Generate pod services.

    Args:
        app_name(str): pod services.
    """
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


def _validate_config(config: Dict[str, Any]):
    """Validate config data.

    Args:
        config (Dict[str, Any]): configuration information.
    """
    if config.get("sctp_port") < 0:
        raise ValueError("Invalid sctp port")
    pdn_subnet = config.get("pdn_subnet")
    pdn_ip_range_start = config.get("pdn_ip_range_start")
    pdn_ip_range_end = config.get("pdn_ip_range_end")
    pdn_gateway_ip = config.get("pdn_gateway_ip")
    for pdn_conf in pdn_subnet, pdn_ip_range_start, pdn_ip_range_end, pdn_gateway_ip:
        if not IP(pdn_conf):
            raise ValueError("Value error in pdn ip configuration")


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

    _validate_config(config)
    ports = _make_pod_ports(config)
    env_config = _make_pod_envconfig(model_name)
    kubernetes = _make_pod_privilege()
    serviceaccount = _make_pod_serviceaccount()
    customdef = _make_pod_customresourcedefinition()
    customresource = _make_pod_resource(config)
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
