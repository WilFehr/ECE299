# from smallLetters.py import singlePrint

from machine import Pin, SPI # SPI is a class associated with the machine library. 
from machine import Timer

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
from ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display.

# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows

# Initialize I/O pins associated with the oled display SPI interface

spi_sck = Pin(6) # sck stands for serial clock; always be connected to SPI SCK pin of the Pico
spi_sda = Pin(3) # sda stands for serial data;  always be connected to SPI TX pin of the Pico; this is the MOSI
spi_res = Pin(7) # res stands for reset; to be connected to a free GPIO pin
spi_dc  = Pin(4) # dc stands for data/command; to be connected to a free GPIO pin
spi_cs  = Pin(5) # chip select; to be connected to the SPI chip select of the Pico 

#
# SPI Device ID can be 0 or 1. It must match the wiring. 
#
SPI_DEVICE = 0 # Because the peripheral is connected to SPI 0 hardware lines of the Pico

#
# initialize the SPI interface for the OLED display
#
oled_spi = SPI( SPI_DEVICE, baudrate= 100000, sck= spi_sck, mosi= spi_sda )

#
# Initialize the display
#
oled = SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )

font = {
    '1':[0b00100,
         0b01100,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b01110],
    '2':[0b01110,
         0b10001,
         0b00001,
         0b00010,
         0b00100,
         0b01000,
         0b11111],
    '3':[0b01110,
         0b10001,
         0b00001,
         0b01110,
         0b00001,
         0b10001,
         0b01110],
    '4':[0b10001,
         0b10001,
         0b10001,
         0b11111,
         0b00001,
         0b00001,
         0b00001],
    '5':[0b11111,
         0b10000,
         0b10000,
         0b11110,
         0b00001,
         0b00001,
         0b11110],
    '6':[0b01110,
         0b10001,
         0b10000,
         0b11110,
         0b10001,
         0b10001,
         0b01110],
    '7':[0b11110,
         0b00001,
         0b00001,
         0b00010,
         0b00100,
         0b01000,
         0b10000],
    '8':[0b01110,
         0b10001,
         0b10001,
         0b01110,
         0b10001,
         0b10001,
         0b01110],
    '9':[0b01110,
         0b10001,
         0b10001,
         0b01111,
         0b00001,
         0b00001,
         0b01110],
    '0':[0b01110,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b01110],
    'A':[0b01110,
         0b10001,
         0b10001,
         0b11111,
         0b10001,
         0b10001,
         0b10001],
    'B':[0b11110,
         0b10001,
         0b10001,
         0b11110,
         0b10001,
         0b10001,
         0b11110],
    'C':[0b01110,
         0b10001,
         0b10000,
         0b10000,
         0b10000,
         0b10001,
         0b01110],
    'D':[0b11100,
         0b10010,
         0b10001,
         0b10001,
         0b10001,
         0b10010,
         0b11100],
    'E':[0b11111,
         0b10000,
         0b10000,
         0b11100,
         0b10000,
         0b10000,
         0b11111],
    'F':[0b11111,
         0b10000,
         0b10000,
         0b11100,
         0b10000,
         0b10000,
         0b10000],
    'G':[0b01110,
         0b10001,
         0b10000,
         0b10111,
         0b10001,
         0b10001,
         0b01110],
    'H':[0b10001,
         0b10001,
         0b10001,
         0b11111,
         0b10001,
         0b10001,
         0b10001],
    'I':[0b01110,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b01110],
    'J':[0b01111,
         0b00010,
         0b00010,
         0b00010,
         0b00010,
         0b10010,
         0b01100],
    'K':[0b10001,
         0b10010,
         0b10100,
         0b11000,
         0b10100,
         0b10010,
         0b10001],
    'L':[0b10000,
         0b10000,
         0b10000,
         0b10000,
         0b10000,
         0b10000,
         0b11111],
    'M':[0b10001,
         0b10001,
         0b11011,
         0b10101,
         0b10101,
         0b10001,
         0b10001],
    'N':[0b10001,
         0b11001,
         0b10101,
         0b10011,
         0b10001,
         0b10001,
         0b10001],
    'O':[0b01110,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b01110],
    'P':[0b01110,
         0b10001,
         0b10001,
         0b11110,
         0b10000,
         0b10000,
         0b10000],
    'Q':[0b01110,
         0b10001,
         0b10001,
         0b10001,
         0b10101,
         0b10010,
         0b01101],
    'R':[0b01110,
         0b10001,
         0b10001,
         0b11110,
         0b10100,
         0b10010,
         0b10001],
    'S':[0b01111,
         0b10000,
         0b10000,
         0b01110,
         0b00001,
         0b00001,
         0b11110],
    'T':[0b11111,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b00100],
    'U':[0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b01110],
    'V':[0b10001,
         0b10001,
         0b10001,
         0b11011,
         0b01010,
         0b01010,
         0b00100],
    'W':[0b10001,
         0b10001,
         0b10001,
         0b10001,
         0b10101,
         0b10101,
         0b01010],
    'X':[0b10001,
         0b10001,
         0b01010,
         0b00100,
         0b01010,
         0b10001,
         0b10001],
    'Y':[0b10001,
         0b10001,
         0b10001,
         0b01010,
         0b00100,
         0b00100,
         0b00100],
    'Z':[0b11111,
         0b00001,
         0b00010,
         0b00100,
         0b01000,
         0b10000,
         0b11111],
    '.':[0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00100],
    '^':[0b00100,
         0b01110,
         0b01110,
         0b01110,
         0b11111,
         0b00000,
         0b00100],
    '!':[0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b00100,
         0b00000,
         0b00100],
    '?':[0b01110,
         0b10001,
         0b00001,
         0b00010,
         0b00100,
         0b00000,
         0b00100],
    ' ':[0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00000,
         0b00000]
    }


def checkerboard(x_start, y_start, width, height):
    pixel = 0
    for y in range(height):
        for x in range(width):
            pixel = 1 * (pixel == 0)
            oled.pixel(x_start + x, y_start + y, pixel)
        if width % 2 == 0:
            pixel = 1 * (pixel == 0)
    return

def bell(x_start, y_start):
    bell = []
    bell.append([0,0,0,1,0,0,0])
    bell.append([0,0,1,1,1,0,0])
    bell.append([0,0,1,1,1,0,0])
    bell.append([0,0,1,1,1,0,0])
    bell.append([0,1,1,1,1,1,0])
    bell.append([1,1,1,1,1,1,1])
    bell.append([0,0,0,0,0,0,0])
    bell.append([0,0,0,1,0,0,0])
    
    y = 0
    for row in bell:
        x = 0
        for pixel in row:
            oled.pixel(x_start + x, y_start + y, pixel)
            x += 1
        y += 1
    return

def singlePrint(x_start, y_start, char):
    y = 0
    for row in font[char]:
        x = 0
        bits = f"{row:0{5}b}"
        for bit in bits:
            oled.pixel(x_start + x, y_start + y, int(bit))
            x += 1
        y += 1
    return

def smallText(x_start, y_start, string):
    x_start = int(x_start / 2)
    if (x_start > 128) or (y_start > 63):
        return
    # letters are 5x7
    # 6x8 bounding box
    # Bottom and right are whitespace
    curX = x_start
    for letter in string:
        if curX > 128:
            break
        singlePrint(x_start+curX, y_start, letter)
        curX += 6
    return

def showTime(state):
    if not state['24hr']:
        if state['hour'] < 12:
            smallText(60, 8, "AM")
        if state['hour'] >= 12:
            smallText(60, 8, "PM")
    if not state['24hr'] and state['hour'] == 0:
        string = "{}".format(12)
    elif not state['24hr'] and state['hour'] > 12:
        string = "{}".format(state['hour'] - 12)
    else:
        string = "{}".format(state['hour'])
    
    string += ":"
    string += "{0:0=2d}".format(state['min'])
    
    if(((state['hour'] > 9) and (state['hour'] < 13)) or (state['hour'] > 21)) or (state['hour'] == 0 and state['24hr'] is False):
        oled.text(string, 14, 16)
        if state['flash'] == 0 or state['flash'] == 3 or state['flash'] == 4:
            return
        elif state['flash'] == 1:
            oled.line(15, 24, 29, 24, state['flashVal'])
        elif state['flash'] == 2:
            oled.line(38, 24, 52, 24, state['flashVal'])
        else:
            oled.line(15, 24, 52, 24, state['flashVal'])
    else:
        oled.text(string, 19, 16)
        if state['flash'] == 0 or state['flash'] == 3 or state['flash'] == 4:
            return
        elif state['flash'] == 1:
            oled.line(20, 24, 26, 24, state['flashVal'])
        elif state['flash'] == 2:
            oled.line(35, 24, 49, 24, state['flashVal'])
        else:
            oled.line(20, 24, 49, 24, state['flashVal'])

def showAlarm(state):
    smallText(10, 30, "SET ALARM")
    
    if not state['24hr']:
        if state['alarmHour'] < 12:
            smallText(60, 8, "AM")
        if state['alarmHour'] >= 12:
            smallText(60, 8, "PM")
    
    if not state['24hr'] and state['alarmHour'] == 0:
        string = "{}".format(12)
    elif not state['24hr'] and state['alarmHour'] > 12:
        string = "{}".format(state['alarmHour'] - 12)
    else:
        string = "{}".format(state['alarmHour'])
    string += ":"
    string += "{0:0=2d}".format(state['alarmMin'])
    
    if(((state['alarmHour'] > 9) and (state['alarmHour'] < 13)) or (state['alarmHour'] > 21)) or (state['alarmHour'] == 0 and state['24hr'] is False):
        oled.text(string, 14, 16)
        if state['flash'] == 0 or state['flash'] == 1 or state['flash'] == 2 or state['flash'] == 5:
            return
        elif state['flash'] == 3:
            oled.line(15, 24, 29, 24, state['flashVal'])
        else:
            oled.line(38, 24, 52, 24, state['flashVal'])
    else:
        oled.text(string, 19, 16)
        if state['flash'] == 0 or state['flash'] == 1 or state['flash'] == 2 or state['flash'] == 5:
            return
        elif state['flash'] == 3:
            oled.line(20, 24, 26, 24, state['flashVal'])
        else:
            oled.line(35, 24, 49, 24, state['flashVal'])

def render(state):
    oled.fill(0)
    oled.line(79, 0, 79, 64, 1)
    oled.rect(0, 0, 128, 64, 1)
    
    # Tuning Box

    oled.rect(82, 10, 43, 10, 1)
            
    oled.line(83 + int(41 * (state['freq'] - 88) / 20), 10, 83 + int(41 * (state['freq'] - 88) / 20), 19, 1)
    
    smallText(92, 2, "TUNE")
    
    # Vol Box
    
    smallText(86, 31, "VOLUME")
    
    oled.rect(82, 39, 43, 10, 1)
    
    checkerboard(83, 40, int(41 * state['vol'] / 16), 8)
    
    oled.line(83 + int(41 * state['vol'] / 16), 39, 83 + int(41 * state['vol'] / 16), 48, 1)

    if state['alarm']:
        smallText(6, 8, "^")
    if state['flash'] < 3 or state['flash'] == 5:
        showTime(state)
    else:
        showAlarm(state)
    
    smallText(82, 22, str(state['freq'])+"FM")
    
    if state['vol'] == 0:
        smallText(89, 50, "MUTED")
    elif state['vol'] > 9:
        smallText(96, 50, str(state['vol']))
    else:
        smallText(100, 50, str(state['vol']))
    
#     bell(8, 8)
            
    oled.invert(state['invertScreen'])
    oled.show()

