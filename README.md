YOLOv8 Ball Tracking with ESP32 and Servos

This repository presents a computer vision and IoT project that enables real-time ball tracking using artificial intelligence. Utilizing YOLOv8, the system detects the ball's position and, via TCP/IP, sends signals to an ESP32, which adjusts the orientation of two servomotors to follow the ball's movement.

🎯 Project Objective

Develop a computer vision and IoT system capable of detecting and tracking objects in real-time, applicable to automation, robotics, and sports. This project demonstrates expertise in machine learning, image processing, network communication, and embedded systems.

📌 Technologies & Tools

YOLOv8 (Ultralytics): Deep learning model for real-time object detection.

OpenCV: Image processing and ball coordinate extraction.

Python (Sockets, NumPy, OpenCV): Implementation of image processing and communication with ESP32.

ESP32 + MicroPython / Arduino IDE: Servo control based on received data.

TCP/IP Communication Protocols: Transmission of detection data between the computer and ESP32.

Embedded Hardware: Integration of microcontrollers and actuators.

🛠️ Implementation

Hardware Used

Camera (webcam or compatible module)

ESP32 (microcontroller for communication and servo control)

2 Servomotors (SG90, MG995, etc.)

Appropriate power supply

Software & Configuration

1️⃣ Install dependencies

pip install ultralytics opencv-python numpy pyserial

2️⃣ YOLOv8 Model Setup

Download and install YOLOv8.

Use a pre-trained model or train one with ball images.

3️⃣ ESP32 Configuration

Flash MicroPython onto the ESP32 or use Arduino IDE.

Upload the code to receive TCP/IP data and control servos.

🔄 Workflow

The camera captures real-time video.

YOLOv8 detects the ball and retrieves its coordinates.

Coordinates are sent to ESP32 via TCP/IP.

ESP32 adjusts the servos to follow the ball.

🚀 Results & Applications

This system can be applied in robotics, industrial automation, sports, and computer vision. It can be enhanced with trajectory prediction algorithms and adapted for autonomous robots or sports training systems.

📷 Detection Example

(Add an image or GIF showcasing the system in action)
