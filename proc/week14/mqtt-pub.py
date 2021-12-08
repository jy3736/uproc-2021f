import paho.mqtt.client as mqtt
import time, sys

GROUP  = 100
TOPIC  = f"P203-{GROUP}"
BROKER = "broker.hivemq.com"
PORT   = 1883
Client = None

# MQTT-Connected call-back function 
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

# Create MQTT client and connect to the broker
def connect_broker():
    global Client, TOPIC, GROUP
    TOPIC  = f"P203-{GROUP}"
    Client = mqtt.Client()
    Client.on_connect = on_connect
    Client.connect(BROKER, PORT, keepalive=60)
    # Clear the retained message send by Kittenblock
    Client.publish(topic=TOPIC, payload=None, retain=True)

# Send test commands with TOPIC to the broker
def pub_cmds(cmds):
    global Client, TOPIC
    for cmd in cmds:
        Client.publish(topic=TOPIC, payload=cmd, retain=False)
        print(f"send '{cmd}' to '{TOPIC}'")
        time.sleep(1)

# Main Loop
# ------------------------------------------
if __name__=="__main__":
    cmds = ['R1','R0','YB/300/500','R2G','G2R']
    if len(sys.argv)>=2:
        GROUP = sys.argv[1]
        if len(sys.argv)>2:
            cmds = sys.argv[2:]
    cmds.append('EXIT')
    connect_broker()
    pub_cmds(cmds)