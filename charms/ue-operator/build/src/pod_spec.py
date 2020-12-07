#!/usr/bin/env python3model = model_name()
# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

import logging
from pydantic import BaseModel, PositiveInt
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class ConfigData(BaseModel):
    """Configuration data model."""

    port: PositiveInt


def _make_pod_ports(config: ConfigData) -> Dict[str, Any]:
    """Generate pod ports details.
    Args:
        port (int): port to expose.
    Returns:
        List[Dict[str, Any]]: pod port details.
    """
    return [
        {"name": "ueport", "containerPort": config["port"], "protocol": "TCP"},
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
        "while :; do service ssh restart; sleep 5 ; done",
    ]
    return ssh_run


def _make_pod_podannotations() -> Dict[str, Any]:
    annot = {
        "annotations": {
            "k8s.v1.cni.cncf.io/networks": '[\n{\n"name" : "internet-network",\n"interface": "eth1",\n"ips": ["60.60.0.114"]\n}\n]' # noqa
        }
    }

    return annot


def make_pod_spec(
    image_info: Dict[str, str],
    config: Dict[str, Any],
    # relation_state: Dict[str, Any],
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

    ConfigData(**(config))

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
