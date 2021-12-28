#include <Wire.h>

#define I2C_ADDR 11
#define R1 11
#define Y1 12
#define G1 13
#define R2 5
#define Y2 6
#define G2 7


#define MAP 55
#define LOOP 66
#define FOREVER 77

const unsigned LEDS[] = {R1,Y1,G1,R2,Y2,G2};

unsigned len;
byte msg[20];
byte cmd = 0;
unsigned index = 0;
unsigned cntdown = 0;

// -----------------------------------------------------
void setup() {
  Wire.begin(I2C_ADDR);
  Serial.begin(9600);
  for(int i=0; i<6; i++)
    pinMode(LEDS[i],OUTPUT); 
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
}

void mapLED(byte dat) {
  for(int i=0; i<6; i++)
    digitalWrite(LEDS[i],dat&(0b00000001<<i)?HIGH:LOW);
}

// -----------------------------------------------------
void loop() {
  switch(cmd) {
    case 0: break;
    case MAP: 
        mapLED(msg[1]);
        cmd = 0;
      break;
    case LOOP: if (cntdown<=0) {
                cmd=0;
                break;
               }
    case FOREVER:  
        mapLED(msg[index++]);
        delay(msg[index++]*100);
        if (index>=len) {
          index = 1;
          cntdown--;
        }
      break;
    default: break;
  }
  delay(1);
}

// -----------------------------------------------------
void irsReceive(int nb) {
  len = 0;
  while (Wire.available())
    msg[len++] = Wire.read();
  cmd = msg[0];  
  disp_msg();
  index = 0;
  cntdown = 0;
  switch(cmd){
    case LOOP: cntdown = msg[len-1];
               len--;
    case FOREVER: index = 1;
  }
}
