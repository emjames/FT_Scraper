
## **Financial Times Scraper**
###### Author: Emanuel James

# Steps to run
* `pip install -r requirements.txt`
* `python scraper.py`


#### scraper.py
Contains the main method of the script. It will ask the user for input of the following:
    indices to be scraped
    name of the file to store the data
    path to store the data file

After it gets user input it will start pulling the equities from Financial Times
and it will store the data in csv format, it will print the obtained data to std out.

If there is a connection error ( connection refused by the server ) it will wait 5 seconds and try again, 
when an empty list is returned, it will exit

