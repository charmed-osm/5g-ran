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
"""ue operator pod_spec"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)
SSH_PORT = 22


def _make_pod_ports(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate pod ports details.

    Args:
        config(Dict[str, Any]): pod ports.

    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    return [
        {"name": "ueport", "containerPort": config["ssh_port"], "protocol": "TCP"},
    ]


def _make_pod_privilege() -> Dict[str, Any]:
    """Generate pod privileges.

    Returns:
        Dict[str, Any]: pod privilege.
    """
    privil = {"securityContext": {"capabilities": {"add": ["NET_ADMIN"]}}}
    return privil


def _make_pod_command() -> List:
    """Generate pod command.

    Returns:
        List: pod command.
    """
    ssh_run = [
        "/bin/bash",
        "-ec",
        "while :; do service ssh restart; sleep 5 ; done",  # Why restarting the service every 5 seconds? I would replace it by reload, to avoid restarting all the service.
    ]
    return ssh_run


def _make_pod_podannotations() -> Dict[str, Any]:
    """Generate pod annotation.

    Returns:
        Dict[str, Any]: pod annotation.
    """
    annot = {
        "annotations": {
            "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",'
            '\n"interface": "eth1",\n"ips": []\n}\n]'
        }
    }

    return annot


def _validate_config(config: Dict[str, Any]) -> None:
    """Validate config data.

    Args:
        config (Dict[str, Any]): configuration information.
    """
    if config.get("ssh_port") != SSH_PORT:
        raise ValueError("Invalid ssh port")


def make_pod_spec(
    image_info: Dict[str, str],
    config: Dict[str, str],
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
    cmd = _make_pod_command()
    kubernetes = _make_pod_privilege()
    podannotations = _make_pod_podannotations()
    return {
        "version": 3,
        "containers": [
            {
                "name": app_name,
                "imageDetails": image_info,
                "imagePullPolicy": "Always",
                "ports": ports,
                "command": cmd,
                "kubernetes": kubernetes,
            }
        ],
        "kubernetesResources": {
            "pod": podannotations,
        },
    }
