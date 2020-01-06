# -*- coding: utf-8 -*-
from luckydonaldUtils.logger import logging
import os

__author__ = 'luckydonald'
logger = logging.getLogger(__name__)


API_KEY = os.getenv('TG_API_KEY', None)
assert(API_KEY is not None)  # TG_API_KEY environment variable

HOSTNAME = os.getenv('URL_HOSTNAME', None)
# can be None

URL_PATH = os.getenv('URL_PATH', None)
assert(URL_PATH is not None)  # URL_PATH environment variable

EVENT_CHANNEL = os.getenv('TG_EVENT_CHANNEL', None)
assert(EVENT_CHANNEL is not None)  # TG_EVENT_CHANNEL environment variable

# This allows to use different server implementations like https://github.com/luckydonald/telegram_api_server
SERVER_BASE_URL = os.getenv('TG_SERVER_BASE_URL', None)  # can be None
if not SERVER_BASE_URL:  # empty "" -> None
    SERVER_BASE_URL = None
# end if

