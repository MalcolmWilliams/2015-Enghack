#define LED 13

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);
  Serial.flush();
}

void loop() {
  // put your main code here, to run repeatedly:
  //if(Serial.available() > 0)
  //{
    Serial.println(Serial.readStringUntil('\n'));
    //Serial.flush();
    //digitalWrite(LED, HIGH);
    //delay(100);
    //digitalWrite(LED, LOW);
  //}
}
