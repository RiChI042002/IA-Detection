# Importa las bibliotecas necesarias
import cv2
from roboflow import Roboflow
import concurrent.futures


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

# Bucle infinito para procesar cada frame
while True:
    # Captura un frame
    ret, frame = cap.read()
    print(frame.shape)
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
    
    
# Libera los recursos de la cámara y cierra las ventanas

cap.release()
cv2.destroyAllWindows()

