import time
import board
import microcontroller
from adafruit_onewire.bus import OneWireBus
from lib.hexim import hx_board_LED, hx_ds18b20, hx_mqtt, hx_wifi

# Board LED off by default
hx_board_LED.off()

# Connect wifi
hx_wifi.connect(debug=False)

# MQTT
mqtt = hx_mqtt.mqtt(subscriber=True, debug=False)

# Initialize one-wire bus on board pin GP17.
ow_bus = OneWireBus(board.GP17)

# DS18B20
ds18 = hx_ds18b20.DS18B20(ow_bus, offset_temperature = 0)

while True:
    try:
        # check if subscribes is enabled
        if mqtt.is_subscriber():
            mqtt.mqtt_client.loop()

        # Get data
        pub_data = dict({})
        pub_data["temperature"]= ds18.get_measurement()

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
