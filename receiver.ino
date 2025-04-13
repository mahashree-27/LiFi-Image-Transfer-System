const int sensorPin = A0;     // Photodiode connected to analog pin A0
const int threshold = 600;    // Threshold for detecting laser light
String receivedBits = "";     // Store received bits

unsigned long lastReadTime = 0;
const unsigned long readInterval = 500;  // Adjust based on sender timing (ms)

void setup() {
  Serial.begin(9600);
  pinMode(sensorPin, INPUT);
  Serial.println("Waiting for initial laser pulse to sync...");

  // Wait for the laser to turn ON (rising edge):
  while (analogRead(sensorPin) <= threshold) {
    // Do nothing until a laser pulse is detected
    delay(10);
  }
  
  Serial.println("Laser pulse detected. Waiting for laser to turn OFF to start reading...");

  // Now wait for the laser to turn OFF (falling edge):
  while (analogRead(sensorPin) > threshold) {
    delay(10);
  }
  
  Serial.println("Laser pulse has ended. Starting to receive bits...");
  
  // Initialize lastReadTime after sync
  lastReadTime = millis();
}

void loop() {
  unsigned long currentTime = millis();
  
  // Read periodically, based on the expected bit duration
  if (currentTime - lastReadTime >= readInterval) {
    lastReadTime = currentTime;
    int sensorValue = analogRead(sensorPin);

    if (sensorValue > threshold) {
      receivedBits += '1';
      Serial.print('1');
    } else {
      receivedBits += '0';
      Serial.print('0');
    }
  }

  // Optional: When a certain length is reached, stop reading
  if (receivedBits.length() >= 8000) {  // Adjust as needed for your application
    Serial.println("\nDone receiving.");
    while (1);  // Stop execution
  }
}
