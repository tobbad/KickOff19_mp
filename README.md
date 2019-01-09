# KickOff19_mp
Files for Kick off 2019

Files unterhalb modules sollten vor dem Kompilieren von micropython nach /ports/esp8266/modules kopiert werden.

BL4752MQTT.py is ein kleines script das versucht von einem STM32 IOT device B-L475E-IOT01A23 die sensor daten zu lesen und sie auf dem MQTT_Broker zu publizieren. Da die STM Software nicht so stabil laeuft, werden die daten bei einem HTTP request der ins Timeout laeuft gefaked.

mqtT_mpws.py ist der Python code enthalten, der von den Teilnehmer im Handson entwickelt werden kann. Unter dieser [Micropythonseite](https://docs.micropython.org/en/latest/esp8266/quickref.html) ist die Referenz zum esp8266 MP zu finden. Das Github von Micropython ist [hier](https://github.com/micropython/micropython).

Der [verwendete MQTT server](https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/umqtt/simple.py) ist in der [Micropython libarary](https://github.com/micropython/micropython-lib) enthalten.

flash_ws.sh wird auch auf dem RasPi benoetigt um ein esp8266 zu programmieren. Ferner wird der esptools folder (Hash 9dfcb35 von [espressif/esptool](https://github.com/espressif/esptool.git) aus dem [esp-open-sdk repo](https://github.com/pfalcon/esp-open-sdk.git) auf dem RasPi beoetigt. 

Zum Aufsetzen von des RasPi als Acess point siehe [hier](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)

[Treiber](https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip) für den Serial Port des Huazzah!

Für einen einfachen Serial Port Zugriff empfehlen wir [Putty](https://the.earth.li/~sgtatham/putty/latest/w64/putty-64bit-0.70-installer.msi).