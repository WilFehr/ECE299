#radio control for frequency and volume using encoders

from machine import Pin, SPI, I2C # SPI is a class associated with the machine library.
import time
from radio_class import Radio


# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
from ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display. 


# Define columns and rows of the oled display. These numbers are the standard values. 
SCREEN_WIDTH = 128 #number of columns
SCREEN_HEIGHT = 64 #number of rows

EncoderState = 0
UpdateDisplay = True

# DoEncoder1
# Encoder service routine for terminal A and B
def DoEncoder1( Encoder, State ):
    global EncoderState
    global Vol
    global UpdateDisplay

#
# Debug output
#
    print( EncoderState, Encoder, State, Vol)

    if ( EncoderState == 0 ):
#
# Check for input A going low ( encoder turning left )
#
        if (( Encoder == 'A' ) and ( State == 4 )):
            EncoderState = 1

#
# Check for input B going low ( encoder turning right )
#
        if (( Encoder == 'B' ) and ( State == 4 )):
            EncoderState = 4

#
# Encoding turing right squence ( A=0 then B=0 then A=1 and finally B=1 )
#

    elif( EncoderState == 1 ):
#        
# This should be input B going low
#
        if (( Encoder == 'B' ) and ( State == 4 )):
            EncoderState = 2
        else:
            EncoderState = 0
            
    elif ( EncoderState == 2 ):
#
# This should be input A going high
#        
        if (( Encoder == 'A' ) and ( State == 8 )):
            EncoderState = 3
        else:
            EncoderState = 0
            
    elif ( EncoderState == 3 ):
#
# Finally input B should go high
#
        if (( Encoder == 'B' ) and ( State == 8 )):

#
# The shaft is turing right so increment the count
#            
            if ( Vol < 16 ):
                Vol = Vol + 1
                UpdateDisplay = True

               
        EncoderState = 0


#
# Encoding turing left squence ( B=0 then A=0 then B=1 and finally A=1 )
#

    elif ( EncoderState == 4 ):
#        
# This should be input A going low
#        
        if (( Encoder == 'A' ) and ( State == 4 )):
            EncoderState = 5
        else:
            EncoderState = 0
            
    elif ( EncoderState == 5 ):
#        
# This should be input B going high
#        
        if (( Encoder == 'B' ) and ( State == 8 )):
            EncoderState = 6
        else:
            EncoderState = 0
                        
    elif ( EncoderState == 6 ):
#        
# This should be input A going high
#        
        if (( Encoder == 'A' ) and ( State == 8 )):
#
# The shaft is turing left so decrement the count
#
            if ( Vol != 0 ):
                Vol = Vol - 1
                UpdateDisplay = True

        EncoderState = 0

    else:
        EncoderState = 0
        
    return( True )
#end of DoEncoder1


#DoEncoder2
def DoEncoder2( Encoder, State ):
    global EncoderState
    global Freq
    global UpdateDisplay

#
# Debug output
#
    print( EncoderState, Encoder, State, Freq )

    if ( EncoderState == 0 ):
#
# Check for input A going low ( encoder turning left )
#
        if (( Encoder == 'A' ) and ( State == 4 )):
            EncoderState = 1

#
# Check for input B going low ( encoder turning right )
#
        if (( Encoder == 'B' ) and ( State == 4 )):
            EncoderState = 4

#
# Encoding turing right squence ( A=0 then B=0 then A=1 and finally B=1 )
#

    elif( EncoderState == 1 ):
#        
# This should be input B going low
#
        if (( Encoder == 'B' ) and ( State == 4 )):
            EncoderState = 2
        else:
            EncoderState = 0
            
    elif ( EncoderState == 2 ):
#
# This should be input A going high
#        
        if (( Encoder == 'A' ) and ( State == 8 )):
            EncoderState = 3
        else:
            EncoderState = 0
            
    elif ( EncoderState == 3 ):
#
# Finally input B should go high
#
        if (( Encoder == 'B' ) and ( State == 8 )):
            print("here a")
#
# The shaft is turing right so increment the count
#            
            if ( Freq < 107.8 ):
                print("here b")
                Freq = Freq + 0.2
                print("here c")
                UpdateDisplay = True
                print("here d")

               
        EncoderState = 0


#
# Encoding turing left squence ( B=0 then A=0 then B=1 and finally A=1 )
#

    elif ( EncoderState == 4 ):
#        
# This should be input A going low
#        
        if (( Encoder == 'A' ) and ( State == 4 )):
            EncoderState = 5
        else:
            EncoderState = 0
            
    elif ( EncoderState == 5 ):
#        
# This should be input B going high
#        
        if (( Encoder == 'B' ) and ( State == 8 )):
            EncoderState = 6
        else:
            EncoderState = 0
                        
    elif ( EncoderState == 6 ):
#        
# This should be input A going high
        print("here 0")
        print("freq: ", Freq)
        if (( Encoder == 'A' ) and ( State == 8 )):
#
# The shaft is turing left so decrement the count
#
            print("here 1")
            if ( Freq > 88.2 ):
                print("here 2")
                print("freq: ", Freq)
                Freq = Freq - 0.2
                print("here 3")
                print("freq: ", Freq)
                UpdateDisplay = True
                print("here 4")

        EncoderState = 0

    else:
        EncoderState = 0
            
    return( True )
#end of DoEncoder2


# Service terminal 1A interrupt
def Encoder1AInterrupt( Pin ):
    DoEncoder1( 'A', Pin.irq().flags())
    return( True )
# Service terminal 1B interrupt
def Encoder1BInterrupt( Pin ):
    DoEncoder1( 'B', Pin.irq().flags())
    return( True )
# Service terminal 2A interrupt
def Encoder2AInterrupt( Pin ):
    DoEncoder2( 'A', Pin.irq().flags())
    return( True )

# Service terminal 2B interrupt
def Encoder2BInterrupt( Pin ):
    DoEncoder2( 'B', Pin.irq().flags())
    return( True )



#
# initialize encoders
#
Encoder1A = Pin( 2, Pin.IN )
Encoder1B = Pin( 0, Pin.IN )
Encoder2A = Pin(10, Pin.IN )
Encoder2B = Pin(12, Pin.IN )

#
# Enable interrupt detection for both rising and falling edges of both signals
#

Encoder1A.irq( handler= Encoder1AInterrupt, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True )
Encoder1B.irq( handler= Encoder1BInterrupt, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True )
Encoder2A.irq( handler= Encoder2AInterrupt, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True )
Encoder2B.irq( handler= Encoder2BInterrupt, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, hard=True )


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
oled_spi = SPI( SPI_DEVICE, baudrate= 10000, sck= spi_sck, mosi= spi_sda )

#
# Initialize the display
#
oled = SSD1306_SPI( SCREEN_WIDTH, SCREEN_HEIGHT, oled_spi, spi_dc, spi_res, spi_cs, True )


# Assign a value to a variable
Vol = 3
Freq = 101.9


#create radio instance
fm_radio = Radio( Freq, Vol, False )








while ( True ):

        if ( UpdateDisplay == True ):
            if ( fm_radio.SetVolume( Vol ) == True ):
                fm_radio.ProgramRadio()
            print("here 5")
            if ( fm_radio.SetFrequency( Freq ) == True ):
                print("here 6")
                fm_radio.ProgramRadio()
                print("here 7")

            UpdateDisplay = False
#
# Clear the buffer
#
            oled.fill(0)
        
#
# Update the text on the screen
#
            oled.text("Vol: %d" %Vol, 0, 0) # Print the text starting from 0th column and 0th row
            oled.text("Freq: %.1f" %Freq, 0, 10 ) # Print the value stored in the variable Count. 
        
#
# Draw box below the text
#
            oled.rect( 0, 50, 128, 5, 1  )        

#
# Transfer the buffer to the screen
#
            oled.show()
    

