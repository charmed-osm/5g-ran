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


def _make_pod_ports(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate pod ports details.
    Args:
        port (int): port to expose.
    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    if config["ssh_port"] == 22:
        return [
            {"name": "ueport", "containerPort": config["ssh_port"], "protocol": "TCP"},
        ]


def _make_pod_privilege() -> Dict[str, Any]:
    """Generate pod privileges.
    Args:
        config (Dict[str, Any]): configuration information.
    Returns:
        Dict[str, Any]: pod privilege.
    """
    privil = {"securityContext": {"capabilities": {"add": ["NET_ADMIN"]}}}
    return privil


def _make_pod_command() -> List:
    """Generate pod privileges.
    Args:
        config (Dict[str, Any]): configuration information.
    Returns:
        Dict[str, Any]: pod privilege.
    """
    ssh_run = [
        "/bin/bash",
        "-ec",
        "while :; do service ssh restart; sleep 5 ; done",  # WHY RESTART THE SSH SERVICE ALL THE TIME?
    ]
    return ssh_run


def _make_pod_podannotations() -> Dict[str, Any]:
    annot = {
        "annotations": {
            # pylint:disable=line-too-long
            "k8s.v1.cni.cncf.io/networks": [
                {
                    "name": "internet-network",
                    "interface": "eth1",
                    "ips": ["60.60.0.114"],  # HARD-CODED IP? WHY? REMOVE IF POSSIBLE.
                }
            ]  # noqa
        }
    }

    return annot


def _validate_config(config: Dict[str, Any]):
    pass  # TODO

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

    _validate_config(config)  # Create this function, and check all parameters needed there. Raise ValueError inside that function if something is not correct.
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
