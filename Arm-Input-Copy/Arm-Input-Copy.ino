int rotation[3];
bool record;
bool playback;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  pinMode(0, INPUT_PULLUP);
  pinMode(1, INPUT_PULLUP);
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
  record = digitalRead(0);
  playback = digitalRead(1);
  
  Serial.println( (String)rotation[0] + " " + (String)rotation[1] + " " + (String)rotation[2] + " " + (String)(int)record + " " + (String)(int)playback);
  
  //Serial.print(" ");
  
  //}
  //Serial.println();
  delay(20);
  
}
