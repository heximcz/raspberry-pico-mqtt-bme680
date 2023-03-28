"""
Pico W board LED driver
"""
import board
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

def off() -> None:
    # turn LED off
    led.value = False
    