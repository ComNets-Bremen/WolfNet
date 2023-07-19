#!/usr/bin/env python3

# Read the data from the serial line if a node is in sniffer mode
# Jens Dede, 2023, jd@comnets.uni-bremen.de

PORT="/dev/ttyUSB0"

import serial

with serial.Serial(PORT, 11520, timeout=2) as ser:
    while True:
        line = ser.readline()
        if len(line):
            print(line)

