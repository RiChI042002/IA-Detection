import cv2
import numpy as np

# Abre la cámara
cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    # Lee un frame
    ret, frame = cap.read()
    if ret == True:
        

        # Muestra el frame
        cv2.imshow('frame', frame)

        # Si se presiona la tecla 'q', termina el bucle
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Libera los recursos
cap.release()

cv2.destroyAllWindows()