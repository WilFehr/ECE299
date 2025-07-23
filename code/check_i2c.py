from machine import Pin, I2C

i2c = I2C(scl=Pin(21), sda=Pin(20), freq=200000)

devices = i2c.scan()

if len(devices) == 0:
   print("No I2C devices found")
else:
   print('I2C devices found:', len(devices))
   for device in devices:
       print("Hexadecimal address:", hex(device))
