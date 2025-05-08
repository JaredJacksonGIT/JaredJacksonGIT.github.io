from paho.mqtt import client as mqtt
import random

broker = "mfa20a52.ala.asia-southeast1.emqxsl.com"
port = 8883
topic = "esp32/sensor_data"
client_id = f"heatmap-{random.randint(0, 1000)}" 

username = password = "admin"

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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()