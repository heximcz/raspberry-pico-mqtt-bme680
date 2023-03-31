import math
import busio
from adafruit_bme280 import basic as adafruit_bme280


class BME280:

    def __init__(self, i2c: busio.I2C, lin_comp: dict, offset_pressure: float = 0, offset_humidity: float = 0, debug: bool = False) -> None:
        """
        :param float offset_temperature
        :param float offset_pressure
        :param float offset_humidity
        """
        #self.i2c = i2c 
        #i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
        self.debug = debug
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 118)
        self.lin_comp = lin_comp
        self.offset_pressure = offset_pressure
        self.offset_humidity = offset_humidity

    def get_measurement(self, dew_point: bool = False) -> list[int]:
        """
        :param bool dew_point: if True add dew_point to return measurements
        """
        raw_temp = self.bme280.temperature
        temperature = round(float(raw_temp + self._lin_comp(raw_temp)),1)
        humidity = round(self.bme280.relative_humidity + self.offset_humidity)
        pressure = round(self.bme280.pressure + self.offset_pressure)

        if self.debug:
            import microcontroller
            print("RAW T: {0}, CPU T: {1}" . format(raw_temp, microcontroller.cpu.temperature))
            print("T: {0}, RH: {1}, hPa: {2}, Dew: {3}". format(temperature, humidity, pressure, self._dew_point(temperature, humidity)))

        if dew_point:
            return (temperature, humidity, pressure, self._dew_point(temperature, humidity))
        return (temperature, humidity, pressure)

    def _dew_point(self, temperature: float, humidity: float) -> float:
        # https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
        b = 17.62
        c = 243.12
        gamma = (b * temperature /(c + temperature)) + math.log(humidity / 100.0)
        return round((c * gamma) / (b - gamma),1)

    def _lin_comp(self, temp: float) -> float:
        """
        Linear temperature compensation
        :param float temp: actual RAW temperature
        """
        # x1 = self.lin_comp["raw_temp_low"]
        # y1 = self.lin_comp["offset_temp_low"]
        # x2 = self.lin_comp["raw_temp_high"]
        # y2 = self.lin_comp["offset_temp_high"]
        # y = y1 + (y2 - y1) / (x2 - x1) * (temp - x1)
        return self.lin_comp["offset_temp_low"] + (self.lin_comp["offset_temp_high"] - self.lin_comp["offset_temp_low"]) / \
            (self.lin_comp["raw_temp_high"] - self.lin_comp["raw_temp_low"]) * (temp - self.lin_comp["raw_temp_low"])
