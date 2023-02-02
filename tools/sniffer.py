#!/usr/bin/env python3

PORT="/dev/ttyUSB0"

import serial

with serial.Serial(PORT, 11520, timeout=2) as ser:
    while True:
        line = ser.readline()
        if len(line):
            print(line)

