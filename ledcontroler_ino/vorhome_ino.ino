#include <Servo.h>

Servo livingroom_curtain;

int greenpin = 6;
int redpin = 7;
// c_lr = curtain living room
int open_c_lr = 25;
int close_c_lr = 170;
int none_c_lr = 90;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(greenpin, OUTPUT);
  pinMode(redpin, OUTPUT);
  livingroom_curtain.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(greenpin, LOW);
  digitalWrite(redpin, LOW);
  livingroom_curtain.write(none_c_lr);
  
  if (Serial.readStringUntil('\n') == "open") {
    livingroom_curtain.write(open_c_lr);
    Serial.println("++");
  }
  if (Serial.readStringUntil('\n') == "close") {
    livingroom_curtain.write(close_c_lr);
    Serial.println("++");
  }


  if (Serial.readStringUntil('\n') == "blue") {
    
    digitalWrite(greenpin, HIGH);
    Serial.println("++");
  }

  if (Serial.readStringUntil('\n') == "red") {
    
    digitalWrite(redpin, HIGH);
    delay(50);
    Serial.println("++");

  }
}
