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

#Heltec LoRa module
device_config = {
    'miso':19,
    'mosi':27,
    'ss':18,
    'sck':5,
    'dio_0':26,
    'reset':14,
    'led':25, 
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
    'sync_word': 0x12,  #0x12 = private, 0x34 = public
    'enable_CRC': False,
    'invert_IQ': False,
}

wifi_config = {
    'ssid':'',
    'password':''
}

# Network wide encryption parameters
encrypt_config = {
    "aes_key" : b"ausme8Sdk29dswapausme8Sdk29dswap"
}

# Per node config parameters, stored by node id
nodes_config = {
    "2276286798" : {
        "is_sender" : True,
        "flash_node" : 4291548233,
        "flash_frequency" : 20, # Hz
        "flash_duration"  : 4000, # 4000 ms = 4 sec
        "protection_time" : 60000, # 60000 ms = 60 sec
        "beacon_interval" : 120, # 120 seconds
        "beacon_jitter" : 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type" : "max17043",
    },
    "4291548233" : {
        "is_sender" : False,
        "beacon_interval" : 120, # 120 seconds
        "beacon_jitter" : 10,    # seconds, will vary the above value by +- 10 seconds
        "battery_type" : "analog", # Read battery from Pin 36
    },
    "1892008357": {
        "is_sender" : False,
        "is_sniffer" : True,
    }
}