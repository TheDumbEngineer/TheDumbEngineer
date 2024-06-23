import machine
import utime
from i2c_lcd import I2cLcd

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

# Stepper motor control pins
stepper_pins = [
    machine.Pin(6, machine.Pin.OUT),  # IN1
    machine.Pin(7, machine.Pin.OUT),  # IN2
    machine.Pin(8, machine.Pin.OUT),  # IN3
    machine.Pin(9, machine.Pin.OUT)   # IN4
]

# Stepper motor steps for one revolution
step_sequence = [
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [0, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 1, 1],
    [0, 0, 0, 1],
    [1, 0, 0, 1]
]

# Variables to track button states
button_state = button_pin.value()
prev_button_state = button_state

# Function to display LED and motor state on the LCD
def update_lcd(led_state, motor_state):
    lcd.clear()  # Clear the LCD before writing new text
    utime.sleep_ms(100)  # Give a small delay to ensure clearing completes
    
    if led_state:
        lcd.move_to(0, 0)
        lcd.putstr("LED: ON")
    else:
        lcd.move_to(0, 0)
        lcd.putstr("LED: OFF")
        
    if motor_state:
        lcd.move_to(0, 1)
        lcd.putstr("Motor: RUNNING")
    else:
        lcd.move_to(0, 1)
        lcd.putstr("Motor: STOPPED")

# Function to control stepper motor steps
def step_motor(steps, direction=1, delay=10):
    for _ in range(steps):
        for step in step_sequence[::direction]:
            for pin, value in zip(stepper_pins, step):
                pin.value(value)
            utime.sleep_ms(delay)

# Display initial states
update_lcd(led_pin.value(), False)

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
                motor_running = led_pin.value() == 1
                update_lcd(led_pin.value(), motor_running)
                
                # If LED is ON, run the stepper motor
                if motor_running:
                    step_motor(512, direction=1, delay=5)  # Run motor for 512 steps (one revolution)
                else:
                    for pin in stepper_pins:
                        pin.value(0)  # Stop the motor by setting all pins to low
    
    # Update the previous button state
    prev_button_state = button_state
    
    # Short delay to reduce CPU usage
    utime.sleep_ms(50)
