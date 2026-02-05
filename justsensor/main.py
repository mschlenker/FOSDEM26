#!/usr/bin/env python3
# encoding: utf-8

import esp32
import time
# import network
# import socket
import machine

# Initialize the board LED to show activity
led = machine.Pin(8, machine.Pin.OUT)
# led.on()
# time.sleep(1.0)
# led.off()

adc_pin = machine.Pin(3, machine.Pin.IN)
adc = machine.ADC(adc_pin)
adc.atten(machine.ADC.ATTN_11DB)

while True:
    led.on()
    val = adc.read()
    print("Read: " + str(val))
    led.off()
    time.sleep(2.0)
