#include <PubSubClient.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include "cert.h"

// WiFi
const char *ssid = "sphone";
const char *password = "thegreatfilter";

// MQTT Broker
const char *mqtt_broker = "mfa20a52.ala.asia-southeast1.emqxsl.com";
const char *topic = "esp32/receiving";
const char *mqtt_username = "admin";
const char *mqtt_password = "admin";
const int mqtt_port = 8883;

WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(1000);
  setupWiFi();

  espClient.setCACert(ca_cert);
  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(callback);

  connectMQTT();
}

void callback(char *topic, byte *payload, unsigned int length) {
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  Serial.println("-----------------------");
}

void loop() {
  // put your main code here, to run repeatedly:

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected. Reconnecting...");
    setupWiFi();
  }

  if (!client.connected()) {
    Serial.println("MQTT disconnect. Reconnecting...");
    connectMQTT();
  }

  client.loop();

  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    if (data.length() > 0) {
      Serial.println("Publishing: " + data);
      client.publish(topic, data.c_str());
    }
  }
}

void setupWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(2000);
    Serial.print("Connecting to WiFi, current status: ");
    Serial.println(WiFi.status());
  }
  Serial.println("Connected to the WiFi network");
}

void connectMQTT() {
  while (!client.connected()) {
    String client_id = "esp32-client-";
    client_id += String(WiFi.macAddress());
    Serial.printf("The client %s connects to the public MQTT broker\n", client_id.c_str());
    if (client.connect(client_id.c_str(), mqtt_username, mqtt_password)) {
      Serial.println("Public EMQX MQTT broker connected");
    } else {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
}
