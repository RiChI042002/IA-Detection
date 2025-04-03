#include <ESP32Servo.h>  // Incluye la biblioteca ESP32Servo para controlar servos.
#include <WiFi.h>  // Incluye la biblioteca WiFi para conectarse a una red WiFi.

// Define las credenciales de la red WiFi a la que se conectará el ESP32.
const char* ssid = "RILOBE-2_2.4Ghz";
const char* password = "rilobe1483";

// Crea una IP estática para el servidor.
IPAddress local_IP(192, 168, 0, 184);
IPAddress gateway(192, 168, 0, 1);
IPAddress subnet(255, 255, 255, 0);

// Define las direcciones IP de los servidores DNS primario y secundario.
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

// Define el puerto del servidor.
#define SERVER_PORT 6669

// Crea un servidor que escucha las conexiones entrantes en el puerto especificado.
WiFiServer TcpServer(SERVER_PORT);

// Crea un buffer para contener los bytes entrantes enviados desde el cliente.
uint8_t receiveBuffer[255];

// Variable para almacenar el estado del interruptor.
bool switchState;

// Crea dos objetos servo.
Servo myservo;  
Servo myservo2;  

// Variable para almacenar la posición del servo.
int pos = 0;    
int valores[2];
int posAntx = 90;
int posAnty = 90;

// Define las constantes para los límites de x e y y la cantidad de movimiento.
const int X_MIN = 300;
const int X_MAX = 340;
const int Y_MIN = 220;
const int Y_MAX = 260;
const int MOVE_AMOUNT = 5;

void setup() {
  // Inicia la comunicación serial a 115200 baudios.
  Serial.begin(115200);

  // Conecta los servos a los pines GPIO 12 y 13.
  myservo.attach(12);  
  myservo2.attach(13);  

  // Escribe la posición inicial de los servos.
  myservo.write(posAntx);
  myservo2.write(posAnty); 

  // Configura el pin 2 como salida.
  pinMode(2, OUTPUT);

  // Configura la conexión WiFi con una IP estática.
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA failed to configure");
  }

  // Conecta a la red WiFi.
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // Espera hasta que la conexión WiFi esté establecida.
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  // Imprime un mensaje cuando la conexión WiFi está establecida.
  Serial.println("WiFi connected!");

  // Enciende el LED conectado al pin 2.
  digitalWrite(2, true);

  // Imprime la dirección IP local del ESP32.
  Serial.println(WiFi.localIP());

  // Inicia el servidor TCP.
  TcpServer.begin();

  // Imprime un mensaje cuando el servidor TCP está escuchando.
  Serial.println("TCP Server is listening");
}


void moverServo(int x, int y) {


  // Verifica si x está fuera de los límites definidos.
  if(!(X_MIN < x && x < X_MAX)){
    // Si x es menor que el límite inferior, mueve el servo a la derecha.
    if(x < X_MIN){
      Serial.println("derecha");
      for (pos = posAntx; pos >= posAntx - MOVE_AMOUNT; pos -= 1) { 
        myservo.write(pos); 
        delay(15);             
      }
      posAntx = pos;
    } 
    // Si x es mayor que el límite superior, mueve el servo a la izquierda.
    if(x > X_MAX){
      Serial.println("izquierda");
      for (pos = posAntx; pos <= posAntx + MOVE_AMOUNT; pos += 1) { 
        myservo.write(pos); 
        delay(15);             
      }
      posAntx = pos;
    }
  }

  // Verifica si y está fuera de los límites definidos.
  if(!(Y_MIN < y && y < Y_MAX)){
    // Si y es menor que el límite inferior, mueve el servo hacia arriba.
    if(y < Y_MIN){
      Serial.println("arriba");
      for (pos = posAnty; pos >= posAnty - MOVE_AMOUNT; pos -= 1) { 
        myservo2.write(pos); 
        delay(15);             
      }
      posAnty = pos;
    } 
    // Si y es mayor que el límite superior, mueve el servo hacia abajo.
    if(y > Y_MAX){
      Serial.println("abajo");
      for (pos = posAnty; pos <= posAnty + MOVE_AMOUNT; pos += 1) { 
        myservo2.write(pos); 
        delay(15);             
      }
      posAnty = pos;
    }
  } 
}



void loop() {
  //Gets a client that is connected to the server and has data available for reading
  //Returns a Client object
  WiFiClient TcpClient = TcpServer.available();

  if (TcpClient) {

    if (TcpClient.connected()) {
      Serial.println("TcpClient connect");
      digitalWrite(2, true);
      switchState = true;
      Serial.println(switchState);

      Serial.println("server is waiting for incoming data");
    }
    //TcpClient.connected() returns true if the client is connected, false if not
    //while TcpClient is connected, perform read write operations
    while (TcpClient.connected()) {

      //if there are incoming bytes available read them and print them
      //TcpClient.available() returns the number of bytes available for reading
      if (switchState) {
        if (TcpClient.available() > 0) {
          
          leerDatosCliente(TcpClient);
          moverServo(valores[0], valores[1]);
          /*a real check to ensure transmission has been completed
          Discard any bytes that have been written but not yet read
          else TcpClient.available() always returns the number of 
          bytes available for reading > 0*/
          TcpClient.flush();
          Serial.println(switchState);
          switchState = false;
          
          // break;
        }
      }

      //Get the number of bytes (characters) available for reading from the serial port
      //Serial.available() returns the number of bytes available to read.
      if (!switchState) {
        String incomingString = 'listopa$\n';

          //create a buffer to contain bytes that server will send to client
        uint8_t sendBuffer[incomingString.length()];

          //copy the string's characters to the sendBuffer.
        incomingString.getBytes(sendBuffer, incomingString.length());

          //send data in sendBuffer to client
        TcpClient.write(sendBuffer, sizeof(sendBuffer));
        switchState = true;
      }
    }

    //ckeck whether or not the client is connected
    if (!TcpClient.connected()) {
      digitalWrite(2, false);
      Serial.println();
      Serial.println("Client has disconnected");
      TcpClient.stop();
    }
    delay(1000);
  }
}


void leerDatosCliente(WiFiClient TcpClient) {

    // Leer los bytes entrantes del cliente y guardarlos en receiveBuffer
    int c = TcpClient.read(receiveBuffer, sizeof(receiveBuffer));

    // Procesamiento de datos
    for (size_t j = 0; j < strlen((char*)receiveBuffer); j++) {
      if (receiveBuffer[j] == '$') {
        receiveBuffer[j] = '\0';
        break;
      }
    }

    // Dividir la cadena en partes basándose en la coma como delimitador
    char* token = strtok(((char*)receiveBuffer), ",");
    int i = 0;
    while (token != NULL && i < 2) {
      // Convertir cada parte a un entero y guardarla en el array
      valores[i] = atoi(token);
      i++;

      // Obtener la siguiente parte
      token = strtok(NULL, ",");
    }
    
}