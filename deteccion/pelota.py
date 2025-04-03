import os
from roboflow import Roboflow

# Cambia el directorio de trabajo al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

rf = Roboflow(api_key="MgHoVZRK2j7xXdTabYHo")
project = rf.workspace().project("pelota-dxie4")
model = project.version("1").model

print(model.predict("/Users/richi4/Documents/universidad/SemestreIX/Laser/proyecto/deteccion/pelo.jpeg", confidence=40, overlap=30).json())