import busio
import math
import adafruit_sht4x

class SHT4x:

    def __init__(self, i2c: busio.I2C, offset_temperature: float = 0, offset_humidity: float = 0, debug: bool = False) -> None:
        """
        :param float offset_temperature
        :param float offset_humidity
        """

        # I2C
        self.sht4x = adafruit_sht4x.SHT4x(i2c)

        # Mode
        # Possible modes:
        # NOHEAT_HIGHPRECISION, NOHEAT_MEDPRECISION, NOHEAT_LOWPRECISION,
        # HIGHHEAT_1S, HIGHHEAT_100MS, MEDHEAT_1S, MEDHEAT_100MS, LOWHEAT_1S, LOWHEAT_100MS

        #self.sht4x.mode = adafruit_sht4x.Mode.LOWHEAT_100MS
        self.sht4x.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

        if debug:
            print("Found SHT4x with serial number", hex(self.sht4x.serial_number))
            print("SHT41 - current mode is: ", adafruit_sht4x.Mode.string[self.sht4x.mode])

        self.offset_temperature = offset_temperature
        self.offset_humidity = offset_humidity

    def get_measurement(self, dew_point: bool = False) -> list[int]:
        """
        :param bool dew_point: if True add dew_point to return measurements
        """
        temperature, relative_humidity = self.sht4x.measurements
        temperature = round(temperature + self.offset_temperature,1)
        humidity = round(relative_humidity + self.offset_humidity)
        if dew_point:
            return (temperature, humidity, self._dew_point(temperature, humidity))
        return (temperature, humidity)

    def _dew_point(self, temperature: float, humidity: float) -> float:
        # https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
        b = 17.62
        c = 243.12
        gamma = (b * temperature /(c + temperature)) + math.log(humidity / 100.0)
        return round((c * gamma) / (b - gamma),1)

