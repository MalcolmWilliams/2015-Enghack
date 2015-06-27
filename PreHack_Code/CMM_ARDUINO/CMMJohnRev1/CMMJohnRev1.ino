float sensorValue[3] = {-1024,-1024,-1024};
//first three are pot readings;
float previousPot[3] = {-1024,-1024,-1024};
//These are the previous pot values to preventing double reads

boolean debounceCheck = true;
//will be 1 if current reading is new; 0 if too close to the old reading
int debounceRange = 5;
//range that the new pot value must exceed to count as a new contact

boolean probePush = 0;
//

void setup() {
  
  //start the serial
  Serial.begin(9600);
  
  pinMode(2,INPUT);//probe
  pinMode(3,OUTPUT);//buzzer
  pinMode(4,OUTPUT);//baselight
  pinMode(5,OUTPUT);//touch status light
  //digitalWrite(4,HIGH);
  
  //make cool beep noise on start
  digitalWrite(3,HIGH);
  delay(125);
  digitalWrite(3,LOW);
  delay(75);
  digitalWrite(3,HIGH);
  delay(25);
  digitalWrite(3,LOW);
  delay(75);
  digitalWrite(3,HIGH);
  delay(25);
  digitalWrite(3,LOW);
}// end setup()

void loop() 
{
  probePush = digitalRead(2);
  //reads if probe has touched something
  if(probePush)
    digitalWrite(5,HIGH);
  else
    digitalWrite(5,LOW);
  
  for (int i = 0; i <= 2; i++) 
  {//get current pot locations
    sensorValue[i] = analogRead(i);
  }//end for loop
    
  if ((sensorValue[0]>(previousPot[0]+debounceRange)||sensorValue[0]<(previousPot[0]-debounceRange)
        ||sensorValue[1]>(previousPot[1]+debounceRange)||sensorValue[1]<(previousPot[1]-debounceRange)
        ||sensorValue[2]>(previousPot[2]+debounceRange)||sensorValue[2]<(previousPot[2]-debounceRange))
        &&probePush==LOW)
    debounceCheck = true;
    //if the pot readings are not too close the the last touch and the probe is no longer in contact, the check will be reset to true
  
  if (probePush == HIGH && debounceCheck)
  {//if the probe is touched and the debounce is all good then print the value
    digitalWrite(3,HIGH);
    digitalWrite(4,LOW);
    delay(25);
    digitalWrite(3,LOW);
    digitalWrite(4,HIGH);
    //buzz upon touch
    debounceCheck = false;
    //debounce is set to false indicating a touch has just been completed in this coordinate area
    
    for (int i = 0; i <= 2; i++) 
    {//print each pot value out one by one and copy last sucessful touch location to memory
    previousPot[i] = sensorValue[i];
    Serial.print(sensorValue[i], DEC);
    Serial.print(" ");
    }//end print loop
    
    Serial.println("");
    
  }//end if
  
}//end loop()


