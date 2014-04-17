#!/usr/bin/python

import logging
import os
import smtplib
import sys

from email.mime.text import MIMEText

from council_website import CouncilWebsite

if len(sys.argv) not in (4,7):
    error = "Syntax {0} '<address>' '<postcode>' <black|blue|green> [<email_subject> <email_to> <email_from>]".format(
        sys.argv[0])

    print error
    exit(1)

script_dir = os.path.dirname(sys.argv[0])

log_dir = os.path.join(script_dir, 'log')
logger = logging.getLogger('check_collection_date')
handler = logging.FileHandler(os.path.join(log_dir,'check_collection_date.log'))
logger.addHandler(handler)
website = CouncilWebsite(logger)

address = sys.argv[1]
postcode = sys.argv[2]
colour = sys.argv[3]

try:
    email_subject = sys.argv[4] 
    email_to = sys.argv[5]
    email_from = sys.argv[6]

    send_email = True

except IndexError:
    send_email = False

if website.bin_collected_tomorrow(address, postcode, colour):
    message = "The {0} bin will be collected tomorrow so don't forget to put it out".format(colour)

    if send_email:
        email = MIMEText(message)

        email['Subject'] = email_subject
        email['From'] = email_to
        email['To'] = email_from

        s = smtplib.SMTP('localhost')
        s.sendmail(email_from, [email_to], email.as_string())
        s.quit()
    else:
        print message
