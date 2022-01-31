"""
Main wolf application

Jens Dede <jd@comnets.uni-bremen.de>

"""

from lib.utils import get_nodename, get_node_id, get_this_config, get_millis, blink
from machine import Pin, SPI, I2C
import utime as time
import ubinascii
from config import encrypt_config, lora_parameters, device_config
import datahandler
import batteryhandler

from sx127x import SX127x
import ssd1306

import uasyncio

import random

SHUTDOWN_DISPLAY_AFTER = 120

irq_triggered = False
irq_last_trigger = get_millis()

display_off_time = time.time() + SHUTDOWN_DISPLAY_AFTER
display_is_on = True

num_received_packets = 0

def irq_handler(pin):
    global irq_triggered
    if pin.value():
        irq_triggered = True

def button_handler(pin):
    global display_off_time
    display_off_time = time.time() + SHUTDOWN_DISPLAY_AFTER

# Heltec LoRa 32 with OLED Display
oled_width = 128
oled_height = 64
# OLED reset pin
i2c_rst = Pin(16, Pin.OUT)
# Initialize the OLED display
i2c_rst.value(0)
time.sleep_ms(5)
i2c_rst.value(1) # must be held high after initialization
# Setup the I2C lines
i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
# Create the bus object
i2c = I2C(scl=i2c_scl, sda=i2c_sda)
# Create the display object
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)
  
#oled.line(0, 0, 50, 25, 1)
oled.show()

device_spi = SPI(baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)

actor_pin = Pin(12, Pin.OUT)
actor_pin.value(1)
irq_pin = Pin(13, Pin.IN, Pin.PULL_DOWN)
irq_pin.irq(irq_handler)

led = Pin(25, Pin.OUT)
led.value(0)

button = Pin(0, Pin.IN)
button.irq(button_handler)

print("This is node ID:  " + str(get_node_id()))
print("This is node HEX: " + str(get_node_id(True)))

dh = datahandler.DataHandler(encrypt_config["aes_key"])

nodeCfg = get_this_config()

bh = None

if "battery_type" in nodeCfg:
    if nodeCfg["battery_type"] == "max17043":
        bh = batteryhandler.Max17043BatteryStatus(i2c)
    elif nodeCfg["battery_type"] == "analog":
        bh = batteryhandler.AnalogBatteryStatus()

oled_changed = True
pkg_sent = 0

next_beacon_time = time.time()

while True:
    if display_is_on and display_off_time < time.time():
        oled.poweroff()
        display_is_on = False
    elif not display_is_on and display_off_time > time.time():
        oled.poweron()
        display_is_on = True
        oled_changed = True

    oled.fill(0)
    oled.text("ID:  " + str(get_node_id()), 0, 0)
    oled.text("HEX: " + str(get_node_id(True)), 0,10)

    if irq_triggered:
        if get_millis() > irq_last_trigger + nodeCfg["protection_time"]:
            irq_last_trigger = get_millis()
            if nodeCfg and "is_sender" in nodeCfg and nodeCfg["is_sender"]:
                print("Sending alarm message")
                bindata = dh.sendEncFlash(nodeCfg["flash_node"], nodeCfg["flash_duration"], nodeCfg["flash_frequency"])
                lora.println(bindata)
                pkg_sent += 1

                oled.text("#TX: " + str(pkg_sent), 0, 55)
                oled_changed = True
        else:
            print("Alarm was " + str((irq_last_trigger + nodeCfg["protection_time"] - get_millis()) / 1000.0) + "s too early")

        irq_triggered = False

    
    if time.time() > next_beacon_time and "beacon_interval" in nodeCfg:
        print("Sending out beacon")
        bindata = dh.sendEncBeacon()
        if bh:
            bat_data = bh.do_read()
            if bat_data:
                print("Attaching battery status to beacon:", bat_data)
                bat = (int(bat_data[0]), int(bat_data[1]*1000))
                bindata = dh.sendEncBeacon(bat=bat)
        lora.println(bindata)
        jitter = 0
        if "beacon_jitter" in nodeCfg:
            jitter = random.randint(-nodeCfg["beacon_jitter"], nodeCfg["beacon_jitter"])

        next_beacon_time += nodeCfg["beacon_interval"] + jitter

        print(time.time(), next_beacon_time)

    if lora.received_packet():
        payload = lora.read_payload()
        #print(payload)
        packet = None
        is_sniffer = False

        if "is_sniffer" in nodeCfg:
            is_sniffer = nodeCfg["is_sniffer"]

        try:
            packet = dh.receiverEncPacket(bytearray(payload), is_sniffer)
        except:
            print("Packet parsing failed. Not for us?")
        if packet:
            packet.set_rssi(lora.packet_rssi())
            packet.set_snr(lora.packet_snr())
            print("Received:", packet)
            num_received_packets += 1

            print("Total received packets:", num_received_packets)

            if not is_sniffer:
                ack = packet.create_ack()
                if ack:
                    lora.println(dh.encrypt(ack.create_packet()))
                if packet.get_type() == packet.TYPE_ACTOR_FLASH:
                    duration, frequency = packet.get_flash()
                    oled.text('f:' + str(frequency) + "Hz", 0, 35)
                    oled.text('d:' + str(round(duration/1000.0,2)) + "s", 0,45)
                    uasyncio.run(blink(actor_pin, frequency, duration))

                elif packet.get_type() == packet.TYPE_BEACON:
                    print("Received beacon from", packet.get_sender(), "with RSSI of ", packet.get_rssi(), "and SNR of", packet.get_snr())
                    oled.text('b:' + str(packet.get_sender()), 0, 35)
                    oled.text('r:' + str(packet.get_rssi()) + " s:" + str(packet.get_snr()), 0,45)

            else:
                print("Sniffed_packet")
                print("!{"+str(ubinascii.hexlify(payload).decode())+"}#")
                oled.text('sp:' + str(num_received_packets), 0, 35)
            oled_changed = True

    if oled_changed:
        oled_changed = False
        oled.show()
