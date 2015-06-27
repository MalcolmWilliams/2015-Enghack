#include <SerialCommand.h>
#include <Servo.h> 
Servo servo1;
Servo servo2;
Servo servo3;

/*

myo input ranges

0 - 90 (120degree)  90 i right
0 - 25. 25 is low.

0, 1, 2 for grip.
0 dont move, 1 go high, 2 go low.
*/


SerialCommand sCmd;

#define PACKET_LEN 4
#define MOTOR_DELAY 10

long now, lastMotorWrite = 0;
bool inputReceived = false;

//float * input;
float input[4] = {90, 90, 90, 0};
float limitHigh[] = {140, 140, 140};
float limitLow[] = {10, 10, 10};


void setup(void)
{
  servo1.attach(6);
  servo2.attach(7);
  servo3.attach(8);
  
  /* init servos */
  servo1.write(100);
  servo2.write(160);
  servo3.write(0);
  
  pinMode(13, OUTPUT);
  
  sCmd.addCommand("g", processMyo);
  sCmd.addCommand("c", processCMM);
  sCmd.setDefaultHandler(unrecognisedCommand);
  
  Serial.begin(9600);
}


void loop(void)
{ 
  now = millis();
  
  /*
  if(Serial.available() > 0)
  {
    sCmd.readSerial();
  }
  */
  Serial.flush();
  while(Serial.available() == 0);
 
  sCmd.readSerial();
  
  if((now - lastMotorWrite) >= MOTOR_DELAY)
  {
    lastMotorWrite = now;
    //do mapping
    if(inputReceived)
    {
      
      
      /* bounds check *
      for(int i = 0; i < 3; i++)
      {
        if(input[i] >= limitHigh[i]) input[i] = limitHigh[i];
        else if(input[i] <= limitLow[i]) input[i] = limitLow[i];
      }
      * */
      
      /*
      Serial.print(input[0]);
      Serial.print(" ");
      Serial.print(input[1]);
      Serial.print(" ");
      Serial.println(input[2]);
      */
       servo1.write(input[0]);  //these inputs might be swapped
       servo2.write(input[1]);
       servo3.write(input[2]);
       
       inputReceived = false;
    }
  }
  

  
  
}

void processCMM()
{
  for(int i = 0; i < PACKET_LEN; i++)
    {
      input[i] = atof(sCmd.next());
    }
    /*
    digitalWrite(13, HIGH);
    delay(100);
    digitalWrite(13, LOW);
    */
    inputReceived = true;
}

void processMyo()
{
    for(int i = 0; i < PACKET_LEN; i++)
    {
      input[i] = atof(sCmd.next());
    }
    
    /* loopback for testing */
    for(int i = 0; i < PACKET_LEN; i++)
    {
      Serial.print(input[i]);
      Serial.print(" ");
    }
    Serial.println();
    
    input[0] = map(input[0] ,0,90,85,175);
    input[1] = map(input[1],25,0,5,90);
    
    if (input[2]==1) input[2] = 140;
    else if (input[2]==2) input[2] = 10;
    else input[2] = servo3.read();
    
    inputReceived = true;
}


void unrecognisedCommand(const char * commmand)
{
  Serial.println(F("Unrecognised"));
}
