#include <Wire.h>

#define DEVICE_A (0x1D)    
#define DEVICE_B (0x53)    
#define TO_READ (6)        

byte buff[TO_READ];        
char str[64];              

void writeTo(int device, byte address, byte val) {
   Wire.beginTransmission(device);
   Wire.write(address);
   Wire.write(val);
   Wire.endTransmission();
}

void readFrom(int device, byte address, int num, byte buff[]) {
  Wire.beginTransmission(device);
  Wire.write(address);
  Wire.endTransmission(false); // Restart condition

  delay(10); // Give ADXL345 time to respond

  Wire.requestFrom(device, num);
  
  for (int i = 0; i < num; i++) {
    if (Wire.available()) {
      buff[i] = Wire.read();
    } else {
      buff[i] = 0; // Default if no data available
    }
  }
}

void setup() {
  Wire.begin();        
  Serial.begin(115200); 
  
  writeTo(DEVICE_A, 0x2D, 8);
  writeTo(DEVICE_B, 0x2D, 8);
}

void loop() {
  int xa, ya, za, xb, yb, zb;
  int regAddress = 0x32;

  readFrom(DEVICE_A, regAddress, TO_READ, buff);
  xa = (((int)buff[1]) << 8) | buff[0];
  ya = (((int)buff[3]) << 8) | buff[2];
  za = (((int)buff[5]) << 8) | buff[4];

  readFrom(DEVICE_B, regAddress, TO_READ, buff);
  xb = (((int)buff[1]) << 8) | buff[0];
  yb = (((int)buff[3]) << 8) | buff[2];
  zb = (((int)buff[5]) << 8) | buff[4];

  sprintf(str, "%d %d %d %d %d %d", xa, ya, za, xb, yb, zb);
  Serial.println(str);

  delay(200); // delay between readings in ms
}
