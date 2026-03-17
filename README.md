# Emotion-Sensing Affective Robotic System

This project implements a real-time **Human-Robot Interaction (HRI)** system. It uses Computer Vision and Deep Learning to recognize human emotions via a webcam and translates those emotions into physical robotic movements using an ESP32-controlled 4-wheel chassis.

---

## 🚀 System Architecture & Workflow

The project utilizes a distributed computing approach where a PC handles high-level AI processing and an ESP32 manages real-time hardware actuation.

* **Vision & Detection**: **OpenCV** captures live video, and **Haar Cascade** classifiers isolate the face (Region of Interest).
* **Emotion Inference**: The cropped face is processed by a **Mini-Xception** model running on **TensorFlow**.
* **Training**: The model is pre-trained on the **FER2013 dataset**, allowing it to classify 7 emotional states: Happy, Sad, Angry, Surprise, Neutral, Fear, and Disgust.
* **Communication**: The PC sends an **HTTP GET request** wirelessly over Wi-Fi to the ESP32’s local IP address.
* **Actuation**: The **ESP32** receives the command and signals the **L298N Motor Driver** to execute specific movements.

---

## 🛠️ Technical Stack

* **Languages**: Python 3.x, C++ (Arduino/ESP32)
* **AI Libraries**: TensorFlow, Keras, OpenCV
* **Hardware**: ESP32 Microcontroller, L298N Dual H-Bridge, 4-wheel Robotic Chassis
* **Communication**: HTTP Protocol via Wi-Fi

---

## 🤖 Emotion-Movement Mapping

| Emotion | Robot Action | Command Path |
| :--- | :--- | :--- |
| **Happy** | Fast Spin Circle | `/circle` |
| **Sad** | Slow Forward | `/slowforward` |
| **Angry** | Rapid Shake | `/shake` |
| **Surprise** | Quick Back-Stop | `/backstop` |
| **Neutral** | Idle / Stop | `/stop` |

---

## 📂 Project Structure

* `bot (1).py`: Main Python script for face detection and emotion classification.
* `emotion_model.hdf5`: Pre-trained Mini-Xception model weights.
* `emootion_bot_firmware.ino`: ESP32 source code for web server and motor control.
