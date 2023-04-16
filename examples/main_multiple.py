import board
import busio
import displayio
import microcontroller
from lib.hexim import (hx_bme280, hx_board_LED, hx_mqtt, hx_sgp30, hx_ssd1306, hx_wifi)

# Reset display
displayio.release_displays()

# Board LED off by default
hx_board_LED.off()

# Connect wifi
hx_wifi.connect(debug=False)

# MQTT
mqtt = hx_mqtt.mqtt(subscriber=True, is_ssl=False, debug=False)

# I2C
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# Scan I2C
#from hexim import hx_i2c_scan
#hx_i2c_scan.scan(i2c)

## Data for linear temperature compensation of parasitic heating
## This is need for compensation if sensor is in the any box with raspberry pico
## For ignore this function set both "offset_temp_<low/high>" to 0
lin_comp = {
    # low temperature
    "raw_temp_low": 12.6,
    # temperature difference compared to a calibrated thermometer
    "offset_temp_low": -1.6,
    # high temperature
    "raw_temp_high": 25,
    # temperature difference compared to a calibrated thermometer
    "offset_temp_high": -3.6
}

# BME280 I2C Sensor
bme280 = hx_bme280.BME280(i2c, lin_comp, offset_pressure = 0, offset_humidity = 0, debug=True)

# OLED display
oled = hx_ssd1306.SSD1306(i2c)

# SGP30 eCO2/TVOC !!! for this module use boot.py !!!
sgp30 = hx_sgp30.SGP30(i2c, debug=True)

while True:
    try:
        # check if subscribes is enabled
        if mqtt.is_subscriber():
            mqtt.mqtt_client.loop()

        # Get data
        pub_data = dict({})

        # BME280
        pub_data["temperature"], \
            pub_data["humidity"], \
            pub_data["pressure"], \
            pub_data["dewpoint"] = bme280.get_measurement(dew_point=True)

        # SGP30 with compensation
        pub_data["eCO2"], \
            pub_data["TVOC"] = sgp30.get_measurment(temp=pub_data["temperature"], humid=pub_data["humidity"], comp=True)

        # MQTT PUB
        mqtt.pub(msg=pub_data)

        # OLED 1 minute
        oled.showText(temp=pub_data["temperature"], humid=pub_data["humidity"])
    except KeyboardInterrupt as e:
        print("Keyboard exit!")
        import sys
        sys.exit()
    except:
        microcontroller.reset()
