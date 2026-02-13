# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example sketch to connect to PM2.5 sensor with either I2C or UART.
"""

import time
import csv
import board
import busio
from digitalio import DigitalInOut, Direction, Pull

from adafruit_pm25.i2c import PM25_I2C

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


# For use with a computer running Windows:
# import serial
# uart = serial.Serial("COM30", baudrate=9600, timeout=1)

# For use with microcontroller board:
# (Connect the sensor TX pin to the board/computer RX pin)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)

# For use with Raspberry Pi/Linux:
import serial
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)

# For use with USB-to-serial cable:
# import serial
# uart = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.25)

# Connect to a PM2.5 sensor over UART
from adafruit_pm25.uart import PM25_UART
pm25 = PM25_UART(uart, reset_pin)

# Create library object, use 'slow' 100KHz frequency!
# i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
# Connect to a PM2.5 sensor over I2C
# pm25 = PM25_I2C(i2c, reset_pin)

# create a csv file that we can read later
file = open('AirQuality.csv', 'w', newline = None)
csvwriter = csv.writer(file, delimiter = ',')

# writing out the meta data
meta = ['t_s', 'pm10_standard', 'pm25_standard', 'pm100_standard', 'pm10 env', 'pm25 env', 'pm100 env', 'particles 03um', 'particles 05um',
        'particles 10um', 'particles 25um', 'particles 50um', 'particles 100um']
csvwriter.writerow(meta)

print("Found PM2.5 sensor, reading data...")

time_stamp = time.ctime()
time_int_start = int(time.time())
time_int_stop = 0

while time_int_stop <= (time_int_start + 30):
    time_int_stop = int(time.time())
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print(f"Time Stamp:  {time_stamp}")
    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    csvwriter.writerow([time_int_stop, aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"], aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"],
                        aqdata["particles 03um"], aqdata["particles 05um"], aqdata["particles 10um"], aqdata["particles 25um"], aqdata["particles 50um"], aqdata["particles 100um"]])
