import cv2
from roboflow import Roboflow

rf = Roboflow(api_key="MgHoVZRK2j7xXdTabYHo")
project = rf.workspace().project("pelota-dxie4")
model = project.version("1").model

cap = cv2.VideoCapture(0)

while True:
    # Captura un frame
    
    ret, frame = cap.read()
    if not ret:
        break   
    
    # Usa el modelo para predecir en el frame
    data = model.predict(frame).json()    

    try:
        # Dibuja los resultados de la predicción en el frame
        for prediction in data['predictions']:
            x = prediction['x']
            y = prediction['y']
            width = prediction['width']
            height = prediction['height']
            cv2.rectangle(frame, (int(x - width / 2), int(y - height / 2)), (int(x + width / 2), int(y + height / 2)), (0, 255, 0), 2)
        # Muestra el frame
        cv2.imshow('Frame', frame)

            # Si se presiona la tecla 'q', rompe el bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    
    except:
    

        # Muestra el frame
        cv2.imshow('Frame', frame)

            # Si se presiona la tecla 'q', rompe el bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Libera todo si el trabajo ha terminado
cap.release()

cv2.destroyAllWindows()