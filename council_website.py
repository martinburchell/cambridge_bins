import urllib

from lxml.cssselect import CSSSelector

from web_automation.website import Website

class CouncilWebsite(Website):
    def __init__(self, logger=None):
        super(CouncilWebsite, self).__init__('cambridge.jdi-consult.net')

    def check_collection_date(self, address, postcode):
        bins_page = self.insecure_domain + '/bins/bins.php?address={}&postcode={}'.format(urllib.quote_plus(address),urllib.quote_plus(postcode))

        root = self.send_request_and_return_dom(bins_page)
        selector = CSSSelector('.inside div div')

        for div in selector(root):
            if div.text is not None:
                bin_type = div.text.strip()
                if bin_type == 'Blue and green bins':
                    date = div.find('b').text_content()
                    print date

