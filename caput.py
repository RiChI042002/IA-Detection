import cv2

# Crea un objeto VideoCapture. El argumento puede ser el índice del dispositivo de la cámara o el nombre del archivo de video.
cap = cv2.VideoCapture(0)

# Define el codec y crea un objeto VideoWriter

frame_counter = 0
while(cap.isOpened()):
    # Captura cuadro por cuadro
    ret, frame = cap.read()
    if ret == True:
        

        # Muestra el cuadro resultante
        cv2.imshow('Frame', frame)

        # Rompe el bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite('/Users/richi4/Documents/universidad/SemestreIX/Laser/proyecto/imagenes/pelota{}.png'.format(frame_counter+13), frame)
            frame_counter += 1
    else:
        break

# Cuando todo esté hecho, libera los objetos de captura y escritura de video
cap.release()


# Cierra todas las ventanas
cv2.destroyAllWindows()