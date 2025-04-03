# Importamos las librerias
from ultralytics import YOLO
import cv2
import socket
import threading

ServerIP = "192.168.0.184"
ServerPort = 6669

TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
TCPClientSocket.connect((ServerIP, ServerPort))

print("TCP client connected to server and ready to perform read write operations")
print(f"Connected by server {ServerIP}")

receivedData = ""
bufferSize = 1024

x1=0
y1=0
x2=0
y2=0

switchState = 1


def interne():
    global switchState, TCPClientSocket, bufferSize, receivedData, ServerIP, ServerPort, x1, y1, x2, y2
    
    desvio=0.1
    if not switchState:
        
        try:
            receivedData = TCPClientSocket.recv(bufferSize).decode('utf-8')
            if not receivedData: 
                return
            else:
                switchState = not switchState
        except:
            print("something's wrong, client can't receive data from server")

        
                   
    
    if switchState:
        
        r1=x2-x1
        r2=y2-y1
        
        centro=(480/2,640/2)  
        centroCaja=(r1/2 + x1,r2/2 + y1)
        
        if (centroCaja[0] - desvio*r1 <centro[0]<centroCaja[0] + desvio*r1) and centroCaja[1] - desvio*r2 <centro[1]<centroCaja[1] + desvio*r2:
            return
        else:
            msg = (str(int(centroCaja[0]))+","+str(int(centroCaja[1]))+"$").encode('utf-8')
            
            try:
                TCPClientSocket.sendall(msg)
                switchState = not switchState
                print("client is wating for incoming data")
            except:
                print("something's wrong, client can't send data to server")
                return
        

hilo = threading.Thread(target=interne)
hilo.start()
# Leer nuestro modelo
model = YOLO("final/best.pt")

# Realizar VideoCaptura
cap = cv2.VideoCapture(0)

# Bucle
while True:
    # Leer nuestros fotogramas
    ret, frame = cap.read()

    # Leemos resultados
    resultados = model.predict(frame, imgsz = 640, conf = 0.3)
    

    # Para cada objeto detectado
    for resultado in resultados:
    # Para cada caja delimitadora en el resultado
        for deteccion in resultado.boxes.boxes:
            # Convertimos el tensor a una lista de Python
            deteccion_lista = deteccion.cpu().numpy().tolist()

            # Extraemos las coordenadas del cuadro delimitador y la confianza
            x1, y1, x2, y2, conf, cls = deteccion_lista

    
    if not hilo.is_alive():
        hilo = threading.Thread(target=interne)
        hilo.start()
    
            
    

    # Mostramos resultados
    anotaciones = resultados[0].plot()
    
    

    # Mostramos nuestros fotogramas
    cv2.imshow("DETECCION Y SEGMENTACION", anotaciones)

    # Cerrar nuestro programa
    if cv2.waitKey(1) == 27:
        break




cap.release()
cv2.destroyAllWindows()