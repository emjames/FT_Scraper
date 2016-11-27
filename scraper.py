# Handles the scraping tasks
#

# lxml parses xml and html docs very well
from lxml import html
# requests instead of urllib2 because of readability and speed
import requests
from pprint import pprint


website = "https://markets.ft.com/data/indices/tearsheet/constituents?s=INX:IOM"

# retrieve the website with the data
# parse it and save as a tree
page = requests.get(website)
tree = html.fromstring(page.content)

# get the list of equities
equities = tree.xpath('//td/a[@class="mod-ui-link"]/text()')

print 'Equities: '
pprint(equities)

