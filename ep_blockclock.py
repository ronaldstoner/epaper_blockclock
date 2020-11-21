import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys

import epd2in13_V2

from PIL import Image, ImageDraw, ImageFont

def startup():
    epd = epd2in13_V2.EPD()     # get the display
    epd.init(epd.FULL_UPDATE)   # initialize the display
    print("Clear...")           # prints to console, not the display, for debugging 
    epd.Clear(0xFF)             # clear the display and set to white

if __name__ == '__main__':
    startup()
