# DigitalTwinDemo

## High-level overview


Figure 7: An architecture model of the demonstration.
TODO: Insert image here

19.2. Arduino sketches
wifi_controller.ino
This script is responsible for establishing a WiFi connection and subscribing to an MQTT topic. It sends a digital signal to an output pin when a start or stop signal is received via the MQTT topic.
Key components of the script:
Includes necessary libraries (ArduinoMqttClient.h and WiFiNINA.h)
Defines constants and global variables for WiFi and MQTT configurations, such as the SSID, password, broker IP, port, and topic
Initialises the serial communication, WiFi connection, and MQTT client in the setup() function
Subscribes to the specified MQTT topic and sets the onMqttMessage callback function for received messages
In the loop() function, the script polls for MQTT messages and sets the output pin according to the should_drive variable
The onMqttMessage() function reads incoming messages and updates the should_drive variable based on received "start" or "stop" commands
car_controller.ino
This script controls a line-following robot. It reads input from two IR sensors and stops the motor when the IR sensor goes over the line. The script also checks the input from the WiFi board to determine if the robot is allowed to drive.
Key components of the script:
Includes the necessary library (AFMotor.h) for motor control
Initialises the right and left motors
Defines constants for the left and right IR sensor pins and the WiFi board input pin
Sets up input pins for the IR sensors and WiFi board output sensor in the setup() function
Initialises the motors and sets their speed
In the loop() function, the script reads the input from the WiFi board to determine if the robot can drive
If the sensors detect a change in IR light or if the robot is not allowed to drive, the motors will stop rotating
19.3 Python scripts
mqtt_client.py
This script contains a class called MqttClient, which is responsible for creating an MQTT client, connecting to an MQTT broker, and publishing messages to a specific topic. It utilises the Paho MQTT library.
Key components:
__init__: Initialises the MQTT client with a topic and an optional broker (default: 'localhost').
connect_mqtt: Connects the MQTT client to the broker and sets up the on_connect callback function.
publish: Publishes a message to the specified topic.


locator.py
This script is an adaptation of the Pozyx readyToLocalize example for a digital twin demo. It connects to the anchor and remote tag using an UWB connection, gets the relative position to the anchors, and calculates the grid position based on the real-world size.
Key components:
ReadyToLocalize: The main class, which sets up the Pozyx device, connects to the MQTT broker, and continuously performs positioning.
setup: Sets up the Pozyx device for positioning by calibrating its anchor list and connects to the MQTT broker.
loop: Performs positioning and sends the results via MQTT.
publishPosition: Publishes the position of the Pozyx device to the MQTT topic.
Additional methods for handling errors, anchor configuration, and printing results.
To use these scripts, you must provide the appropriate parameters, such as the real-world size, relative anchor coordinates, and grid size. The locator.py script also imports and uses the MqttClient class from the mqtt_client.py script to send grid positions to an MQTT topic.
20. Appendix: Installation manual
20.1. Prerequisites
Arduino IDE installed on your computer.
Python version >= 3.10 installed on your computer.
PlantSim version >= 16 installed on your computer.
20.2. Required Hardware
Arduino WiFi Rev2 board
Arduino Uno Rev3 board
Pozyx tag and anchors
Appropriate power supplies and cables for the devices
20.3. Required Libraries
Install the following libraries in the Arduino IDE:
Pozyx library
Adafruit Motor Shield V2 library
WiFiNINA library
ArduinoMqttClient library
20.4. Physical build
To set up this demo one needs the following items:
4 Anchors + power cables of the pozyx kit
Stands of differing height to set up the anchors upright 
1 Tag and 1 mastertag of the pozyx kit
Usb to micro usb to connect the master tag to a pc
Arduino car which includes:
3 Power banks
2 Usb to usb-b cables to power the Arduino rev3 and rev2 wifi boards
1 Usb to micro usb to power the pozyx tag
An even area of at least 3x3 m with electrical sockets nearby
White tape if the surface of the area is black, black tape if this is not the case
One pc/laptop with all the prerequisites above installed
20.5. Building steps
Place the first anchor top left of the area you are using as the (0, 0, 0) anchor.
Place the other 3 anchors on the corners of the area you want to cover.
For the most accurate positioning the anchors need to be upright and differing placement height, an example of how they are set up is given in the picture by measurements below.
Plug the power cables into the anchors.
Plug the master tag into a pc/laptop that has all the prerequisites installed.
Fill in the IDs and coordinates of the anchors in the locator.py file as shown below.
Open up the simulation in the PlantSim software.
Recreate the following route as shown in the picture below by sticking tape to the surface.
If the surface is black, use white tape. Else use black tape. You can check if a surface is seen as black by the IR sensors by turning on the car and hovering it closely above the ground, if just one light is on on both sensors, the surface is seen as black by the sensors.
At the end of this set up guide there is a picture with measurements you can use for setting up the demonstration.
Plug in the two power banks with the usb to usb b cables into the rev3 and rev2 wifi boards.
Plug in the last power bank with the usb to micro usb cable into the pozyx tag on top of the powerbanks.
Turn on the Arduino car with the on/off switch in the middle of the car.
Put the car on the track in such a way that both IR sensors are on the outside of the tape line. The car should now start following the line on its own.
Start up the python script as explained below under the heading: Starting the demo, and run the simulation in PlantSim.
Now you should be able to start and stop the car from the simulation with the start/stop button.
20.6. Set parameters of locator.py
To set up the appropriate parameters for the locator.py script, you'll need to configure the following values:
Anchor coordinates: Replace the default anchor coordinates with the actual anchor coordinates in your setup. The coordinates are specified in millimetres. Update the anchors list in the if __name__ == '__main__': section:

anchors = [DeviceCoordinates(0x1128, 1, Coordinates(0, 2500, 240)), DeviceCoordinates(0x116F, 1, Coordinates(2500, 0, 500)), DeviceCoordinates(0x116E, 1, Coordinates(2500, 2500, 0)), DeviceCoordinates(0x113B, 1, Coordinates(0, 0, 0))]


Replace the network IDs (e.g., 0x1128) and the corresponding Coordinates with the correct values for your setup.
Grid size and the number of grids: In the ReadyToLocalize class, the following parameters are used to calculate the grid position based on the real-world size:
grid_size_x: The total size of the grid in the X direction (in millimetres).
grid_size_y: The total size of the grid in the Y direction (in millimetres).
grids_amount_x: The number of grid divisions along the X axis.
grids_amount_y: The number of grid divisions along the Y axis.
Update these values when creating a ReadyToLocalize instance in the if __name__ == '__main__': section:

r = ReadyToLocalize(pozyx, anchors, algorithm, dimension, height, remote_id, grid_size_x=2500, grid_size_y=2500, grids_amount_x=10, grids_amount_y=10)


Change the grid_size_x, grid_size_y, grids_amount_x, and grids_amount_y parameters to match your specific grid layout.
Remote ID: If you're using a remote device for positioning, set the remote_id variable to the remote device's network ID in the if __name__ == '__main__': section. If you're not using a remote device, set remote_id to None and remote to False.

remote_id = 0x684F # Remote device network ID 
remote = True # Whether to use a remote device 
if not remote: 
    remote_id = None


MQTT topic: If you want to change the MQTT topic to which the grid positions will be published, update the topic parameter when creating a ReadyToLocalize instance. By default, it is set to 'position'.
MQTT broker: If you want to use a different MQTT broker, update the broker parameter in the MqttClient class in the mqtt_client.py script. By default, it is set to 'localhost'.
After updating these parameters, the script should be ready to run and send the grid positions to the specified MQTT topic based on your setup.
20.7. Starting the demo
Compile and upload the Arduino code:
a. Open the wifi_controller.ino script in the Arduino IDE and upload it to the Arduino WiFi Rev2 board.
b. Open the car_controller.ino script in the Arduino IDE and upload it to the Arduino Uno Rev3 board.
Set up the MQTT broker:
Ensure that an MQTT broker is running and accessible to the devices. Update the broker parameter in the MqttClient class in the mqtt_client.py script with the address of the MQTT broker you are using. By default, it is set to 'localhost'.
Power up the Pozyx tag and anchors:
Connect and power up the Pozyx tag and anchors according to your setup. Ensure that they are all functioning correctly.
Configure the Python script:
Update the necessary parameters in the locator.py script, such as anchor coordinates, grid size, grid divisions, and MQTT topic. Refer to the previous explanations on how to update these parameters.
Run the Python script:
Open a command terminal, navigate to the directory containing the locator.py script, and run the following command:
python locator.py


This command will start the script, which will connect to the Pozyx tag and anchors, obtain the position data, and send the grid positions to the specified MQTT topic.

After completing these steps, the system should be up and running, with the Arduino boards controlling the car and the Python script sending grid position updates through the MQTT broker.
20.8. Demo environment measurements
All measurements are taken from the middle point of the tape, as roughly shown by the red lines. For example: A - 1 = 30cm means that from point A to side 1 with a perpendicular angle is 30cm. The measurements do not have to be exactly 1 on 1 as given below, as long as there is not too big of a difference since the simulation is based on this routing specifically. To change the routing you also need to change the markers in PlantSim. Also note that the intersection of side 1 and 4 is where the (0,0,0) coordinates are, just like in PlantSim.

Figure 8: The demo environment.
TODO add image here.

A - 1: 30cm	D - 1: 88cm	G - 2: 73cm	K - 3: 130cm	N - 1: 80cm
A - 4: 63cm	D - 2: 70cm	G - 3: 19cm	K - 4: 70cm	N - 4: 63cm
A - B: 100cm	D - E: 40 cm	G - H: 92cm	K - L: 78cm

B - 1: 30cm	E - 1: 115cm	H - 3: 19cm	L - 2: 102cm
B - 2: 87cm	E - 2: 43cm	H - 4: 84cm	L - 3: 130cm
B - C: 30cm	E - F: 90Cm	

C - 1: 52cm	F - 2: 43cm	I - 3: 48cm	M - 1: 80cm
C - 2: 70cm	F - 3: 45cm	I - 4: 53cm	M - 2: 110cm
C - D: 35cm			I - J: 59cm	M - N: 84cm

