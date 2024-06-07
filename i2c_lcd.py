from micropython import const
import time
import ustruct
from machine import I2C

# Commands
LCD_CLEARDISPLAY = const(0x01)
LCD_RETURNHOME = const(0x02)
LCD_ENTRYMODESET = const(0x04)
LCD_DISPLAYCONTROL = const(0x08)
LCD_CURSORSHIFT = const(0x10)
LCD_FUNCTIONSET = const(0x20)
LCD_SETCGRAMADDR = const(0x40)
LCD_SETDDRAMADDR = const(0x80)

# Flags for display entry mode
LCD_ENTRYRIGHT = const(0x00)
LCD_ENTRYLEFT = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

# Flags for display on/off control
LCD_DISPLAYON = const(0x04)
LCD_DISPLAYOFF = const(0x00)
LCD_CURSORON = const(0x02)
LCD_CURSOROFF = const(0x00)
LCD_BLINKON = const(0x01)
LCD_BLINKOFF = const(0x00)

# Flags for display/cursor shift
LCD_DISPLAYMOVE = const(0x08)
LCD_CURSORMOVE = const(0x00)
LCD_MOVERIGHT = const(0x04)
LCD_MOVELEFT = const(0x00)

# Flags for function set
LCD_8BITMODE = const(0x10)
LCD_4BITMODE = const(0x00)
LCD_2LINE = const(0x08)
LCD_1LINE = const(0x00)
LCD_5x10DOTS = const(0x04)
LCD_5x8DOTS = const(0x00)

# Flags for backlight control
LCD_BACKLIGHT = const(0x08)
LCD_NOBACKLIGHT = const(0x00)

En = const(0b00000100)  # Enable bit
Rw = const(0b00000010)  # Read/Write bit
Rs = const(0b00000001)  # Register select bit

class I2cLcd:
    def __init__(self, i2c, address, num_lines, num_columns):
        self.i2c = i2c
        self.address = address
        self.num_lines = num_lines
        self.num_columns = num_columns
        self.backlight = LCD_BACKLIGHT
        self.display_function = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
        if num_lines > 1:
            self.display_function |= LCD_2LINE
        self.display_control = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display_mode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

        self._write_cmd(0x03)
        time.sleep_ms(5)
        self._write_cmd(0x03)
        time.sleep_ms(5)
        self._write_cmd(0x03)
        time.sleep_ms(5)
        self._write_cmd(0x02)

        self._write_cmd(LCD_FUNCTIONSET | self.display_function)
        self._write_cmd(LCD_DISPLAYCONTROL | self.display_control)
        self.clear()
        self._write_cmd(LCD_ENTRYMODESET | self.display_mode)
        self._write_cmd(LCD_DISPLAYCONTROL | self.display_control | LCD_DISPLAYON)

    def clear(self):
        self._write_cmd(LCD_CLEARDISPLAY)
        time.sleep_ms(2)

    def move_to(self, column, row):
        if row > self.num_lines:
            row = self.num_lines - 1
        self._write_cmd(LCD_SETDDRAMADDR | (column + 0x40 * row))

    def putstr(self, string):
        for char in string:
            self._write_char(ord(char))

    def _write_cmd(self, cmd):
        self._write(cmd, 0)

    def _write_char(self, char_value):
        self._write(char_value, Rs)

    def _write(self, data, mode):
        high = mode | (data & 0xF0) | self.backlight
        low = mode | ((data << 4) & 0xF0) | self.backlight
        self.i2c.writeto(self.address, ustruct.pack('BB', high | En, high & ~En))
        self.i2c.writeto(self.address, ustruct.pack('BB', low | En, low & ~En))


