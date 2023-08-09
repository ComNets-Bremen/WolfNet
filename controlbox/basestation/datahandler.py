from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

from packets import UniversalPacket, BasePacket, BeaconPacket

class DataHandler:
    def __init__(self, key):
        if type(key) != bytes:
            raise ValueError("Key has to be a byte array")
        if len(key) != 32:
            raise ValueError("Key has to be 16 bytes long")
        self.key = key


    def decrypt(self, data):
        iv = data[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(data[16:]), AES.block_size)
        

    def receiverEncPacket(self, packet, is_sniffer=False):
        data = self.decrypt(packet)
        p = BasePacket()
        p.parse_packet(data)

        if p.get_type() == BasePacket.TYPE_ACTOR_UNIVERSAL:
            p = UniversalPacket()
            p.parse_packet(data)

        elif p.get_type() == BasePacket.TYPE_BEACON:
            p = BeaconPacket()
            p.parse_packet(data)


        if p.get_broadcast():
            return p
        
        # packet not for us
        print("Dropping packet: Not for us")
        return None

