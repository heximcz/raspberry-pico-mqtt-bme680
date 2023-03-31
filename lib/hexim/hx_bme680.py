import math
import busio
import adafruit_bme680

class BME680:

    def __init__(self, i2c: busio.I2C, lin_comp: dict, bme680_address: int = 119, offset_pressure: float = 0, offset_humidity: float = 0, debug: bool = False) -> None:
        """
        :param dict lin_comp: data for linear temperature compensation see: self._lin_comp()
        :param float offset_pressure
        :param float offset_humidity
        """
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address = bme680_address)
        self.lin_comp = lin_comp
        self.offset_pressure = offset_pressure
        self.offset_humidity = offset_humidity
        self.debug = debug

    def get_measurement(self, dew_point: bool = False) -> list[int]:
        """
        :param bool dew_point: if True add dew_point to return measurements
        """
        pressure = self.bme680.pressure + self.offset_pressure
        self.bme680.sea_level_pressure = pressure

        raw_temp = self.bme680.temperature
        temperature = round(float(raw_temp + self._lin_comp(raw_temp)),1)
        humidity = round(self.bme680.relative_humidity + self.offset_humidity)
        pressure = round(self.bme680.pressure + self.offset_pressure)
        gas = self.bme680.gas
        altitude = round(self.bme680.altitude)

        if self.debug:
            import microcontroller
            print("RAW T: {0}, CPU T: {1}" . format(raw_temp, microcontroller.cpu.temperature))
            print("T: {0}, RH: {1}, hPa: {2}, Gas: {3}, Alt: {4}, Dew: {5}". format(temperature, humidity, pressure, gas, altitude, self._dew_point(temperature, humidity)))

        if dew_point:
            return (temperature, humidity, pressure, gas, altitude, self._dew_point(temperature, humidity))
        return (temperature, humidity, pressure, gas, altitude)

    def _dew_point(self, temperature, humidity):
        """
        See: https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test
        """
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
