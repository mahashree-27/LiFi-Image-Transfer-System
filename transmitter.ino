#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "Galaxy A04e 6648";
const char* password = "Susanthmk";

// Updated Dropbox direct download link
const char* dropboxFileURL = "https://dl.dropboxusercontent.com/scl/fi/0wi7agjqbx3wwu96eptfg/MyProject.txt?rlkey=z9fgxpet3jd3t03aslk1ztdx0&st=zvgqztx5&dl=1";

const int laserPin = 26;
const int oneDelay = 150;   // Duration for sending '1'
const int zeroDelay = 50;   // Duration for sending '0'
const int gapDelay = 30;    // Gap after each bit

void setup() {
  Serial.begin(115200);
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW);

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");

  sendBitstreamFromDropbox();
}

void loop() {
  // Nothing here
}

void sendBitstreamFromDropbox() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(dropboxFileURL);

    int httpCode = http.GET();
    if (httpCode == 200) {
      String bitstream = http.getString();
      Serial.println("Bitstream received. Transmitting...");

      for (int i = 0; i < bitstream.length(); i++) {
        char bit = bitstream.charAt(i);
        if (bit == '1') {
          digitalWrite(laserPin, HIGH);
          delay(oneDelay);
          digitalWrite(laserPin, LOW);
        } else if (bit == '0') {
          digitalWrite(laserPin, LOW);
          delay(zeroDelay);
        }
        delay(gapDelay); // small gap between bits
      }

      Serial.println("Transmission complete.");
      digitalWrite(laserPin, LOW);
    } else {
      Serial.printf("Failed to fetch file. HTTP error code: %d\n", httpCode);
    }

    http.end();
  }
}
