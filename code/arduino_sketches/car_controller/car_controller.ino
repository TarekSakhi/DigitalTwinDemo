#include <AFMotor.h>

AF_DCMotor  motor_right(1);
AF_DCMotor  motor_left(2);

// Defining the pins, A means it's an analog pin
#define L_S A5
#define R_S A0
#define WIFI_BOARD A1

void setup() {
  // Set-up IR sensors
  pinMode(L_S, INPUT);
  pinMode(R_S, INPUT);

  // Set-up wifi board output sensor
  pinMode(WIFI_BOARD, INPUT);

  // Set-up motors
  motor_right.setSpeed(140);
	motor_right.run(RELEASE);

  motor_left.setSpeed(140);
	motor_left.run(RELEASE);

  /*
  Initialize serial and wait for port to open
  Serial prints can be read through the serial monitor in the Arduino IDE
  */
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
}

void loop() {
  // Read the input from the WIFI_BOARD, to see if can drive
  int wifi_read = digitalRead(WIFI_BOARD);
  Serial.println(wifi_read); 

  /*
  If the sensos detects a change in IR light or is not allowed to drive,
  the motor will stop rotating. This happens for both motors.
  */ 
  if(digitalRead(L_S) == 1) {
    motor_left.run(RELEASE);
  } else {
    if(wifi_read == 1) {
      motor_left.run(BACKWARD);
    } else {
      motor_left.run(RELEASE);
    }
  }

  if(digitalRead(R_S) == 1) {
    motor_right.run(RELEASE);
  } else {
    if(wifi_read == 1) {
      motor_right.run(BACKWARD);
    } else {
      motor_right.run(RELEASE);
    }
  }
}
