from machine import Pin
from time import sleep

pin0 = Pin(0, Pin.OUT)

while True:
    sleep(0.01)
    pin0.toggle()
    
