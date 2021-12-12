#include <Wire.h>

#define I2C_ADDR 11
#define R 11
#define Y 12
#define G 13

unsigned len;
byte msg[20];
byte cmd = 0;

// -----------------------------------------------------
void setup() {
  Wire.begin(I2C_ADDR);
  Serial.begin(9600);
  pinMode(R,OUTPUT); 
  pinMode(Y,OUTPUT); 
  pinMode(G,OUTPUT); 
  Serial.print("MQTT + I2C Homework 01: ");
  Serial.println(I2C_ADDR);
  Serial.println("======================================");
  delay(1000);    
  // register onReceive event services           
  Wire.onReceive(irsReceive);
}

void disp_msg() {
    Serial.print("Received data  : ");
    for(int i=0; i<len; i++) {
      Serial.print(msg[i]);
      Serial.print(" ");
    }
    Serial.println();  
    cmd = 0;
}

void LED(int pin, int stu) {
  digitalWrite(pin,stu);  
  cmd = 255;
}

// -----------------------------------------------------
void loop() {
  switch(cmd) {
    case 0   : break;
    case 1   : LED(R,0); break;
    case 2   : LED(R,1); break;
    case 3   : LED(Y,0); break;
    case 4   : LED(Y,1); break;
    case 5   : LED(G,0); break;
    case 6   : LED(G,1); break;
    case 255 :
    default  : disp_msg();
  }
  delay(0);
}

// -----------------------------------------------------
void irsReceive(int nb) {
  len = 0;
  while (Wire.available())
    msg[len++] = Wire.read();
  cmd = msg[0];  
}
