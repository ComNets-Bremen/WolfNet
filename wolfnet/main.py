"""
Main wolf application

Jens Dede <jd@comnets.uni-bremen.de>

"""
import sys
from lib.utils import get_nodename, get_node_id, get_this_config, get_millis, blink, actor_on
from machine import Pin, SPI, I2C, Timer
import utime as time
import ubinascii
from config import encrypt_config, lora_parameters, device_config, node_params
import datahandler
import batteryhandler

from sx127x import SX127x
import ssd1306

import uasyncio

from nodetype import NodeTypes as NT

import random


ACK_RETRIES = 3
ACK_WAIT    = 1000 # ms


SHUTDOWN_DISPLAY_AFTER = 120
DEBOUNCE_TIME = 100 # ms

irq_triggered = False
irq_debounce_timer = get_millis()
irq_last_trigger = get_millis()

display_off_time = time.time() + SHUTDOWN_DISPLAY_AFTER
display_is_on = True

actor_timer = None
actor_timer_channel = None
actor_timer_timeout = 0

num_received_packets = 0

def irq_handler(pin):
    global irq_triggered, irq_debounce_timer
    if pin.value() and irq_debounce_timer + DEBOUNCE_TIME < get_millis():
        irq_triggered = True
        irq_debounce_timer = get_millis()

def flash_timer_handler(timer):
    global actor_pin, actor_timer_timeout, actor_timer
    if actor_timer_timeout < get_millis():
        timer.deinit()
        actor_pin.value(1)
        signal_status(0)
        actor_timer = None
    else:
        actor_pin.value(not actor_pin.value())

def ultrasonic_timer_handler(timer):
    global actor_pin, actor_timer_timeout, actor_timer
    timer.deinit()
    actor_pin.value(1)
    signal_status(0)
    actor_timer = None


def button_handler(pin):
    global display_off_time
    display_off_time = time.time() + SHUTDOWN_DISPLAY_AFTER

def signal_status(onoff):
    global status_led
    if status_led is not None:
        print("New LED status", onoff)
        status_led.value(onoff)

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

lora = None
try:
    lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)
except:
    print("Error init LoRa radio. Restart and try again.")
    sys.exit() # Soft reboot

actor_pin = Pin(12, Pin.OUT)
actor_pin.value(1)

# On Board LED
led = Pin(25, Pin.OUT)
led.value(0)

# On Board button
button = Pin(0, Pin.IN)
button.irq(button_handler)

print("This is node ID:  " + str(get_node_id()))
print("This is node HEX: " + str(get_node_id(True)))

dh = datahandler.DataHandler(encrypt_config["aes_key"])

nodeCfg = get_this_config()

irq_pin = None
if "gpio_button_irq" in nodeCfg:
    irq_pin = Pin(nodeCfg["gpio_button_irq"], Pin.IN, Pin.PULL_DOWN)
    irq_pin.irq(irq_handler)

status_led = None
if "gpio_led_status" in nodeCfg:
    print("Using status LED on pin", nodeCfg["gpio_led_status"])
    status_led = Pin(nodeCfg["gpio_led_status"], Pin.OUT)
    status_led.value(0)


if nodeCfg == None:
    print("Node not configured. Please update config.py")
    while(True):
        pass

bh = None

if "battery_type" in nodeCfg:
    if nodeCfg["battery_type"] == "max17043":
        bh = batteryhandler.Max17043BatteryStatus(i2c)
    elif nodeCfg["battery_type"] == "analog":
        bh = batteryhandler.AnalogBatteryStatus()

# TODO: Disable Device if Battery is too low

oled_changed = True
pkg_sent = 0

next_beacon_time = time.time()

node_config = None

if "receiver_type" in nodeCfg:
    node_config = node_params[nodeCfg["receiver_type"]]
    print("Node config", node_config)


packets_waiting_ack = []
dedup_list = []

last_event_start = 0

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
                (bindata, seq, ack) = dh.sendEncActor(nodeCfg)
                lora.println(bindata)
                if ack:
                    packets_waiting_ack.append((bindata, seq, get_millis(), 0))
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
                    lora.println(dh.encrypt(ack))


                current_packet_is_dup = False
                if packet.get_type() in (packet.TYPE_ACTOR_UNIVERSAL, ) and not nodeCfg["is_sender"]:
                    # remove duplicates
                    for item in dedup_list:
                        if item[0] == packet.get_sequence() and item[1] == packet.get_sender():
                            current_packet_is_dup = True
                            print("DUP")

                    dedup_list.append((packet.get_sequence(), packet.get_sender(), get_millis()))



                if packet.get_type() in (packet.TYPE_ACTOR_UNIVERSAL, ) and not nodeCfg["is_sender"] and not current_packet_is_dup:
                    if last_event_start + (node_config["block_time"] / 1000) > time.time():
                        print("Inside Block time. Skipping event.", last_event_start + (node_config["block_time"]/1000)-time.time())
                        continue

                    last_event_start = time.time()

                    if nodeCfg["receiver_type"] == NT.FLASH:
                        print("Acting as flash actor")

                        can_cancel = packet.get_params()[0]
                        duration = node_config["duration"]
                        frequency = node_config["frequency"]


                        if actor_timer != None and can_cancel:
                            try:
                                actor_timer.deinit()
                                actor_timer = None
                                actor_pin.value(1)
                                signal_status(0)
                                print("Cancelled Timer")
                            except:
                                pass
                        else:
                            oled.text('f:' + str(frequency) + "Hz", 0, 35)
                            oled.text('d:' + str(round(duration/1000.0,2)) + "s", 0,45)
                            signal_status(1)

                            actor_timer = Timer(3)
                            actor_timer_timeout = get_millis() + duration
                            actor_timer.init(mode=Timer.PERIODIC, period=int(1.0/frequency/2.0*1000.0), callback=flash_timer_handler)

                    elif nodeCfg["receiver_type"] == NT.ULTRASOUND_CANNON:
                        print("Acting as ultrasound actor")
                        can_cancel = packet.get_params()[0]
                        duration = node_config["duration"]

                        if actor_timer != None and can_cancel:
                            try:
                                actor_timer.deinit()
                                actor_timer = None
                                actor_pin.value(1)
                                signal_status(0)
                                print("Cancelled timer")
                            except:
                                pass
                        else:
                            oled.text('d:' + str(round(duration/1000.0,2)) + "s", 0,45)
                            actor_timer = Timer(3)
                            actor_timer_timeout = get_millis() + duration
                            actor_timer.init(mode=Timer.ONE_SHOT, period=duration, callback=ultrasonic_timer_handler)
                            actor_pin.value(0)
                            signal_status(1)
                    else:
                        print("Unhandled packet type")

                elif packet.get_type() == packet.TYPE_BEACON:
                    print("Received beacon from", packet.get_sender(), "with RSSI of ", packet.get_rssi(), "and SNR of", packet.get_snr())
                    print("Battery from beacon:", packet.getBattery())
                    oled.text('b:' + str(packet.get_sender()), 0, 35)
                    oled.text('r:' + str(packet.get_rssi()) + " s:" + str(packet.get_snr()), 0,45)

                elif packet.get_type() == packet.TYPE_ACK:
                    # Remove acked packets from the list
                    print("Got ack from", packet.get_sender(), "with seq", packet.get_sequence())
                    reack = []

                    for pkg in packets_waiting_ack:
                        if pkg[1] == packet.get_sequence():
                            continue
                        reack.append(pkg)
                    packets_waiting_ack = reack
                    del reack

            else:
                print("Sniffed_packet")
                print("!{"+str(ubinascii.hexlify(payload).decode())+"}#")
                oled.text('sp:' + str(num_received_packets), 0, 35)
            oled_changed = True

    if oled_changed:
        oled_changed = False
        oled.show()

    # Handle ACKs
    reack = []
    for pkg in packets_waiting_ack:
        # packets_waiting_ack.append((bindata, seq, time.time(), 0))
        pkg = list(pkg)
        if (pkg[2] + ACK_WAIT) < get_millis(): # retry
            print("Retry")
            pkg[3] = pkg[3] + 1
            pkg[2] = get_millis()
            pkg_sent += 1
            lora.println(pkg[0])

        if pkg[3] >= ACK_RETRIES:
            continue

        reack.append(pkg)

    packets_waiting_ack = reack
    del reack


    # Tidy up dedup list
    dedup = []
    for pkg in dedup_list:
        if pkg[-1] + (2*ACK_RETRIES*ACK_WAIT) < get_millis():
            continue
        else:
            dedup.append(pkg)
    current_packet_is_dup = dedup
    del dedup
    