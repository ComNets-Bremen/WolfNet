Jens Dede, <jd@comnets.uni-bremen.de>

Licence for AES lib: https://github.com/iyassou/mpyaes MIT license


Idea of basic data packet:

        '''
        VERSION uint_8
            0x0 init version
        SEQUENCE uint_16
        SENDER_ID uint_32
        CONFIG uint 8, bits
            #0   = broadcast
            #1   = is ACK
            #2   = ACK requested
        if not broadcast:
            RECEIVER_ID uint_32
        TYPE uint_8
            0x0     undefined
            0x1     ACK
            0x2     STATUS
            0x3     CONFIG
            0x4     BEACON
            0x11    ACTOR_FLASH
            0x21    ACTOR_ULTRASONIC
        DATALEN uint_8
        N data bytes
        CRC uint_32
        '''



New one for SX126x: https://github.com/ehong-tl/micropySX126X
Old one for SX1276: https://github.com/lemariva/uPyLoRaWAN
