#!/usr/bin/env python3
# Copyright 2020 Tata Elxsi canonical@tataelxsi.onmicrosoft.com
# See LICENSE file for licensing details.

"""Operator Charm main library."""
# Load modules from lib directory
import logging
from typing import NoReturn
from oci_image import OCIImageResource, OCIImageResourceError

# from typing import Any, Dict, NoReturn

# import setuppath  # noqa:F401
from ops.charm import CharmBase
from ops.framework import StoredState, EventBase
from ops.main import main
from ops.model import BlockedStatus, ActiveStatus, MaintenanceStatus
from pod_spec import make_pod_spec


logger = logging.getLogger(__name__)


class ConfigurePodEvent(EventBase):
    """Configure Pod event"""


class RanCharm(CharmBase):
    """Ran Charm"""
    state = StoredState()

    def __init__(self, *args) -> NoReturn:
        """RAN Charm constructor"""
        super().__init__(*args)

        # Internal state initialization
        self.state.set_default(pod_spec=None)

        self.image = OCIImageResource(self, "image")

        # Registering regular events
        self.framework.observe(self.on.start, self.configure_pod)
        self.framework.observe(self.on.config_changed, self.configure_pod)
        self.framework.observe(self.on.upgrade_charm, self.configure_pod)

        # Registering custom internal events
        # self.framework.observe(self.on.configure_pod, self.configure_pod)

        # self.framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_config_changed(self, _):
        current = self.config["thing"]
        if current not in self.state.things:
            logger.debug("found a new thing: %r", current)
            self.state.things.append(current)

    def configure_pod(self, event: EventBase) -> NoReturn:
        """Assemble the pod spec and apply it, if possible.
        Args:
            event (EventBase): Hook or Relation event that started the
                               function.
        """
        logging.info(event)
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus("ready")
            return

        self.unit.status = MaintenanceStatus("Assembling pod spec")

        # Fetch image information
        try:
            self.unit.status = MaintenanceStatus("Fetching image information")
            image_info = self.image.fetch()
        except OCIImageResourceError:
            self.unit.status = BlockedStatus("Error fetching image information")
            return

        try:
            pod_spec = make_pod_spec(
                image_info,
                self.config,
                self.model.name,
                self.model.app.name,
            )
        except ValueError as exc:
            logger.exception("Config data validation error")
            self.unit.status = BlockedStatus(str(exc))
            return

        if self.state.pod_spec != pod_spec:
            self.model.pod.set_spec(pod_spec)
            self.state.pod_spec = pod_spec

        self.unit.status = ActiveStatus("ready")


if __name__ == "__main__":
    main(RanCharm)
