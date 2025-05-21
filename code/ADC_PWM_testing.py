'''
this is a test for the ADC and the PWM
I will be reading an analog voltage from a potentiometer and using that to adjust the speed of a DC motor
'''

#imports
from machine import Pin, PWM, ADC,
from time import sleep

#global counter
#counter = 0
pwm0 = PWM(Pin(0), freq = 2000, duty_u16 = 0)


while True:
    #global counter
    #sleep(0.25)
    adc_pot = ADC(Pin(26))
    '''adc_pot1 = ADC(Pin(27))
    adc_pot2 = ADC(Pin(28))
    adc_pot3 = ADC(Pin(29))'''
    #print("count: ", counter, "values: ", adc_pot.read_u16(), ", ", adc_pot1.read_u16(), ", ", adc_pot2.read_u16(), ", ", adc_pot3.read_u16() )
    #counter += 1
    pwm0.duty_u16(adc_pot.read_u16())


