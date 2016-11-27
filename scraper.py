# Handles the scraping tasks
#

# lxml parses xml and html docs very well
from lxml import html
# requests instead of urllib2 because of readability and speed
import requests
from pprint import pprint
import time

from utils.IOCSV import IOCSV

# get xid from an index (i.e INX:IOM, FTSE:FSI, etc)
def get_xid(index):
    payload = {'s': index}
    website = "https://markets.ft.com/data/indices/tearsheet/constituents"
    page = requests.get(website, params=payload)
    tree = html.fromstring(page.content)
    xid = tree.xpath('//div[@class=')


if __name__ == '__main__':
    file_path = './data'
    file_name = 'data01'
    # create an instance of IOJson
    saveData = IOCSV(file_path, file_name)

    # website to crawl
    # website = "https://markets.ft.com/data/indices/ajax/getindexconstituents?xid=575769&pagenum=26"
    # website = "https://markets.ft.com/data/indices/tearsheet/constituents?s=INX:IOM"
    website = "https://markets.ft.com/data/indices/ajax/getindexconstituents"
    payload = {'xid': '575769', 'pagenum': 1}

    while True:
        try:
            # retrieve the website with the data
            # parse it and save as a tree
            page = requests.get(website, params=payload)
            tree = html.fromstring(page.json()['html'])
            # tree = html.fromstring(page.content)

            # get the list of equities
            equities = tree.xpath('//td/a[@class="mod-ui-link"]/text()')

            if not equities:
                # list is empty, no more data
                break
            else:
                # store into a file
                saveData.save(equities)
                payload['pagenum'] += 1
                print 'Equities: '
                pprint(equities)
        except requests.exceptions.ConnectionError:
            print "Connection reset"
            print "Waiting"
            time.sleep(5)
            print "Trying again"

