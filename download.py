#!/usr/bin/python
# Download the links

import urllib.request

# file where it will be stored to
rawSrc='tmp.txt'
linkSrc='lnksSrc.txt'

# this function will download the source code and save it as a txt file.
def dlSrc():
    # Open first file where source code will be saved
    wRawSrc=open(rawSrc,'w')
    # connect and donwnload
    locPage='http://www.basketball-reference.com/friv/trades.fcgi?f1=ATL&f2=BOS'
    webPage=urllib.request.urlopen(locPage)
    wPageSrc=webPage.read()
    webPage.close()
    # write to text file
    wRawSrc.write(str(wPageSrc))

# this function will extract all the links and save them on another txt file
def cleanFile():
    # open raw HTML source for reading
    rRawSrc=open(rawSrc,'r')
    # open the stripped one for writing
    wlinkSrc=open(linkSrc,'w')
    # export only the lines that contain 'a href'
    for line in rRawSrc:
        if 'a href' in line:
            wlinkSrc.write(line)

# Run the functions
dlSrc()
#cleanFile()
