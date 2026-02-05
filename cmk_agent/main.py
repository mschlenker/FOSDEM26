#!/usr/bin/env python3
# encoding: utf-8

import esp32
import time
import network
import socket
import machine
from wifisecrets import wifisecrets

TIMEOUT = None
PORT = 6556

# Sensor readings for moisture warn and moisture crit
MC = 2500
MW = 2000

# Initialize the board LED to show activity
led = machine.Pin(8, machine.Pin.OUT)
led.on()
time.sleep(10.0)
led.off()

adc_pin = machine.Pin(3, machine.Pin.IN)
adc = machine.ADC(adc_pin)
adc.atten(machine.ADC.ATTN_11DB)

# Initialize the WiFi interface in station mode
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan() # Scan for available access points
print("Trying to connect to: " + wifisecrets["ssid"])
sta_if.connect(wifisecrets["ssid"], wifisecrets["wpapsk"])
sta_if.isconnected()
print("My IP is " + sta_if.ifconfig()[0])

# Start a listening server on the Checkmk agent port:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', PORT))
s.listen(2)

# Prepare a minimal static Checkmk agent output:
output = """<<<check_mk_agent>>>
AgentOS: MicroPython
<<<soilmoisture>>>
"""

print(output)

while True:
    # On connect, print the IP address:
    conn, addr = s.accept()
    led.on()
    val = adc.read()
    print("Request from " + str(addr[0]) + ", port " + str(addr[1]))
    print("Read: " + str(val))
    conn.settimeout(TIMEOUT)
    msg = output + str(val) + "\n<<<local>>>\n"
    if val > MC:
        msg = msg + "2 \"Soil moisture ESP32\" smval=" + str(val) + " Uh, I am dying\n"
    elif val > MW:
        msg = msg + "1 \"Soil moisture ESP32\" smval=" + str(val) + " Uh, Please give me water\n"
    else:
        msg = msg + "0 \"Soil moisture ESP32\" smval=" + str(val) + " Everything is fine\n"
    conn.send(msg)
    print("Served request, closing...")
    conn.close()
    led.off()
