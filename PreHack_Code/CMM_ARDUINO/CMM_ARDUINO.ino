volatile bool button = false;
volatile float sensorValue[5];

void setup() {
  
  //start the serial
  Serial.begin(9600);
  
  //attach interrupt
  attachInterrupt(0,touch,CHANGE);
}

void loop() {
  //Code to send position if isTouched = true
  if (button == true){
    if (sensorValue[4] == 0) {
    //Constantly set all angle array values to appropriate POT values
    for (int i = 1; i <= 3; i++) {
    sensorValue[i] = analogRead(i-1);
    
    if (sensorValue[i] < 100 ){
      sensorValue[i] = sensorValue[i]*0.41;
    }
    else {
      sensorValue[i] = (0.259)*(sensorValue[i])+15.4343;
    }
    }
    
    //Printout
    for (int i = 1; i <= 3; i++) {
      Serial.print(sensorValue[i], DEC);
      Serial.print(" ");
    }
    
    Serial.println("");
    
    }
  sensorValue[4] = 1;
  }
}

void touch() {
  //change button
  button = !button;
  sensorValue[4] = 0;
}
