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

    def check_collection_date(self, address, postcode, colour):
        dates = self.get_all_collection_dates(address, postcode)

        next_date = dates[colour][0]
        tomorrow = self.get_tomorrows_date()

        if next_date == tomorrow:
            print "The {} bin will be collected tomorrow so don't forget to put it out".format(colour)

    def get_tomorrows_date(self):
        return datetime.date.today() + datetime.timedelta(days=1)
            
    def get_all_collection_dates(self, address, postcode):
        bins_page = self.insecure_domain + '/bins/bins.php?address={}&postcode={}'.format(urllib.quote_plus(address),urllib.quote_plus(postcode))

        root = self.send_request_and_return_dom(bins_page)
        selector = CSSSelector('.inside div div')

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
        iso_date = None
        
        bold = div.find('b')
        if bold is not None:
            pattern = re.compile('[\W_]+')
            pattern.sub('', string.printable)
            date_text = re.sub(r'[^a-zA-Z0-9]', '', bold.text_content())

            full_date_text = "{}{}".format(date_text,
                                           str(datetime.date.today().year))

            iso_date = datetime.datetime(
                *(time.strptime(full_date_text, '%A%d%B%Y')[0:6])).date()

        return iso_date
