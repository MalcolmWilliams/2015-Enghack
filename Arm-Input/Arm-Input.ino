int rotation[3];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
}

void loop() {
  //for(int i = 0; i < 3; i++)
  //{
    //rotation[i] = analogRead(i);
    //Serial.print(rotation[i]);
    //Serial.print(" ");
    
    /*
  Serial.print(map(analogRead(0), 0, 1024, 85,175));
  Serial.print(" ");
  Serial.print(map(analogRead(1), 300, 750, 90, 5));
  Serial.print(" ");
  Serial.print(map(analogRead(2), 100, 700, 140, 10));
  //Serial.print(analogRead(2));
  */
  
  rotation[0] = map(analogRead(0), 250, 774, 85,175);
  rotation[1]= map(analogRead(1), 500, 700, 90, 5);
  rotation[2] = map(analogRead(2), 100, 500, 140, 10);
  
  Serial.println( (String)rotation[0] + " " + (String)rotation[1] + " " + (String)rotation[2] );
  
  //Serial.print(" ");
  
  //}
  //Serial.println();
  delay(20);
  
}
