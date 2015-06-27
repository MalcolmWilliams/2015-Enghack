float sensorValue[4] = {0,0,0,1};
int probePush = 0;
int recentPush = 0;

void setup() {
  
  //start the serial
  Serial.begin(9600);
  
  pinMode(2,INPUT);
}
void loop() {
  //Code to send position if isTouched = true
  probePush = digitalRead(2);
  
  if ( probePush == HIGH && sensorValue[4] != 0){
    
    for (int i = 0; i <= 2; i++) {
    sensorValue[i] = analogRead(i);
    Serial.print(sensorValue[i], DEC);
    Serial.print(" ");
    recentPush = millis();
    sensorValue[3] = 0;
    }
    Serial.println("");
  }
  
  if (millis() - recentPush > 1000) {
    sensorValue[3] = 1;
  }
  
}


