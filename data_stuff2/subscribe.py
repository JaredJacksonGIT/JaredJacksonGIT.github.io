from paho.mqtt import client as mqtt
import random
import queue

broker = "mfa20a52.ala.asia-southeast1.emqxsl.com"
port = 8883
topic = "esp32/receiving"
client_id = f"heatmap-{random.randint(0, 1000)}" 

username = password = "admin"

message_queue = queue.Queue()

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv311)
    client.username_pw_set(username, password)
    client.on_connect = on_connect

    client.tls_set(ca_certs="./emqxsl-ca.crt")

    client.connect(broker, port)

    # Start the loop
    return client

def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        msg_dict = create_dict(msg)
        message_queue.put(msg_dict)

    client.subscribe(topic)
    client.on_message = on_message

def create_dict(msg):
    msg_str = msg.payload.decode()
    msg_array = msg_str.split()
    long = msg_array[0]
    lat = msg_array[1]
    return [
        {"long" : float(long), "lat" : float(lat), "pollutant" : "CO", "value" : float(msg_array[2])},
        {"long" : float(long), "lat" : float(lat), "pollutant" : "CO2", "value" : float(msg_array[3])},
        {"long" : float(long), "lat" : float(lat), "pollutant" : "CH4", "value" : float(msg_array[4])},
        {"long" : float(long), "lat" : float(lat), "pollutant" : "VOC", "value" : float(msg_array[5])}
    ]

def start_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()