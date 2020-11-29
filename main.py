#!/usr/bin/env python3
"""Ucopia connect helper"""
from typing import Any
import os
import sys
import time
import logging

import requests


class AuthError(RuntimeError):
    """Authentication error"""

    def __str__(self):
        return 'Wrong credentials'


# pylint: disable=too-few-public-methods
class ApiResponse:
    """API Response"""

    def __init__(self, j: dict[str, Any]):
        self.j = j

    @property
    def step(self) -> str:
        """Current authentication step returned by the API"""
        return self.j.get('step')


class PortalAuth:
    """Portal authentication"""
    STEP_FEEDBACK = 'FEEDBACK'
    STEP_LOGON = 'LOGON'
    ACTION_INIT = 'init'
    ACTION_AUTHENTICATE = 'authenticate'

    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Linux) ' \
                                             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                             'Chrome/86.0.4240.198 Safari/537.36'

    @property
    def _api_url(self) -> str:
        """API URL"""
        return f'{self.base_url}/portal_api.php'

    def get_status(self) -> ApiResponse:
        """Get the current status"""
        resp = self.session.post(self._api_url, data={'action': PortalAuth.ACTION_INIT})
        return ApiResponse(resp.json())

    def perform_logon(self) -> ApiResponse:
        """Perform the logon"""
        resp = self.session.post(self._api_url, data={
            'action': PortalAuth.ACTION_AUTHENTICATE,
            'login': self.login,
            'password': self.password,
            'policy_accept': False,
            'from_ajax': True,
            'wispr_mode': False,
        })
        return ApiResponse(resp.json())

    def auto(self):
        """Automatic handling"""
        logging.info("Checking current step")
        status = self.get_status()
        logging.info("Current step: %s", status.step)
        if status.step == PortalAuth.STEP_FEEDBACK:
            logging.info("All good")
            return
        if status.step == PortalAuth.STEP_LOGON:
            logging.info("Attempting login !")
            status = self.perform_logon()
            if status.step == PortalAuth.STEP_FEEDBACK:
                logging.info("We're connected !")


def main():
    """Main method"""
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
    )
    conf_portal_address = os.environ.get('PORTAL_ADDRESS', 'https://controller.access.network')
    conf_portal_login = os.environ['PORTAL_LOGIN']
    conf_portal_password = os.environ['PORTAL_PASSWORD']
    conf_sleep_time = int(os.environ.get('CHECK_PERIOD', '20'))
    portal = PortalAuth(conf_portal_address, conf_portal_login, conf_portal_password)

    while True:
        try:
            portal.auto()
        except requests.exceptions.ConnectionError:
            logging.warning("Connection issue")
        time.sleep(conf_sleep_time)


if __name__ == '__main__':
    main()
