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
    msg_str = msg.payload.decode().strip()
    msg_array = msg_str.split()
    long = float(msg_array[0])
    lat = float(msg_array[1])
    pm25 = float(msg_array[2])
    pm10 = float(msg_array[3])
    no2 = float(msg_array[4])
    co = float(msg_array[5])
    co2 = float(msg_array[6])
    ch4 = float(msg_array[7])
    voc = float(msg_array[8])
    o3 = float(msg_array[9])
    return [
        {"long" : long, "lat" : lat, "pollutant" : "PM25", "value" : pm25},
        {"long" : long, "lat" : lat, "pollutant" : "PM25", "value" : pm10},
        {"long" : long, "lat" : lat, "pollutant" : "NO2", "value" : no2},
        {"long" : long, "lat" : lat, "pollutant" : "CO", "value" : co},
        {"long" : long, "lat" : lat, "pollutant" : "CO2", "value" : co2},
        {"long" : long, "lat" : lat, "pollutant" : "VOC", "value" : voc},
        {"long" : long, "lat" : lat, "pollutant" : "CH4", "value" : ch4},
        {"long" : long, "lat" : lat, "pollutant" : "O3", "value" : o3},
    ]

def start_mqtt():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()