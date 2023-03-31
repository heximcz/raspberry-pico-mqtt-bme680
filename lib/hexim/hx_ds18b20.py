from adafruit_ds18x20 import DS18X20
from adafruit_onewire.bus import OneWireBus

class DS18B20:

    def __init__(self, ow_bus: OneWireBus, offset_temperature: float = 0) -> None:
        """
        :param float offset_temperature
        """

        # DS18
        self.ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

        self.offset_temperature = offset_temperature

    def get_measurement(self) -> float:
        temperature = self.ds18.temperature
        temperature = round(temperature + self.offset_temperature,1)
        return temperature
