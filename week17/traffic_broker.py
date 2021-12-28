#! /usr/bin/python

import smbus2 as smbus 
from time import sleep
from random import randrange, random
import paho.mqtt.client as mqtt
import threading, os

#---------------------------------------------------------------
I2C_ADDR = 11
PORT = 1
I2C = smbus.SMBus(PORT)

# LED Pin Mapped
R1, Y1, G1 = 1, 2, 4
R2, Y2, G2 = 8, 16, 32

MAP = 55
LOOP = 66
FOREVER = 77

#---------------------------------------------------------------
# send LED-Control command to Arduino with parameters
# cmd : commands
# dat : additional parameters
def toArduino(cmd, dat=[]):
    global I2C
    bytes_msg = bytes(dat)
    print(f"{cmd}",end=" ")
    I2C.write_i2c_block_data(I2C_ADDR, cmd, bytes_msg)
    #sleep(0.1)
    
#---------------------------------------------------------------
TOPIC  = f"uproc2021f/traffic/{randrange(10,50)}"
BROKER = "broker.emqx.io"
PORT   = 1883
Client = None

#---------------------------------------------------------------
# MQTT-Connected callback function 
def on_connect(client, userdata, flags, rc):
    global TOPIC
    print(f"{TOPIC} is connected with result code {rc}.")

#---------------------------------------------------------------
# MQTT message retrieval callback function for the subscribed topics
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"TOPIC({topic}) : MSG({payload})")
    cmds = payload.split(',')
    #print(cmds)
    try:
        if cmds[0]=='EXIT':
            print('Bye')
            client.disconnect()
        elif cmds[0]=='LOOP':
            cmd = LOOP
            par = [int(c) for c in cmds[1:]]
            toArduino(cmd, par)
        elif cmds[0]=='FOREVER':
            cmd = FOREVER
            par = [int(c) for c in cmds[1:]]
            toArduino(cmd, par)
        elif cmds[0]=='MAP':
            cmd = MAP
            par = [int(cmds[1])]
            toArduino(cmd, par)
    except:
        print("Something wrong!")
            
#---------------------------------------------------------------
def connect_mqtt():
    global Client
    # Create MQTT client and connect to the broker    
    Client = mqtt.Client()
    Client.on_connect = on_connect
    Client.on_message = on_message
    # client.username_pw_set("user-name","password")
    Client.connect(BROKER, PORT, keepalive=60)
    # Clear the retained message send by Kittenblock
    Client.publish(topic=TOPIC, payload=None, retain=True)
    # Subscribe interested topic(s)
    Ｃlient.subscribe(TOPIC)

#---------------------------------------------------------------
# Main Loop
def main():
    global Client
    Client.loop_forever()

#---------------------------------------------------------------
if __name__ == "__main__":
    connect_mqtt()
    main()