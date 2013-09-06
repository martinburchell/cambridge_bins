import urllib

from lxml.cssselect import CSSSelector

from web_automation.website import Website

class CouncilWebsite(Website):
    colours = ('black', 'blue', 'green', 'all')

    def __init__(self, logger=None):
        super(CouncilWebsite, self).__init__('cambridge.jdi-consult.net')

    def check_collection_date(self, address, postcode, colour):
        dates = self.get_all_collection_dates(address, postcode)

        if colour not in self.colours:
            colour = 'all'

        print dates[colour]

    def get_all_collection_dates(self, address, postcode):
        bins_page = self.insecure_domain + '/bins/bins.php?address={}&postcode={}'.format(urllib.quote_plus(address),urllib.quote_plus(postcode))

        root = self.send_request_and_return_dom(bins_page)
        selector = CSSSelector('.inside div div')

        dates = {}

        for colour in self.colours:
            dates[colour] = []

        for div in selector(root):
            bold = div.find('b')
            if bold is not None:
                date = bold.text_content()

                bin_type = div.text.strip()
                if bin_type == 'Blue and green bins':
                    dates['blue'].append(date)
                    dates['green'].append(date)
                elif bin_type == 'Black bins':
                    dates['black'].append(date)

                if bin_type != '':
                    dates['all'].append(date)

        return dates
