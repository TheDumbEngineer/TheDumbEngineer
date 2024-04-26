#!/bin/bash

# Check if rp2.py is installed and available in PATH
command -v rp2.py >/dev/null 2>&1 || { echo >&2 "rp2.py is required but it's not installed or not in PATH. Aborting."; exit 1; }

# Prompt the user to enter the serial port
read -p "Enter the serial port for your Raspberry Pi Pico (e.g., /dev/ttyACM0): " SERIAL_PORT

# Check if the serial port is provided
if [ -z "$SERIAL_PORT" ]; then
    echo "Serial port cannot be empty. Aborting."
    exit 1
fi

# Prompt the user to enter the path to the MicroPython firmware file
read -p "Enter the path to the MicroPython firmware file (.uf2): " FIRMWARE_PATH

# Check if the firmware file exists
if [ ! -f "$FIRMWARE_PATH" ]; then
    echo "Firmware file not found at $FIRMWARE_PATH. Aborting."
    exit 1
fi

# Flash the MicroPython firmware
echo "Flashing MicroPython firmware onto Raspberry Pi Pico..."
rp2.py -p "$SERIAL_PORT" -b 115200 -f "$FIRMWARE_PATH"

# Check the exit status of rp2.py
if [ $? -eq 0 ]; then
    echo "Flashing successful!"
else
    echo "Error occurred while flashing MicroPython firmware."
fi
