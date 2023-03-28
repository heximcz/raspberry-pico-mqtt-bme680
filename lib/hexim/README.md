## Hexim modules

## CircuitPython
- [Download latest UF2](https://circuitpython.org/board/raspberry_pi_pico_w/)

## Compile module to .mpy

- Download [mpy-cross compiler](https://adafruit-circuit-python.s3.amazonaws.com/index.html?prefix=bin/mpy-cross/)
- Example: ```./mpy-cross.static-amd64-linux-8.0.3 hx_<xxx>.py```


### Circup

- first install circup: ```pip3 install circup```

### Instal for:

- I2C
```
circup install adafruit_bus_device
```
- NTP
```
circup install adafruit_ntp
```
- MQTT
```
circup install adafruit_minimqtt
```
- SGP30
```
circup install adafruit_sgp30
```
- SHT4x
```
circup install adafruit_sht4x
```
- BME280
```
circup install adafruit_bme280
```
- BME680
```
circup install adafruit_bme680
```
- SSD1306
```
circup install adafruit_bitmap_font
circup install adafruit_display_text
circup install adafruit_displayio_ssd1306
```
- DS18B20
```
circup install adafruit_ds18x20
```
