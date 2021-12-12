import paho.mqtt.client as mqtt
import time, sys

TOPIC  = []
BROKER = "broker.hivemq.com"
PORT   = 1883
Client = None

# MQTT-Connected callback function 
def on_connect(client, userdata, flags, rc):
    global TOPIC
    print("Connected with result code "+str(rc))

# MQTT message retrieval callback function for the subscribed topics
def on_message(client, userdata, msg):
    global TOPIC
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    if payload=='': return
    print(f"TOPIC({topic}) : MSG({payload})")
    if payload=='EXIT':
        client.disconnect()

# Create MQTT client and connect to the broker    
def connect_broker():
    global Client
    Client = mqtt.Client()
    Client.on_connect = on_connect
    Client.on_message = on_message
    Client.connect(BROKER, PORT, keepalive=60)
    # Clear the retained message
    for t in TOPIC:
        Client.publish(topic=t, payload=None, retain=True)

# Subscribe interested topic(s)
def sub_topics():
    global Client
    for t in TOPIC:
        print(f"Subscribe('{t}')")
        Ｃlient.subscribe(t)

# Main Loop
# ------------------------------------------
if __name__=="__main__":
    if len(sys.argv)>1:
        for st in sys.argv[1:]:
            TOPIC.append("P203-{0}".format(st))
    else:
        TOPIC.append("P203-100")
    connect_broker()
    sub_topics() 
    Client.loop_forever()
