#include <ArduinoMqttClient.h>
#include <WiFiNINA.h>

// Set-up output pin, A means it's an analog pin
#define CAR A1

// Wifi variables
char ssid[] = "CuriousInc-Corp"; 
char pass[] = "PMEF4pW6x39G"; 

WiFiClient wifiClient;

// MQTT variables
MqttClient mqttClient(wifiClient);
const char broker[] = "192.168.133.75";//"e00c2bec62a44970bf0a6815c1326900.s2.eu.hivemq.cloud";    // When run on a private network, this should be the local IP address
int        port     = 30000 ;   // Don't forget to open this port via the firewall
const char topic[]  = "topic1";   // The MQTT topic

// Global variable to keep check if the vehicle should drive
bool should_drive = false;

void setup() {
  /*
  Initialize serial and wait for port to open
  Serial prints can be read through the serial monitor in the Arduino IDE
  */
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // Attempt to connect to Wifi network:
  Serial.print("Attempting to connect to WPA SSID: ");
  Serial.println(ssid);
  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    // failed, retry
    Serial.println(status);
    delay(5000);
  }

  Serial.println("You're connected to the network");
  Serial.println();

  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);
  mqttClient.setUsernamePassword("bitinc", "Admin2023!");

  // Attempt to connect to the MQTT client
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());
    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

  // Set the message receive callback
  mqttClient.onMessage(onMqttMessage);

  Serial.print("Subscribing to topic: ");
  Serial.println(topic);
  Serial.println();

  // Subscribe to a topic
  mqttClient.subscribe(topic);

  Serial.print("Subscribed to topic: ");
  Serial.println(topic);

  Serial.println();

  // Set output pin
  pinMode(CAR, OUTPUT);
}

void loop() {
  /*
  Call poll() regularly to allow the library to receive MQTT messages and
  send MQTT keep alive which avoids being disconnected by the broker
  */
  mqttClient.poll();

  // If should_drive changed, this will be outputted to the car controller
  if(should_drive) {
    digitalWrite(CAR, HIGH);
  } else {
    digitalWrite(CAR, LOW);
  }
}

void onMqttMessage(int messageSize) {
  // Read from the MQTT stream untill there are no more bites
  String msg_str = "";
  while (mqttClient.available()) {
    char msg = (char)mqttClient.read();
    msg_str += msg;
  }

  // Check if the msg send is a start or stop signal and change the should_drive accordingly
  if(msg_str.equals(String("start"))){ 
    should_drive = true;
    Serial.println("START");
  } else if (msg_str.equals(String("stop"))) {
    should_drive = false;
    Serial.println("STOP");
  }
}




