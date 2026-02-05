#!/usr/bin/env python3
# encoding: utf-8

import esp32
import time
import network
import socket
import machine
import usyslog
from wifisecrets import wifisecrets

# Initialize the board LED to show activity
led = machine.Pin(15, machine.Pin.OUT)
led.on()
time.sleep(10.0)
led.off()

# Initialize the WiFi interface in station mode
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan() # Scan for available access points
print("Trying to connect to: " + wifisecrets["ssid"])
sta_if.connect(wifisecrets["ssid"], wifisecrets["wpapsk"])
sta_if.isconnected()
print("My IP is " + sta_if.ifconfig()[0])
time.sleep(5.0)
print("My IP is " + sta_if.ifconfig()[0])

SYSLOG_SERVER_IP = '10.76.23.249'

s = usyslog.UDPClient(ip=SYSLOG_SERVER_IP)
pin = machine.Pin(39, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    pstate = pin.value()
    if pstate > 0:
        led.on()
        print('Door is open!')
        s.warning('Door is open!')
        time.sleep(10)
    else:
        led.off()
        print('Door is closed.')
        s.notice('Door is closed.')
        time.sleep(10)
