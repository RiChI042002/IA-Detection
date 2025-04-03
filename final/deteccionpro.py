# Importamos las librerias
from ultralytics import YOLO
import cv2

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

            print(f"Posición: ({x1}, {y1}), ({x2}, {y2}), Confianza: {conf}, Clase: {cls}")

    # Mostramos resultados
    anotaciones = resultados[0].plot()
    
    

    # Mostramos nuestros fotogramas
    cv2.imshow("DETECCION Y SEGMENTACION", anotaciones)

    # Cerrar nuestro programa
    if cv2.waitKey(1) == 27:
        break

        

cap.release()
cv2.destroyAllWindows()