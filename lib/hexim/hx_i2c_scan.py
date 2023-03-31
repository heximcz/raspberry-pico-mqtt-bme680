"""
Scan I2C a return address in decimal
Scanning on: scl=board.GP21, sda=board.GP20
"""
import sys
import busio

def scan(i2c: busio.I2C) -> None:
    while not i2c.try_lock():
        pass
    print("I2C Scan:")
    devices = i2c.scan()

    x=0
    print("-----------------")
    for i in range(0, len(devices)):
        print("{0}: dec={1} hex={2:x}" . format(x, devices[i], devices[i]))
        x = x+1

    i2c.deinit()
    print("-----------------")
    print()
    print("I2C ID`s printed. The script will now exit.")
    sys.exit()
