float sensorValue[] = {0,0,0};
bool probePush = 0;
int recentPush = 0;

void setup() {
  
  //start the serial
  Serial.begin(9600);
  pinMode(4,OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(2,INPUT);
}
void loop() {
  //Code to send position if isTouched = true
  probePush = digitalRead(2);
  
  if ( probePush == HIGH) {
    digitalWrite(4,HIGH);
  }
  
  if ( probePush == HIGH && (millis() - recentPush > 500)){
    
    for (int i = 0; i <= 2; i++) {
      sensorValue[i] = analogRead(i);
      Serial.print(sensorValue[i], DEC);
      Serial.print(" ");
    }
    recentPush = millis();
    Serial.println("");
    digitalWrite(3,HIGH);
    delay(25);
  }
  digitalWrite(4,LOW);
  digitalWrite(3,LOW);
}


