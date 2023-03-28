from adafruit_ds18x20 import DS18X20

class DS18B20:

    def __init__(self, ow_bus, offset_temperature = 0):
        """
        :param float offset_temperature
        :param float offset_humidity
        """

        # DS18
        self.ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

        self.offset_temperature = offset_temperature

    def get_measurement(self) -> float:
        """
        :param bool dew_point: if True add dew_point to return measurements
        """
        temperature = self.ds18.temperature
        temperature = round(temperature + self.offset_temperature,1)
        return temperature
