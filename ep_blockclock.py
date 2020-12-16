import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys
import epd2in13_V2
import subprocess
import json
import time
import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps

# TODO:
# Add in try conditions for api call failure
# More graceful failure on failed hardware init
# More screens / animations / sats-per-dollar
# Screen update time to variable
# Functionize timestamps for console/log output

api = 'https://api.coinbase.com/v2/prices/spot?currency=USD'

def printToDisplay(string, init_display):
    # Create draw object and pass in the image layer (HBlackImage)
    HBlackImage = Image.new('1', (epd2in13_V2.EPD_HEIGHT, epd2in13_V2.EPD_WIDTH), 0)
    draw = ImageDraw.Draw(HBlackImage)
    font = ImageFont.truetype('./fonts/steelfish_rounded_bd.ttf', 65)
    
    # Caluculate screen center based off draw.textsize and screen width & height
    w,h = font.getsize(string)
    #print("Font Width: ", w)
    #print("Font Height:", h)
    #print("Max Width: ", epd2in13_V2.EPD_WIDTH)
    #print("Max Height: ", epd2in13_V2.EPD_HEIGHT)  

    # TODO: Make H value dynamic instead of static - hacky
    W = (epd2in13_V2.EPD_WIDTH - h)  
    H = (86 - h)
    #print("Output Width: ", W)
    #print("Output Height: ", H)

    # Draw the text (white) and display the buffer (black)
    draw.text((W, H), string, font = font, align='center', fill=255)
    
    # Rotate image so device can sit like a clock
    HBlackImage = HBlackImage.rotate(angle=180)

    # Determine if we are doing a full or partial refresh
    global initial_display
    if init_display == True:
        #print(init_display, " - Full Display")
        epd.displayPartBaseImage(epd.getbuffer(HBlackImage))
        epd.init(epd.PART_UPDATE)
        initial_display=False
    else:
        #print(init_display, " - Partial Update")
        epd.displayPartial(epd.getbuffer(HBlackImage))
    
    initial_display=False
    return initial_display

def getPrice(): 
    response = subprocess.check_output(['curl', '-s', api])

    #json response to string
    json_response = json.loads(response)

    # Parse json response and get timestamps
    #print(json_response)
    ts = time.time()
    base = json_response['data']['base']
    currency = json_response['data']['currency']
    amount = json_response['data']['amount']
    print('[%s] [GET_PRICE] %s/%s %s' % (datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'), base, currency, amount))
    return(str(amount))

if __name__ == '__main__':
    # Get and init display
    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    print('[STARTUP]   Clearing the display') 
    # Cleat the display and set it to white 
    epd.Clear(0xFF)
    initial_display = True

    while True:
        cur_btcPrice = getPrice()
        printToDisplay(cur_btcPrice, initial_display)
        time.sleep(600)
