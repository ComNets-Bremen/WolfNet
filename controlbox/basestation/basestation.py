#!/usr/bin/env python3

""" A simple continuous receiver class. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.


from time import sleep, time, localtime
from SX127x.LoRa import *
#from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD
import datahandler
from config import encrypt_config
from savetofile import MyRecord
from packets import BasePacket

BOARD.setup()
BOARD.reset()
idnumber = 0
#parser = LoRaArgumentParser("Continous LoRa receiver.")


class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        packet = dh.receiverEncPacket(bytes(payload))
        packet.set_rssi(self.get_pkt_rssi_value())
        packet.set_snr(self.get_pkt_snr_value())
        print(packet)
        global idnumber
        idnumber = idnumber + 1
        if packet.get_type() == BasePacket.TYPE_ACTOR_UNIVERSAL:
            params = packet.get_params()
            battery = [0,0]
        elif packet.get_type() == BasePacket.TYPE_BEACON:
            battery = packet.getBattery()
            params = [0,0]
        savethis = MR(str(idnumber), str(str(localtime()[2]) + '.' +  str(localtime()[1]) + '.' + str(localtime()[0]) + '; ' + str(localtime()[3]) + ':' +  str(localtime()[4]) + ':' + str(localtime()[5])), str(packet.get_sender()), str(packet.get_receiver()), str(packet.get_broadcast()), battery[0], str(battery[1]/1000), params[0], params[1], str(packet.get_rssi()), str(packet.get_snr()))
        MR.savedata(savethis)
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        BOARD.led_off()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))


lora = LoRaRcvCont(verbose=True)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)
lora.set_bw(BW.BW125)
lora.set_coding_rate(CODING_RATE.CR4_5)
lora.set_spreading_factor(7)
lora.set_rx_crc(False)
lora.set_freq(868.0)

dh = datahandler.DataHandler(encrypt_config["aes_key"])
MR = MyRecord
MR.setup()




print(lora)
assert(lora.get_agc_auto_on() == 1)

try: input("Press enter to start...")
except: pass

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    print("")
    lora.set_mode(MODE.SLEEP)
    print(lora)
    BOARD.teardown()
