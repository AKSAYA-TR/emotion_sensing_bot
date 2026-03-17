#include <WiFi.h>
#include <WebServer.h>

// Wi-Fi credentials
const char* ssid = "$$$$";
const char* password = "Enter_ypur_password";

// Web server on port 80
WebServer server(80);

// Motor driver pins
#define IN1 14
#define IN2 27
#define IN3 26
#define IN4 25
#define ENA 12
#define ENB 13

void setup() {
  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

  stopBot();

  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to WiFi!");
  Serial.print("📡 IP Address: ");
  Serial.println(WiFi.localIP());

  // Define all emotion-based routes
  server.on("/circle", spinCircle);
  server.on("/slowforward", moveSlowForward);
  server.on("/shake", shakeBot);
  server.on("/backstop", backStop);
  server.on("/stop", stopBot);

  server.begin();
  Serial.println("🌐 HTTP server started");
}

void loop() {
  server.handleClient();
}

// ===== Movements =====

// Happy → Spin in circle
void spinCircle() {
  Serial.println("😊 HAPPY: Spinning in circle");
  for (int i = 0; i < 2; i++) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    analogWrite(ENA, 255);
    analogWrite(ENB, 255);
    delay(1000);
  }
  stopBot();
  server.send(200, "text/plain", "Circle spin done");
}

// Sad → Move slowly forward
void moveSlowForward() {
  Serial.println("😢 SAD: Moving slowly forward");
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 120);
  analogWrite(ENB, 120);
  delay(1500);
  stopBot();
  server.send(200, "text/plain", "Slow forward done");
}

// Angry → Shake back and forth rapidly
void shakeBot() {
  Serial.println("😡 ANGRY: Shaking rapidly");
  for (int i = 0; i < 4; i++) {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3, LOW);
    digitalWrite(IN4, HIGH);
    delay(200);
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    delay(200);
  }
  stopBot();
  server.send(200, "text/plain", "Shake done");
}

// Surprised → Move backward quickly then stop
void backStop() {
  Serial.println("😮 SURPRISED: Moving back quickly and stop");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 255);
  analogWrite(ENB, 255);
  delay(700);
  stopBot();
  server.send(200, "text/plain", "Backstop done");
}

// Neutral → Stay still
void stopBot() {
  Serial.println("🛑 STOP: Neutral or idle");
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
  server.send(200, "text/plain", "Stopped");
}
