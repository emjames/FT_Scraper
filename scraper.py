# Handles the scraping tasks
#

# lxml parses xml and html docs very well
from lxml import html
from lxml import etree
# requests instead of urllib2 because of readability and speed
import requests
from pprint import pprint
import time

from utils.IOCSV import IOCSV

# default global variables
_index = 'INX:IOM'
file_path = './data'
file_name = 'data01'


# get xid from an index (i.e INX:IOM, FTSE:FSI, etc)
def get_xid(index):
    payload = {'s': index}
    xidSite = "https://markets.ft.com/data/indices/tearsheet/constituents"
    page = requests.get(xidSite, params=payload)
    tree = html.fromstring(page.content)
    xid = tree.xpath('/html/body/div[3]/div[3]/section/div[1]/div/div/div')
    if xid:
        return xid[0].attrib['data-mod-xid']
    else:
        print 'Did not find the xid for', index


def get_user_input():
    print 'Leave blank for defaults'
    index = raw_input('Index to scrape (default: ' + _index + '> ')
    if index:
        xid = get_xid(index)
    else:
        xid = get_xid(_index)


def main():
    # create an instance of IOJson
    saveData = IOCSV(file_path, file_name)

    # website to crawl
    # the following is the AJAX URL used by Financial Times
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
            print "Connection reset, waiting"
            time.sleep(5)
            print "Trying again"


if __name__ == '__main__':
    # main()
    print get_xid(raw_input("Index to find> "))
