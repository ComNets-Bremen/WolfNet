import mpyaes

from packets import FlashPacket, BasePacket, BeaconPacket
from utils import get_node_id

class DataHandler:
    def __init__(self, key):
        if type(key) != bytes:
            raise ValueError("Key has to be a byte array")
        if len(key) != 32:
            raise ValueError("Key has to be 16 bytes long")
        self.key = key


    def encrypt(self, data):
        iv = mpyaes.generate_IV(16)
        cipher = mpyaes.new(self.key, mpyaes.MODE_CBC, iv)
        return iv + cipher.encrypt(data)

    def decrypt(self, data):
        iv = data[:16]
        cipher = mpyaes.new(self.key, mpyaes.MODE_CBC, iv)
        return cipher.decrypt(data[16:])


    def sendEncFlash(self, receiver, duration, frequency):
        fp = FlashPacket(get_node_id())
        fp.set_flash(duration, frequency)
        fp.set_receiver(receiver)
        return self.encrypt(fp.create_packet())


    def sendEncBeacon(self):
        bp = BeaconPacket(get_node_id())
        return self.encrypt(bp.create_packet())

    def receiverEncPacket(self, packet):
        data = self.decrypt(packet)
        p = BasePacket()
        p.parse_packet(data)
        if p.get_type() == BasePacket.TYPE_ACTOR_FLASH:
            p = FlashPacket()
            p.parse_packet(data)

        elif p.get_type() == BasePacket.TYPE_BEACON:
            p = BeaconPacket()
            p.parse_packet(data)


        if p.get_broadcast() or p.get_receiver() == get_node_id():
            return p
        
        # packet not for us
        print("Dropping packet: Not for us")
        return None

