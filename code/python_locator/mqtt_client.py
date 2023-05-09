from paho.mqtt import client as mqtt_client
import random

class MqttClient():
    def __init__(self, topic, broker='localhost'):
        self.broker = broker
        self.port = 30000
        self.topic = topic 
        self.client_id = f'pozyx-mqtt-{random.randint(0, 1000)}'
        self.client = None

        self.is_connected = False

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
                self.is_connected = True
            else:
                print("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        self.client = mqtt_client.Client(self.client_id)
        # If you want a secure connection add -> client.username_pw_set(self.username, self.password)
        self.client.on_connect = on_connect

        self.client.username_pw_set("bitinc", "Admin2023!")
        self.client.connect(self.broker, self.port)
        #self.client.connect("e00c2bec62a44970bf0a6815c1326900.s2.eu.hivemq.cloud", 30000)

    # Publish a message to the topic
    def publish(self, msg):
        result = self.client.publish(self.topic, msg)
        print(result)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{self.topic}`")
            pass
        else:
            print(f"Failed to send message to topic {self.topic}")

