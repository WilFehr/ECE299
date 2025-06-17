from machine import Pin
from time import sleep

#some test code
#when button pressed toggle led


led = Pin(0, Pin.OUT)
button = Pin(2, Pin.IN, Pin.PULL_DOWN)

def button_handler(pin):
    if pin.value() == 1:
        led.toggle()
        sleep(0.15)
        

button.irq( trigger=Pin.IRQ_RISING, handler = button_handler)
    