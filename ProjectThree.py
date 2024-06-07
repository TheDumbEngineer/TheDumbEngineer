import machine
import utime
from i2c_lcd import I2cLcd  # Ensure i2c_lcd.py is on the Pico

# Define the I2C address of the LCD (use the address detected by the I2C scanner)
I2C_ADDR = 0x27  # Replace with your LCD's I2C address
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C on bus 1 with SDA on Pin 2 and SCL on Pin 3
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=100000)

# Initialize the LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Define GP0 as an output pin for the LED
led_pin = machine.Pin(0, machine.Pin.OUT)

# Define GP1 as an input pin with a pull-up resistor for the button
button_pin = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)

# Variables to track button states
button_state = button_pin.value()
prev_button_state = button_state

# Function to display LED state on the LCD
def update_lcd(led_state):
    lcd.clear()  # Clear the LCD before writing new text
    utime.sleep_ms(100)  # Give a small delay to ensure clearing completes
    
    if led_state:
        lcd.move_to(0, 0)
        lcd.putstr("LED: ON")
    else:
        lcd.move_to(0, 0)
        lcd.putstr("LED: OFF")

# Display initial state
update_lcd(led_pin.value())

# Main loop
while True:
    # Read the state of the button
    button_state = button_pin.value()
    
    # Check if the button state has changed (active low)
    if button_state != prev_button_state:
        # Debounce delay
        utime.sleep_ms(20)
        # Confirm the state change
        if button_state == button_pin.value():
            # If the button is pressed
            if button_state == 0:
                # Toggle the LED
                led_pin.toggle()
                # Update the LCD with the new LED state
                update_lcd(led_pin.value())
    
    # Update the previous button state
    prev_button_state = button_state
    
    # Short delay to reduce CPU usage
    utime.sleep_ms(50)

