import time
import board
import busio
import microcontroller
from lib.hexim import hx_board_LED, hx_mqtt, hx_sht4x, hx_wifi

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

# SHT41 I2C Sensor
sht4x = hx_sht4x.SHT4x(i2c, offset_temperature = -3.8, offset_humidity = 2, debug=False)

while True:
    try:
        # check if subscribes is enabled
        if mqtt.is_subscriber():
            mqtt.mqtt_client.loop()

        # Get data
        pub_data = dict({})
        pub_data["temperature"], \
            pub_data["humidity"], \
            pub_data["dewpoint"] = sht4x.get_measurement(dew_point=True)

        # pub values from sensor
        mqtt.pub(msg=pub_data)

        # wait one minute
        time.sleep(60)
    except KeyboardInterrupt as e:
        print("Keyboard exit!")
        import sys
        sys.exit()
    except:
        microcontroller.reset()
