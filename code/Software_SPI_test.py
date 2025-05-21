#experimentint with softwareSPI
from machine import Pin, SoftSPI

'''use pin0 to power digital potentiometer'''
pin0 = Pin(0, Pin.OUT)
pin0.on()


spi = SoftSPI(baudrate = 100_000, polarity = 1, phase = 0, sck = Pin(1)