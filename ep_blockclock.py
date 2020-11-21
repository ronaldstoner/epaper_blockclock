import sys
sys.path.insert(1, "./lib") # Adds lib folder in this directory to sys
import epd2in13_V2
import subprocess
import json
import time

from PIL import Image, ImageDraw, ImageFont, ImageOps

def printToDisplay(string):
    HBlackImage = Image.new('1', (epd2in13_V2.EPD_HEIGHT, epd2in13_V2.EPD_WIDTH), 0)
    draw = ImageDraw.Draw(HBlackImage) # Create draw object and pass in the image layer we want to work with (HBlackImage)
    font = ImageFont.truetype('./fonts/steelfish_rounded_bd.ttf', 65) # Create our font, passing in the font file and font size
    
    # Caluculate screen center based off draw.textsize and screen width & height
    w,h = font.getsize(string)
    #print("Font Width: ", w)
    #print("Font Height:", h)

    #print("Max Width: ", epd2in13_V2.EPD_WIDTH)
    #print("Max Height: ", epd2in13_V2.EPD_HEIGHT)  

    W = (epd2in13_V2.EPD_WIDTH - h)  
    H = (86 - h)

    #print("Output Width: ", W)
    #print("Output Height: ", H)

    # Draw the text and display the buffer
    draw.text((W, H), string, font = font, align="center", fill=255)
    epd.display(epd.getbuffer(HBlackImage))

def getPrice(): 
    response = subprocess.check_output(['curl', '-s', "https://api.coinbase.com/v2/prices/spot?currency=USD"])

    #json response to string
    json_response = json.loads(response)

    # Print entire json response
    print(json_response)

    # Pull out balance field 
    balance=json_response['data']['amount']
    print(str(balance))
    return(str(balance))

if __name__ == '__main__':
    epd = epd2in13_V2.EPD()     # get the display
    epd.init(epd.FULL_UPDATE)   # initialize the display
    print("Clear...")           # prints to console, not the display, for debugging 
    epd.Clear(0xFF)             # clear the display and set to white
   
    while True:
        cur_btcPrice = getPrice()
        printToDisplay(cur_btcPrice)
        time.sleep(20)
