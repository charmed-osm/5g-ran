#!/usr/bin/python3
# Copyright 2020 Tata Elxsi
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
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

"""
Ubuntu charm functional test using Zaza. Take note that the Ubuntu
charm does not have any relations or config options to exercise.
"""

import unittest
import socket
import logging
import requests
import zaza.model as model


class BasicDeployment(unittest.TestCase):
    """ class defines functional testing of ran charms """

    def test_upfgtp_connection(self):
        """ ***** checking gtp connection in ran ***** """
        ran_gtp_port = 2152
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for unit in model.get_units("ran"):
            ran_ip = model.get_status().applications["ran"]["units"][unit.entity_id][
                "address"
            ]
            result = sock.connect_ex((ran_ip, ran_gtp_port))
            if result == 0:
                logging.info("GTP Transport is Listening ...")
            else:
                logging.info("GTP Transport is not available")
            self.assertEqual(result, 0)

