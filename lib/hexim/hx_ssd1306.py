import time
import busio
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
import adafruit_displayio_ssd1306

class SSD1306:

    def __init__(self, i2c: busio.I2C) -> None:

        displayio.release_displays()

        ssd1306_i2c_addr = 60
        display_width = 128
        display_height = 64
        NUM_OF_COLOR = 2

        display_bus = displayio.I2CDisplay(i2c, device_address=ssd1306_i2c_addr)
        display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=display_width, height=display_height, brightness=0)

        group = displayio.Group()

        bitmap = displayio.Bitmap(display_width, display_height, NUM_OF_COLOR)
        bitmap_palette = displayio.Palette(NUM_OF_COLOR)
        bitmap_palette[0] = 0x000000
        bitmap_palette[1] = 0xFFFFFF

        tileGrid = displayio.TileGrid(bitmap, pixel_shader=bitmap_palette, x=0, y=0)
        group.append(tileGrid)

        # Draw a label
        text_group = displayio.Group()

        font = bitmap_font.load_font("/lib/BigShouldersDisplay-Thin-50.bdf")

        self.text_temp = label.Label(font, text="", color=0xFFFFFF, x=20, y=display_height // 2 - 1)
        self.text_humid = label.Label(font, text="", color=0xFFFFFF, x=20, y=display_height // 2 - 1)

        text_group.append(self.text_temp)
        text_group.append(self.text_humid)
        group.append(text_group)

        display.show(group)

    def showText(self, temp: float, humid: float) -> None:
        """
        One minute to end show params
        :param Any temp: Temperature - showing 40 second
        :param Any humid: Relative Humidity - showing 20 secon
        """
        
        self.text_humid.text = ""

        self.text_temp.text = "{0} °C" . format(temp)
        time.sleep(40)
        self.text_temp.text = ""

        self.text_humid.text = "{0} %rh" . format(humid)
        time.sleep(20)
