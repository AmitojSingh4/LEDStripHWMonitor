import plasma
from plasma import plasma_stick
import machine

import time
import json

import network
import requests
import socket

import wifiDetails # .py file with wifi details

NUM_LEDS = 50

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB)

led_strip.start()

# Onboard led
led = machine.Pin('LED', machine.Pin.OUT)

# URL of webserver to pull data from
URL = 'http://localhost:3000/'

# Connects to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifiDetails.SSID,wifiDetails.PSK)

# Onboard led turns on if connected to wifi
if wlan.status() == 3:
   led.toggle()
#print(wlan.ifconfig()[0]) # Prints picos ip

def obtainData():
    sock = socket.socket()
    sock.connect(('192.168.0.38', 3000)) # Creates a socket connection
    resp_data = b'' # Clears previous data
    sock.send(b"GET / HTTP/1.1\r\nHost: 192.168.0.38:3000\r\n\r\n")
    while (resp_data := sock.recv(1024) + sock.recv(1024)) == b'':
        time.sleep(0.1) # Waits for data to arive to prevent further lines from breaking
    resp_data = str(resp_data)
    body_index = resp_data.find('{')
    data = json.loads(resp_data[body_index:-2]) # Converts data from Json to a dictionary
    sock.close()
    return(data)

def hexToRGB(hex_value):
    R = int('0x'+hex_value[0:2])
    G = int('0x'+hex_value[2:4])
    B = int('0x'+hex_value[4:6])
    return R, G, B

def activateLED(section):
    no_LED = round(float(values['ValueRaw'+str(section)]['value'])/(max_values[str(section)]/10) + 1) # Calculates number of leds that need to be turned on
    for i in range(1,no_LED): # Turns leds on
        colour = hexToRGB(values['Color'+str(section)]['value'])
        led_strip.set_rgb(i+((section)*13), colour[0], colour[1], colour[2])
    if (no_LED != 11): # Turns unneeded leds off
        for i in range(no_LED,11):
            led_strip.set_rgb(i+((section)*13), 0, 0, 0)

max_values = { # Maximum values of your hardware must be entered here, example system r3 3100, rtx 4060
  "0": 95, # CPU_Temp 95
  "1": 65, # CPU_Power 65
  "2": 85, # GPU_Temp 85
  "3": 115 # GPU_Power 115
}

while(True): # Turns on and refreshes all leds forever
    data = obtainData()
    values = data["HKCU\\\\SOFTWARE\\\\HWiNFO64\\\\VSB"]["values"]
    activateLED(0)
    activateLED(1)
    activateLED(2)
    activateLED(3)
    time.sleep(0.1)

