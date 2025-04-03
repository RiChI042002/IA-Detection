#include <ESP32Servo.h>

Servo myservo;  // crea un objeto servo
Servo myservo2;  // crea un objeto servo
int pos = 0;    // variable para almacenar la posición del servo

int posAntx = 90;
int posAnty = 90;

void setup() {
    myservo.attach(12);  // conecta el servo al pin GPIO 12   
    myservo2.attach(13);  // conecta el servo al pin GPIO 13
    Serial.begin(115200);
    Serial.println("Servo inicializado");
    myservo.write(90);
    myservo2.write(90);
}

void moverServo(int x, int y) {
  int mover = 10;
  Serial.println("entro a mover");
  if(!(300 < x && x < 340)){
    if(x < 300){
      Serial.println("derecha");
      for (pos = posAntx; pos >= posAntx - mover; pos -= 1) { 
        myservo.write(pos); 
        delay(15);             
      }
      posAntx = pos;
    } 
    if(x > 340){
      Serial.println("izquierda");
      for (pos = posAntx; pos <= posAntx + mover; pos += 1) { 
        myservo.write(pos); 
        delay(15);             
      }
      posAntx = pos;
    }
  }

  if(!(220 < y && y < 260)){
    if(y < 220){
      Serial.println("arriba");
      for (pos = posAnty; pos >= posAnty - mover; pos -= 1) { 
        myservo2.write(pos); 
        delay(15);             
      }
      posAnty = pos;
    } 
    if(y > 260){
      Serial.println("abajo");
      for (pos = posAnty; pos <= posAnty + mover; pos += 1) { 
        myservo2.write(pos); 
        delay(15);             
      }
      posAnty = pos;
    }
  } 
}

void leerSerial(){
  if(Serial.available() > 0){
    String data = Serial.readString();

    
    int x = data.substring(0, 3).toInt();
    int y = data.substring(4, 7).toInt();
    moverServo(x, y);
  }
}

void loop() {
  leerSerial();
}