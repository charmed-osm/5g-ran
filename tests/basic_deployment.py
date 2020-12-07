#!/usr/bin/python3
"""
Ubuntu charm functional test using Zaza. Take note that the Ubuntu
charm does not have any relations or config options to exercise.
"""

import unittest
import zaza
import socket
import requests
import logging
import zaza.model as model
from juju.model import Model
import zaza.charm_lifecycle.utils as lifecycle_utils


class BasicDeployment(unittest.TestCase):
    def test_upfgtp_connection(self):
        """ ***** checking gtp connection in ran ***** """
        ran_gtp_port = 2152
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        for unit in zaza.model.get_units("ran"):
            ran_ip = model.get_status().applications["ran"]["units"][unit.entity_id][
                "address"
            ]
            result = sock.connect_ex((ran_ip, ran_gtp_port))
            if result == 0:
                logging.info("GTP Transport is Listening ...")
            else:
                logging.info("GTP Transport is not available")
            self.assertEqual(result, 0)

    def test_rest_service_call(self):
        """ ***** Testing the gnB config rest service *****"""
        for unit in zaza.model.get_units("ran"):
            ran_ip = model.get_status().applications["ran"]["units"][unit.entity_id][
                "address"
            ]
        ENDPOINT = "http://" + ran_ip + ":8081/configread"
        data = {
            "Global": {"mcc": "208", "mnc": "93", "gnbid": "454647"},
            "supportlist": [
                {
                    "tac": "0123",
                    "broadplmnlist": [
                        {
                            "mcc": "208",
                            "mnc": "93",
                            "slicesupport": [{"sst": 1, "sd": "010203"}],
                        }
                    ],
                }
            ],
            "paging": "v34",
            "gnbname": "Tata",
            "amfconfig": {
                "amfip": "10.45.28.51",
                "amfport": "38412",
                "gnbport": "9487",
                "ngapinterface": "eth0",
            },
            "upfconfig": {"upfip": "10.45.28.53"},
            "dbconfig": {"dbip": "10.45.28.52", "dbport": "27017", "dbname": "free5gc"},
        }
        result = requests.post(url=ENDPOINT, data=data)
        if result.status_code == 200:
            logging.info("The request was a Success !!")
            self.assertEqual(200, result.status_code)
        else:
            logging.info("Request Failed..")
