# KickOff19_mp
Files for Kick off 2019

Files unterhalb modules sollten vor dem Kompilieren von micropython nach /ports/esp8266/modules kopiert werden.

BL4752MQTT.py is ein kleines script das versucht von einem STM32 IOT device B-L475E-IOT01A23 die sensor daten zu lesen und sie auf dem MQTT_Broker zu publizieren. Da die STM Software nicht so stabil laeuft, werden die daten bei einem HTTP request der ins Timeout laeuft gefaked.

mqtT_mpws.py ist der Python code enthalten, der von den Teilnehmer im Handson entwickelt werden kann.
