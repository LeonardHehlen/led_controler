int greenpin = 6;
int redpin = 7;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(greenpin, OUTPUT);
  pinMode(redpin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(greenpin, LOW);
  digitalWrite(redpin, LOW);

  if (Serial.readStringUntil('\n') == "blue") {
    
    digitalWrite(greenpin, HIGH);
    Serial.println("++");
  }

  if (Serial.readStringUntil('\n') == "red") {
    
    digitalWrite(redpin, HIGH);
    Serial.println("++");

  }
}
