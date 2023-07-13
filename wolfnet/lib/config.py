import packets
from nodetype import NodeTypes

# Copyright 2020 LeMaRiva|tech lemariva.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
# ES32 TTGO v1.0
device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,
    'led':2,
}

# M5Stack ATOM Matrix
device_config = {
    'miso':23,
    'mosi':19,
    'ss':22,
    'sck':33,
    'dio_0':25,
    'reset':21,
    'led':12,
}
"""

# Heltec LoRa module
device_config = {
    'miso': 19,
    'mosi': 27,
    'ss': 18,
    'sck': 5,
    'dio_0': 26,
    'reset': 14,
    'led': 25,
}

app_config = {
    'loop': 200,
    'sleep': 100,
}

lora_parameters = {
    'frequency': 868E6,
    'tx_power_level': 2,
    'signal_bandwidth': 125E3,
    'spreading_factor': 7,
    'coding_rate': 5,
    'preamble_length': 8,
    'implicit_header': False,
    'sync_word': 0x12,  # 0x12 = private, 0x34 = public
    'enable_CRC': False,
    'invert_IQ': False,
}

wifi_config = {
    'ssid': '',
    'password': ''
}

# Network wide encryption parameters
encrypt_config = {
    "aes_key": b"ausme8Sdk29dswapausme8Sdk29dswab"
}


node_params = {
    NodeTypes.FLASH: {
        "frequency": 20,  # Hz
        "duration": 5000,  # ms
        "block_time": 10000,  # ms
    },
    NodeTypes.ULTRASOUND_CANNON: {
        "duration": 22000,  # ms
        "block_time": 30000,  # ms
    }

}

# Per node config parameters, stored by node id
nodes_config = {

    # Start SET 1
    "4172078668": {  # PIR sensor 1, 07.2023
        "is_sender": True,
        "actor_node": 106440645,  # Either address or none to Broadcast
        "action_cancel_previous" : False,
        "protection_time": 1000,  # 1000 ms = 1 sec
        "beacon_interval": 120,  # seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "max17043",
        "gpio_button_irq": 13,  # IRQ on pin 13
        "use_ack": True,  # Use acks
    },
    "2583535806": {  # PIR sensor 2, 07.2023, schwarz
        "is_sender": True,
        "actor_node": 106440645,  # Either address or none to Broadcast
        "action_cancel_previous" : False,
        "protection_time": 1000,  # 1000 ms = 1 sec
        "beacon_interval": 120,  # seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "max17043",
        "gpio_button_irq": 13,  # IRQ on pin 13
        "use_ack": True,  # Use acks
    },
    "106440645": {  # General actor, 2023-07-12
        "is_sender": False,
        # "receiver_type": NodeTypes.ULTRASOUND_CANNON,
        "receiver_type": NodeTypes.FLASH,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "gpio_led_status": 13,  # Status LED on pin 13
    },

    # ENDE SET 1




    "2276286798": {  # PIR sensor
        "is_sender": True,
        "actor_node": None,  # Either address or none to Broadcast
        "msg_type": NodeTypes.FLASH,
        "action_frequency": 20,  # Hz
        "action_duration": 4000,  # 4000 ms = 4 sec
        "action_cancel_previous": False,
        "protection_time": 60000,  # 60000 ms = 60 sec
        "beacon_interval": 240,  # seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "max17043",
        "gpio_button_irq": 13,  # IRQ on pin 13
    },
    "2424541685": {  # PIR sensor 3, 07.2023, schwarz
        "is_sender": True,
        "actor_node": None,  # Either address or none to Broadcast
        "msg_type": NodeTypes.FLASH,
        "action_frequency": 20,  # Hz
        "action_duration": 4000,  # 4000 ms = 4 sec
        "action_cancel_previous": False,
        "protection_time": 60000,  # 60000 ms = 60 sec
        "beacon_interval": 240,  # seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "max17043",
        "gpio_button_irq": 13,  # IRQ on pin 13
    },

    "320270687": {  # Ultrasonic actor, 2023-07-05
        "is_sender": False,
        "receiver_type": NodeTypes.ULTRASOUND_CANNON,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "action_cancel_previous": True,
        "action_duration": 10000,  # 10000 ms = 10 sec
    },



    "4291548233": {  # Flash actor
        "is_sender": False,
        "receiver_type": NodeTypes.FLASH,
        "beacon_interval": 240,  # seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36, hardcoded
    },
    "1892008357": {  # Sniffer
        "is_sender": False,
        "is_sniffer": True,
    },
    "510366793": {  # Buzzer
        "is_sender": True,
        "msg_type": NodeTypes.FLASH,
        "is_sniffer": False,
        "battery_type": "max17043",
        "actor_node": None,
        "action_cancel_previous": True,
        "action_frequency": 25,  # Hz (if applicable)
        "action_duration": 10000,  # 10000 ms = 10 sec
        "protection_time": 1000,  # 1000 ms = 1 sec
        "beacon_interval": 240,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "gpio_button_irq": 13,  # IRQ on pin 13
    },

    "2628889781": {  # Buzzer 2 2023-04
        "is_sender": True,
        "msg_type": NodeTypes.FLASH,
        "is_sniffer": False,
        "battery_type": "max17043",
        "actor_node": None,
        "action_cancel_previous": True,
        "action_frequency": 20,  # Hz (if applicable)
        "action_duration": 10000,  # 10000 ms = 10 sec
        "protection_time": 1000,  # 1000 ms = 1 sec
        "beacon_interval": 240,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "gpio_button_irq": 13,  # IRQ on pin 13
    },
    "1054058": {  # Ultrasonic actor
        "is_sender": False,
        "receiver_type": NodeTypes.ULTRASOUND_CANNON,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "action_cancel_previous": True,
        "action_duration": 10000,  # 10000 ms = 10 sec
    },
    "951712297": {  # Flash Actor
        "is_sender": False,
        "receiver_type": NodeTypes.FLASH,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "action_cancel_previous": True,
        "action_duration": 10000,  # 10000 ms = 10 sec
        "gpio_led_status": 13,  # Status LED on pin 13
    },
    "2308316059": {  # Flash Actor 2, 2023-04
        "is_sender": False,
        "receiver_type": NodeTypes.FLASH,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "action_cancel_previous": True,
        "action_duration": 10000,  # 10000 ms = 10 sec
        "gpio_led_status": 13,  # Status LED on pin 13
    },
    "3567154165": {  # Ultrasonic actor, 2023-04
        "is_sender": False,
        "receiver_type": NodeTypes.ULTRASOUND_CANNON,
        "beacon_interval": 120,  # 120 seconds
        "beacon_jitter": 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type": "analog",  # Read battery from Pin 36
        "action_cancel_previous": True,
        "action_duration": 10000,  # 10000 ms = 10 sec
        "gpio_led_status": 13,  # Status LED on pin 13
    },
}
