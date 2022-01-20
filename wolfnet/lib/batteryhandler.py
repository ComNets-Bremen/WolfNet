from machine import Pin, ADC
from max17043 import max17043


class BatteryHandler:
    adc = None
    adc_pin = None
    max17043 = None

    def __init__(self):
        pass

    def do_wakeup(self):
        pass

    def do_sleep(self):
        pass

    def do_read(self):
        return (None, None)


class AnalogBatteryStatus:
    def __init__(self, analog_pin=Pin(36)):
        self.adc_pin = analog_pin
        self.adc = ADC(self.adc_pin)
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)

    def do_read(self):
        if self.adc:
            return self.adc.read() * 3.6 / 4095
        return None

class Max17043BatteryStatus:
    def __init__(self, i2c):
        try:
            self.max17043 = max17043(i2c)
            print("Gauge:", self.max17043)
            print("%:", self.max17043.getSoc())
            print("V:", self.max17043.getVCell())
        except:
            print("Cannot connect to fuel gauge")
            self.max17043 = None

    def do_read(self):
        if self.max17043:
            return (self.max17043.getSoc(), self.max17043.getVCell())
        return None

