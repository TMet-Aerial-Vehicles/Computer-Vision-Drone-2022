"""Class to communicate with Arduino via serial port communication"""

import serial


SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600
# To identify the serial device name of your Arduino:
#   Run ls /dev/tty*
# Example: /dev/ttyACM0, or /dev/ttyUSB0 or /dev/ttyACM1.


class SerialCommunication:

    def __init__(self):
        # Initial Serial and clear it
        self.serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        self.serial.reset_input_buffer()

    def read(self):
        # while True:
        if self.serial.in_waiting > 0:
            line = self.serial.readline()
            if line != b'':
                # Handle Arduino input
                print(line)

    def write(self):
        self.serial.write(b'hello')
