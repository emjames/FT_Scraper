# handles json storage
#
import csv
import os
import io


class IOCSV(object):
    # get the file path and file name
    # append .csv as file extension
    def __init__(self, path, name):
        self.pathName = path + '/' + name + '.csv'

    # checks if the file exists and decides to append or create a new file
    def save(self, data):
        if os.path.isfile(self.pathName):
            # append existing file
            mode = 'a'
        else:
            # create a new file
            mode = 'w'

        with open(self.pathName, mode) as outFile:
            writer = csv.writer(outFile)
            writer.writerow(data)
