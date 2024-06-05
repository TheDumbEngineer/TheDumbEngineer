import machine
import utime
from machine import Pin, I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# Define I2C connections and LCD size
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Initialize button on GPIO 1 with pull-up resistor
button = Pin(1, Pin.IN, Pin.PULL_UP)

# Main loop
while True:
    if button.value() == 0:  # Active low due to pull-up resistor
        lcd.clear()
        lcd.putstr("LED ON")
    else:
        lcd.clear()
        lcd.putstr("LED OFF")
    utime.sleep(0.1)
