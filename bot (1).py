import cv2
import numpy as np
import requests
from tensorflow.keras.models import load_model
import pyttsx3
import time
import pygame  # for music
import sys
import io

# Force the standard output to use UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== CONFIG ======
ESP32_IP = "http://10.157.45.104"  # Replace with your ESP32 IP
MODEL_PATH = r"emotion_model.hdf5"

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Emotion → command mapping (based on image)
emotion_to_command = {
    'Happy': 'circle',
    'Sad': 'slowforward',
    'Angry': 'shake',
    'Surprise': 'backstop',
    'Neutral': 'stop',
    'Fear': 'stop',
    'Disgust': 'stop'
}

# Comforting messages
COMFORT_MESSAGES = {
    "Angry": "I can see you're upset. Take a deep breath. If you want, press a break and let's relax together.",
    "Disgust": "I understand this is unpleasant. It's okay to take a pause and step back.",
    "Fear": "I am here with you. Take slow breaths — you're not alone.",
    "Happy": "You look happy! Keep smiling. I'm glad to see you feeling good.",
    "Neutral": "Hope you are having a calm moment. Let me know if you'd like a short break.",
    "Sad": "I am sorry you're feeling sad. It's okay to feel this way — sending you a gentle thought.",
    "Surprise": "That looked like a surprise! Take your time. Everything is okay."
}

# Load model
print("Loading model...")
model = load_model(MODEL_PATH, compile=False)
print("✅ Model loaded.")

# Load face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize text-to-speech
tts = pyttsx3.init()
tts.setProperty('rate', 165)

# Initialize music system
pygame.mixer.init()

def play_music():
    """Play relaxing tune after message"""
    try:
        pygame.mixer.music.load(r"C:\Users\prade\OneDrive\Desktop\P3\calm_music.mp3.mp3")
        pygame.mixer.music.play()
        time.sleep(5)
        pygame.mixer.music.stop()
    except Exception as e:
        print("⚠️ Music file missing or error:", e)

last_emotion = ""

def send_command(emotion):
    """Send command to ESP32 + speak comfort + play music"""
    global last_emotion
    if emotion == last_emotion:
        return
    last_emotion = emotion
    cmd = emotion_to_command.get(emotion, "stop")
    try:
        requests.get(f"{ESP32_IP}/{cmd}", timeout=2)
        print(f"✅ Sent to ESP32: {cmd} ({emotion})")
    except Exception as e:
        print(f"❌ ESP32 unreachable: {e}")

    # Comfort message + music
    msg = COMFORT_MESSAGES.get(emotion, "Everything is okay.")
    print(f"💬 Comforting Message: {msg}")
    tts.say(msg)
    tts.runAndWait()
    play_music()

# Start webcam
cap = cv2.VideoCapture(0)
print("🎥 Starting webcam for emotion detection...")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype('float32') / 255.0
        roi = np.expand_dims(roi, axis=[0, -1])
        preds = model.predict(roi, verbose=0)
        emotion_label = emotion_labels[np.argmax(preds)]

        # Send ESP32 command and speak message
        send_command(emotion_label)

        # Draw emotion box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, emotion_label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Emotion-Based Robot", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
