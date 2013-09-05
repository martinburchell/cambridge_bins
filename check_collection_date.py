#!/usr/bin/python

import logging
import os
import sys

from location_settings import *
from council_website import CouncilWebsite

script_dir = os.path.dirname(sys.argv[0])

log_dir = os.path.join(script_dir, 'log')
logger = logging.getLogger('check_collection_date')
handler = logging.FileHandler(os.path.join(log_dir,'check_collection_date.log'))
logger.addHandler(handler)
website = CouncilWebsite(logger)
website.check_collection_date(LOCATION_ADDRESS, LOCATION_POSTCODE)
