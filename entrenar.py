

from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# Use the model
print('entranando')
model.train(data=r"C:\Users\Fabian\Documents\proyecto\datas\dataset.yaml", epochs=3)  # train the model
print(model)  # print model information