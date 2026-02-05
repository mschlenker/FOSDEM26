#!/usr/bin/env python3
# encoding: utf-8

import esp32
import time
import network
import socket
import random
import machine
from wifisecrets import wifisecrets

# A small library providing a subset of the official Prometheus Python lib:
from prometheus_express import start_http_server, CollectorRegistry, Counter, Gauge, Router

TIMEOUT = None
PORT = 8080

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

registry = CollectorRegistry(namespace='prom_express')
metric_g = Gauge('temp_gauge',
    'temperature from various sensors',
    labels=['location', 'sensor'],
    registry=registry)

router = Router()
router.register('GET', '/metrics', registry.handler)
server = False

while True:
    while not server:
        server = start_http_server(PORT, address=sta_if.ifconfig()[0], depth=8)
    led.on()
    time.sleep(0.02)
    led.off()
    metric_g.labels('rack42', 'esp32_on_die').set(esp32.mcu_temperature())
    try:
        server.accept(router)
        print("Successfully served request")
    except OSError as err:
        print('Error accepting request: {}'.format(err))
    except ValueError as err:
        print('Error parsing request: {}'.format(err))
