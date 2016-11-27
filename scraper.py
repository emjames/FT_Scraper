# Handles the scraping tasks
# Author: Emanuel James ( emjames.com )

# lxml parses xml and html docs very well
from lxml import html
# requests instead of urllib2 because of readability and speed
import requests
from pprint import pprint
import time

# storage class
from utils.IOCSV import IOCSV

# default global variables
_index = 'INX:IOM'
user = {
    'index': _index,
    'file_path': './data',
    'file_name': 'data_' + _index.replace(':', '_'),
}


# get xid from an index (i.e INX:IOM, FTSE:FSI, etc)
def get_xid(index):
    payload = {'s': index}
    xid_site = "https://markets.ft.com/data/indices/tearsheet/constituents"

    while True:
        try:
            page = requests.get(xid_site, params=payload)
            tree = html.fromstring(page.content)
            xid = tree.xpath('/html/body/div[3]/div[3]/section/div[1]/div/div/div')
            if xid:
                return xid[0].attrib['data-mod-xid']
            else:
                print 'Did not find the xid for', index
                break
        except requests.exceptions.ConnectionError:
            print "Connection reset, waiting"
            time.sleep(5)
            print "Trying again"


# get user input for:
#                       index to search
#                       file name for data
#                       file location for data
def get_user_input():
    print '=== Leave blank for defaults ==='
    index = raw_input('Index to scrape (default: ' + _index + ' > ')
    if index:
        user['xid'] = get_xid(index)
        user['index'] = index
        user['file_name'] = 'data_' + index.replace(':', '_')
    else:
        user['xid'] = get_xid(_index)

    fname = raw_input('File name to store the data (default: ' + user['file_name'] + '.csv > ')
    if fname:
        user['file_name'] = fname

    fpath = raw_input('Data file path (default: ' + user['file_path'] + '> ')
    if fpath:
        user['file_path'] = fpath

    return user


# main method
#           get user input,
#           create the file to store the data,
#           get the data ( loop until an empty list is returned )
#           store the paginated data
def main():
    user_input = get_user_input()

    print 'Getting the indices for ', user_input['index']
    # create an instance of IOJson
    saveData = IOCSV(user_input['file_path'], user_input['file_name'])

    # website to crawl
    # the following is the AJAX URL used by Financial Times
    website = "https://markets.ft.com/data/indices/ajax/getindexconstituents"
    payload = {'xid': user_input['xid'], 'pagenum': 1}

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
    main()
