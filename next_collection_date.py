#!/usr/bin/python

import logging
import os
import sys

from council_website import CouncilWebsite

if len(sys.argv) != 4:
    error = "Syntax {0} '<address>' '<postcode>' <black|blue|green>".format(
        sys.argv[0])

    print error
    exit(1)

script_dir = os.path.dirname(sys.argv[0])

log_dir = os.path.join(script_dir, 'log')
logger = logging.getLogger('check_collection_date')
handler = logging.FileHandler(os.path.join(log_dir,'next_collection_date.log'))
logger.addHandler(handler)
website = CouncilWebsite(logger)

address = sys.argv[1]
postcode = sys.argv[2]
colour = sys.argv[3]

date = website.get_next_collection_date(address, postcode, colour)
message = "The {0} bin will next be collected on {1}".format(
    colour,
    date.strftime('%A %-d %B %Y'))

print message
