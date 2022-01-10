"""
D1 mini

Pin     Function                ESP-8285 Pin
TX      TXD                     TXD
RX      RXD                     RXD
A0      Analog input, max 3.2V  A0
D0      IO                      GPIO16
D1      IO, SCL                 GPIO5
D2      IO, SDA                 GPIO4
D3      IO, 10k Pull-up         GPIO0
D4      IO, 10k Pull-up, LED    GPIO2
D5      IO, SCK                 GPIO14
D6      IO, MISO                GPIO12
D7      IO, MOSI                GPIO13
D8      IO, 10k Pull-down, SS   GPIO15
G       Ground                  GND
5V      5V                      -
3V3     3.3V                    3.3V
RST     Reset                   RST
"""


"""
D1 mini pro


Pin     Function                ESP-8266 Pin
TX      TXD                     TXD
RX      RXD                     RXD
A0      Analog input, max 3.2V  A0
D0      IO                      GPIO16
D1      IO, SCL                 GPIO5
D2      IO, SDA                 GPIO4
D3      IO, 10k Pull-up         GPIO0
D4      IO, 10k Pull-up, LED    GPIO2
D5      IO, SCK                 GPIO14
D6      IO, MISO                GPIO12
D7      IO, MOSI                GPIO13
D8      IO, 10k Pull-down, SS   GPIO15
G       Ground                  GND
5V      5V                      -
3V3     3.3V                    3.3V
RST     Reset                   RST
"""


from machine import Pin
import utime as time

INTERVAL = 50

half_int = int(float(INTERVAL)/2.0)

ledpin = Pin(14, Pin.OUT)


while True:
    ledpin.value(0)
    print("Val:", 0, "int", INTERVAL)
    time.sleep_ms(half_int)
    ledpin.value(1)
    print("Val:", 1)
    time.sleep_ms(half_int)

