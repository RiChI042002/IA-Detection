#include <ESP32Servo.h>

Servo myservo;  // crea un objeto servo
int pos = 0;    // variable para almacenar la posición del servo

void setup() {
  myservo.attach(12);  // conecta el servo al pin GPIO 13
}

void moverServo(Servo servo, int posicion) {
  servo.write(posicion);
  delay(15);  // espera 15ms para que el servo alcance la posición
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) { // va de 0 grados a 180 grados
    // en pasos de 1 grado
    myservo.write(pos);              // le dice al servo que vaya a la posición en variable 'pos'
    delay(15);                       // espera 15ms para que el servo alcance la posición
  }
  for (pos = 180; pos >= 0; pos -= 1) { // va de 180 grados a 0 grados
    myservo.write(pos);              // le dice al servo que vaya a la posición en variable 'pos'
    delay(15);                       // espera 15ms para que el servo alcance la posición
  }
}