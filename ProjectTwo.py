# MicroPython code to toggle an LED connected to GPIO pin 0 (GP0) on Raspberry Pi Pico
# using a push button connected to GPIO pin 1 (GP1)

import machine
import utime

led_pin = machine.Pin(0, machine.Pin.OUT)  # Define GP0 as an output pin
button_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)  # Define GP1 as an input pin with pull-up resistor

button_state = 0  # Variable to track button state
prev_button_state = 0  # Variable to track previous button state

while True:
    button_state = button_pin.value()  # Read the state of the button
    
    if button_state != prev_button_state:  # If button state changes
        if button_state == 0:  # If button is pressed
            led_pin.toggle()  # Toggle the state of the LED
            
    prev_button_state = button_state  # Update previous button state
    utime.sleep_ms(20)  # Add a small delay to debounce the button