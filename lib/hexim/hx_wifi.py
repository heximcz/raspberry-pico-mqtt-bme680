import ipaddress
import os
import adafruit_ntp
import microcontroller
import rtc
import socketpool
import wifi

def connect(debug: bool = False) -> None:
    if debug:
        print("Connecting to WiFi")

    # Connect to WiFi
    try:
        # DHCP is disabled, set static IP
        if int(os.getenv('WIFI_DHCP')) == 0:
            wifi.radio.stop_dhcp()
            # Static IP address
            ipv4 =  ipaddress.IPv4Address(os.getenv('WIFI_IP'))
            netmask =  ipaddress.IPv4Address(os.getenv('WIFI_NETMASK'))
            gateway =  ipaddress.IPv4Address(os.getenv('WIFI_GATEWAY'))
            ipv4_dns = ipaddress.IPv4Address(os.getenv('WIFI_IPv4_DNS'))
            wifi.radio.set_ipv4_address(ipv4=ipv4, netmask=netmask, gateway=gateway, ipv4_dns=ipv4_dns)
        # Connect
        wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))

        if debug:
            print("Connected!")
            #  Print MAC address to REPL
            print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
            #  Print IP address to REPL
            print("My IP address is", wifi.radio.ipv4_address)
            #  Pings Google
            ipv4 = ipaddress.ip_address("8.8.8.8")
            print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

    except ConnectionError as e:
        print("Error WiFi connect: {0}" . format(e))
        microcontroller.reset()

    # Synchronize time over NTP
    try:
        time_pool = socketpool.SocketPool(wifi.radio)
        ntp = adafruit_ntp.NTP(time_pool, server=os.getenv('NTP_SERVER'), tz_offset=os.getenv('NTP_TZ_OFFSET'), socket_timeout=15)
        rtc.RTC().datetime = ntp.datetime
        if debug:
            print("The time has been synchronized.")
    except:
        print("Error: Cannot synchronize time!")
        microcontroller.reset()
