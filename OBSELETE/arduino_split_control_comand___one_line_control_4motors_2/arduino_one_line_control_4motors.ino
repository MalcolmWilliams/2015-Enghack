#include <string.h>
#include <Servo.h> 
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
String serialdata ="";

void setup()
{
  servo1.attach(6);
  servo2.attach(7);
  servo3.attach(8);
  servo4.attach(9);
  Serial.begin(9600);
  // Serial.print("gewaghgh");
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
}

void loop(){
int prepos=0;
  while (Serial.available() > 0)
  {
    int inChar= Serial.read();
    /*    if (isDigit(inChar))
     {
     Serial.println("is number");
     }
     */
    serialdata += char(inChar);
    //comdata += char(inChar);
    delay(2);
  }
  if (serialdata.length()>0){  
    Serial.println(serialdata);
  serialdata=serialdata+" ";}

  int servonum=0;
  int servov[4]; 
  //String serialdata = "13 145 110 10";
  // prepos=0;
  String str="";
  if (serialdata.length()>0){
    Serial.print("sizeof(serialdata)");
    Serial.println(serialdata.length());
  }
  int x= serialdata.length();
  for (int pos=0; pos <x; pos++){
    Serial.print("pos");
    Serial.println(pos);  
    Serial.print("serialdata[pos]");
    Serial.println(serialdata[pos]);

    if(serialdata[pos]==' '){
      str = serialdata.substring(prepos,pos);
      Serial.print("str = serialdata.substring(prepos,pos);");
      Serial.println(serialdata.substring(prepos,pos));
      prepos=pos;
      servov[servonum]=str.toInt();
      Serial.print("pos=");
      Serial.println(servov[servonum]);
      str="";
      servonum++;
    }
  }

  //for (int servon=0;servon<=3;servon++){
  //    Serial.print(servon);
  //    Serial.println(servov[servon]);
  if (serialdata.length() > 0)
  {
    for (int servon=0;servon<=3;servon++){
      Serial.print(servon);
      Serial.print(" has ");
      Serial.println(servov[servon]);
    }
    servo1.write(servov[0]);
    servo2.write(servov[1]);
    servo3.write(servov[2]);
    servo4.write(servov[3]);
    serialdata = "";
  }
  //  }
}





