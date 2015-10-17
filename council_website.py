import datetime
import re
import time
import string
import urllib

from lxml.cssselect import CSSSelector

from web_automation.website import Website


class CouncilWebsite(Website):
    colours = ('black', 'blue', 'green')

    def __init__(self, logger=None):
        super(CouncilWebsite, self).__init__('cambridge.jdi-consult.net')

    def bin_collected_tomorrow(self, address, postcode, colour):
        dates = self.get_all_collection_dates(address, postcode)

        next_date = dates[colour][0]
        tomorrow = self.get_tomorrows_date()

        return next_date == tomorrow

    def get_tomorrows_date(self):
        return datetime.date.today() + datetime.timedelta(days=1)

    def get_next_collection_date(self, address, postcode, colour):
        dates = self.get_all_collection_dates(address, postcode)

        return dates[colour][0]

    def get_all_collection_dates(self, address, postcode):
        bins_page = self.insecure_domain + '/bins/bins.php?address={0}&postcode={1}'.format(urllib.quote_plus(address),urllib.quote_plus(postcode))

        root = self.send_request_and_return_dom(bins_page)
        selector = CSSSelector('.page div div')

        dates = {}

        for colour in self.colours:
            dates[colour] = []

        for div in selector(root):
            iso_date = self.find_date_in_div(div)

            if iso_date is not None:
                bin_type = div.text.strip()

                if bin_type.lower() == 'blue and green bins':
                    dates['blue'].append(iso_date)
                    dates['green'].append(iso_date)
                elif bin_type.lower() == 'black bins':
                    dates['black'].append(iso_date)

        return dates

    def find_date_in_div(self, div):
        date = None

        bold = div.find('b')
        if bold is not None:
            date_text = re.sub(r'[^a-zA-Z0-9]', '', bold.text_content())

            matches = re.search('([0-9]+)([a-zA-Z]+)', date_text)

            day = int(matches.group(1))
            month = time.strptime(matches.group(2), '%B').tm_mon
            year = datetime.date.today().year

            date = datetime.date(year, month, day)
            if date < datetime.date.today():
                date = datetime.date(year+1, month, day)

        return date
