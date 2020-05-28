#include <Servo.h>

Servo volet_salon;

void setup() {
  // put your setup code here, to run once:`
  Serial.begin(115200);
  volet_salon.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
 volet_salon.write(90);
 delay(5000);
 volet_salon.write(25);
 delay(5000); 
  volet_salon.write(155);
 delay(5000); 
}
