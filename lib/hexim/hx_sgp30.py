import os
import time
import json
import adafruit_sgp30

class SGP30:

    def __init__(self, i2c, debug: bool = False) -> None:

        # IAQ file
        self.iaq_file = "iaq_baseline.txt"

        # First save IAQ after 12 hours
        self.save_iaq_after = 43200

        # Actual UNIX timestamp
        self.now = time.time()

        self.debug = debug

        # Create library object on our I2C port
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

        # check if IAQ baseline data exist and process it
        self.__check_iaq_baseline()

    def get_measurment(self, temp: float = 0, humid: float = 0, comp: bool = False) -> list[int]:
        """
        :param float temp: Actual temperature in C
        :param float humid: Actual relative humidity in %
        :param bool comp: Compensate eCo2 and TVOC algorithm
        """
        # save IAQ baseline if posible
        self.__save_iaq_baseline()

        # get measurement
        eCO2, TVOC = self.sgp30.iaq_measure()

        if self.debug:
            print("eCO2: {0}, TVOC: {1}" . format(eCO2, TVOC))

        # Set the humidity in g/m3 for eCo2 and TVOC compensation algorithm.
        if comp:
            self.sgp30.set_iaq_relative_humidity(celsius=float(temp), relative_humidity=float(humid))

        return (eCO2, TVOC)

    def __save_iaq_baseline(self) -> None:
        """
        Save actual IAQ baseline to file with timestamp. After first run,
        values save after 12 hours. After 12 hours will be saved every hour.

        Desc:
        If no stored baseline is available after initializing the baseline algorithm,
        the sensor has to run for 12 hours until the baseline can be stored.
        This will ensure an optimal behavior for the next time it starts up.
        Reading out the baseline prior should be avoided unless a valid baseline
        is restored first. Once the baseline is properly initialized or restored,
        the current baseline value should be stored approximately once per hour.
        While the sensor is off, baseline values are valid for a maximum of seven days.

        More info:
        https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/arduino-code
        """
        actual_time = time.time()
        if (self.now + self.save_iaq_after) < actual_time:
            try:
                with open("/"+self.iaq_file, "w") as fp:
                    data = dict()
                    data["timestamp"] = actual_time
                    data["eCO2"] = self.sgp30.baseline_eCO2
                    data["TVOC"] = self.sgp30.baseline_TVOC
                    fp.write(json.dumps(data))
                    fp.flush()
                    fp.close()
            except OSError as e:
                print("Error_1: {0}". format(e))
                pass
            # update actual backup time
            self.now = actual_time
            # next time save eCO2 and TVOC every hour
            self.save_iaq_after = 3600

    def __check_iaq_baseline(self) -> None:
        """
        Check file with IAQ baseline values for first run. If file exist and
        values are valid, set iaq baseline. Values in this file are valid for one week.
        """
        if self.iaq_file in os.listdir("/"):
            try:
                with open("/"+self.iaq_file, "r") as fp:
                    data = json.loads(fp.readline())
                    # maximum old IAQ data is 1 week
                    if (time.time() - 604800) < data["timestamp"]:
                        self.sgp30.set_iaq_baseline(data["eCO2"], data["TVOC"])
                    fp.close()
            except RuntimeError as e:
                print("Error_2: {0}". format(e))
                pass
            except OSError as e:
                print("Warn_3: {0}". format(e))
                pass
