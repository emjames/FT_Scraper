# Handles the scraping tasks
#

# lxml parses xml and html docs very well
from lxml import html
# requests instead of urllib2 because of readability and speed
import requests
from pprint import pprint


# get xid from an index (i.e INX:IOM, FTSE:FSI, etc)
def get_xid(index):
    payload = {'s': index}
    website = "https://markets.ft.com/data/indices/tearsheet/constituents"
    page = requests.get(website, params=payload)
    tree = html.fromstring(page.content)
    xid = tree.xpath('//div[@class=')


if __name__ == '__main__':
    # website = "https://markets.ft.com/data/indices/tearsheet/constituents?s=INX:IOM"
    payload = {'xid': '575769', 'pagenum': 26}
    # website = "https://markets.ft.com/data/indices/ajax/getindexconstituents?xid=575769&pagenum=26"
    website = "https://markets.ft.com/data/indices/ajax/getindexconstituents"

    # retrieve the website with the data
    # parse it and save as a tree
    page = requests.get(website, params=payload)
    tree = html.fromstring(page.json()['html'])
    # tree = html.fromstring(page.content)

    # get the list of equities
    equities = tree.xpath('//td/a[@class="mod-ui-link"]/text()')

    print 'Equities: '
    pprint(equities)
