import math
from adafruit_bme280 import basic as adafruit_bme280

class BME280:

    def __init__(self, i2c, offset_temperature = -3.65, offset_pressure = 27.6, offset_humidity = 11):
        """
        :param float offset_temperature
        :param float offset_pressure
        :param float offset_humidity
        """
        #self.i2c = i2c 
        #i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 118)
        self.offset_temperature = offset_temperature
        self.offset_pressure = offset_pressure
        self.offset_humidity = offset_humidity

    def get_measurement(self, dew_point: bool = False) -> list[int]:
        """
        :param bool dew_point: if True add dew_point to return measurements
        """
        temperature = round(float(self.bme280.temperature + self.offset_temperature),1)
        humidity = round(self.bme280.relative_humidity + self.offset_humidity)
        pressure = round(self.bme280.pressure + self.offset_pressure)
        if dew_point:
            return (temperature, humidity, pressure, self._dew_point(temperature, humidity))
        return (temperature, humidity, pressure)

    def _dew_point(self, temperature, humidity):
        # https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
        b = 17.62
        c = 243.12
        gamma = (b * temperature /(c + temperature)) + math.log(humidity / 100.0)
        return round((c * gamma) / (b - gamma),1)
