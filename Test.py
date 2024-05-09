# MicroPython code to blink an LED connected to GPIO pin 0 (GP0) on Raspberry Pi Pico

import machine
import utime

led_pin = machine.Pin(0, machine.Pin.OUT)  # Define GP0 as an output pin

while True:
    led_pin.toggle()  # Toggle the state of the LED
    utime.sleep_ms(500)  # Wait for 500 milliseconds (0.5 seconds)
