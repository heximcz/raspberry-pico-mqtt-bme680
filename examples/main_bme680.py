import time
import board
import busio
import microcontroller
from lib.hexim import hx_bme680, hx_board_LED, hx_mqtt, hx_wifi

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
bme680 = hx_bme680.BME680(i2c, lin_comp, bme680_address=119, offset_pressure=26, offset_humidity=0, debug=False)

while True:
    try:
        # check if subscribes is enabled
        if mqtt.is_subscriber():
            mqtt.mqtt_client.loop()

        # BME680
        pub_data = dict({})
        pub_data["temperature"], \
            pub_data["humidity"], \
            pub_data["pressure"], \
            pub_data["gas"], \
            pub_data["altitude"], \
            pub_data["dewpoint"] = bme680.get_measurement(dew_point=True)

        # pub values from sensor
        mqtt.pub(pub_data)

        # wait one minute
        time.sleep(60)
    except KeyboardInterrupt as e:
        print("Keyboard exit!")
        import sys
        sys.exit()
    except:
        microcontroller.reset()
