from machine import Pin, PWM
#
# Topic 1:
#
# Led control
#
class Led:
    
    PIN=0

    def __init__(self):
        self._pwm=PWM(Pin(Led.PIN))
        self._pwm.freq(1000)
        self.off()        
        
    def on(self, value=1.0):
        value = 1.0 if value>1.0 else value
        value = 0.0 if value<0.0 else value
        value = int(1023*(1-value))
        self._pwm.duty(value)
    
    def off(self):
        self._pwm.duty(1023)

#
# Topic 2 
# MQTT subscribe
#
from config import * # Get SSID and PASSWORD and MQTT broker ip
import network
from mqtt import MQTTClient
import time


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


mqttc = None
# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

def mqtt_listen(server=MQTT_BROKER):
    global mqttc
    mqttc = MQTTClient("umqtt_client", server)
    mqttc.set_callback(sub_cb)
    mqttc.connect()
    mqttc.subscribe(b"sensor/#")
    while True:
        if True:
            # Blocking wait for message
            mqttc.wait_msg()
        else:
            # Non-blocking wait for message
            mqttc.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    mqttc.disconnect()

