import time
import board
import busio
import microcontroller
from lib.hexim import hx_bme280, hx_board_LED, hx_mqtt, hx_wifi

# Board LED off by default
hx_board_LED.off()

# Connect wifi
hx_wifi.connect(debug=False)

# MQTT
mqtt = hx_mqtt.mqtt(subscriber=True, debug=False)

# I2C
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

# Scan I2C
#from hexim import hx_i2c_scan
#hx_i2c_scan.scan(i2c)

# BME280 I2C Sensor
bme280 = hx_bme280.BME280(i2c, offset_temperature = -3.65, offset_pressure = 27.6, offset_humidity = 11)

while True:
    try:
        # check if subscribes is enabled
        if mqtt.is_subscriber():
            mqtt.mqtt_client.loop()

        # BME280
        pub_data = dict({})
        pub_data["temperature"], \
            pub_data["humidity"], \
            pub_data["pressure"], \
            pub_data["dewpoint"] = bme280.get_measurement(dew_point=True)

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
