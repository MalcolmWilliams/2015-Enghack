#include <SerialCommand.h>

SerialCommand sCmd;

#define PACKET_LEN 4
float * input;

void setup(void)
{

  sCmd.addCommand("g", processPacket);
  sCmd.setDefaultHandler(unrecognisedCommand);
  
  Serial.begin(9600);
}


void loop(void)
{ 
  if(Serial.available() > 0)
  {
    sCmd.readSerial();
  }
  
}


void processPacket()
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
}


void unrecognisedCommand(const char * commmand)
{
  Serial.println(F("Unrecognised"));
}


