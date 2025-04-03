# Importa las bibliotecas necesarias
import cv2
from roboflow import Roboflow
import concurrent.futures
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


# Inicializa Roboflow con tu clave de API
rf = Roboflow(api_key="MgHoVZRK2j7xXdTabYHo")

# Selecciona el proyecto y la versión del modelo en Roboflow
project = rf.workspace().project("pelota-dxie4")
model = project.version("1").model

# Inicia la captura de video desde la cámara (0 indica la cámara predeterminada)
cap = cv2.VideoCapture(0)

# Crea un executor para procesar los frames en un hilo separado
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# Inicializa un contador de frames
frame_counter = 0

switchState = 1


x=0
y=0
width=0
height=0

r1=720
r2=1280

desvio=0.05

def interne():
    global switchState, TCPClientSocket, bufferSize, receivedData, ServerIP, ServerPort, x, y, width, height
    
    if not switchState:
        
        try:
            receivedData = TCPClientSocket.recv(bufferSize).decode('utf-8')
        except:
            print("something's wrong, client can't receive data from server")

        if not receivedData: 
           return
        else:
            if receivedData == "ya":
                switchState = not switchState
                   
    
    if switchState:
        
        if  (r1/2 + desvio*r1)<int(x)<(r1/2 - desvio*r1) and (r2/2 + desvio*r2)<int(y)<(r2/2 - desvio*r2):
            return
        else:
            msg = (str(x)+","+str(y)+","+str(width)+","+str(height)+"$").encode('utf-8')
            
            try:
                TCPClientSocket.sendall(msg)
                switchState = not switchState
                print("client is wating for incoming data")
            except:
                print("something's wrong, client can't send data to server")
                return
            
        
        
    
            
thread1 = threading.Thread(target=interne)

thread1.start()



# Bucle infinito para procesar cada frame
while True:
    # Captura un frame
    ret, frame = cap.read()
    # Si no se pudo capturar un frame, rompe el bucle
    
    if not ret:
        break   

    # Incrementa el contador de frames
    frame_counter += 1

    # Si el contador de frames es un múltiplo de 2, procesa el frame
    if frame_counter % 2 == 0:
        # Reduce la resolución del frame a la mitad
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))

        # Usa el modelo para predecir en el frame
        
        
        # Se envía la tarea de predicción al executor, que la ejecutará en un hilo separado
        future = executor.submit(model.predict, frame)
        # Espera a que la tarea de predicción se complete y obtiene el resultado
        data = future.result().json()    

        try:
            # Dibuja los resultados de la predicción en el frame
            for prediction in data['predictions']:
                # Obtiene las coordenadas del centro del objeto predicho
                x = prediction['x']
                y = prediction['y']
                # Obtiene el ancho y la altura del objeto predicho
                width = prediction['width']
                height = prediction['height']
                
                # Dibuja un rectángulo alrededor del objeto predicho
                cv2.rectangle(frame, (int(x - width / 2), int(y - height / 2)), (int(x + width / 2), int(y + height / 2)), (0, 255, 0), 2)
                
            if not thread1.is_alive():
                thread1.start()
                
                
            # Muestra el frame con los objetos predichos
            cv2.imshow('Frame', frame)

            # Si se presiona la tecla 'q', rompe el bucle
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            # Si hay un error al procesar las predicciones, simplemente muestra el frame sin las predicciones
            cv2.imshow('Frame', frame)

    # Si se presiona la tecla 'q', rompe el bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        salir = True
    
    
# Libera los recursos de la cámara y cierra las ventanas

thread1.join()
cap.release()
cv2.destroyAllWindows()

