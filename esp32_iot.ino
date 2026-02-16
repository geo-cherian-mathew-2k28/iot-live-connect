#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
#include "DHT.h"

// --- CONFIGURATION ---
const char* ssid = "Mullananickal KvFi";
const char* password = "geo@6756";
const char* serverName = "https://atomic-maryjo-cropstack-2280857f.koyeb.app/sensor";

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
WiFiClientSecure client; // Persistent client
HTTPClient http;

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  Serial.println("\nWiFi connected");
  
  client.setInsecure(); // Persistent setting
  http.setTimeout(10000); // 10-second timeout to prevent 'Read Timeout'
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    if (isnan(h) || isnan(t)) {
      Serial.println("Failed to read from DHT sensor!");
    } else {
      StaticJsonDocument<200> doc;
      doc["temperature"] = t;
      doc["humidity"] = h;

      String jsonString;
      serializeJson(doc, jsonString);

      Serial.print("Real-time Sending: ");
      Serial.println(jsonString);

      // Re-using the http object with keep-alive
      http.begin(client, serverName);
      http.addHeader("Content-Type", "application/json");
      http.addHeader("X-API-KEY", "iot_secure_key_2024_v1");
      http.addHeader("Connection", "keep-alive"); // Professional keep-alive

      int httpResponseCode = http.POST(jsonString);

      if (httpResponseCode > 0) {
        Serial.print("Server Received Data! Code: ");
        Serial.println(httpResponseCode);
      } else {
        Serial.print("Connection/Timeout Error: ");
        Serial.println(http.errorToString(httpResponseCode).c_str());
        // If timeout happens, the data might still have reached the server!
      }
      http.end(); // Clean up current request but keep hardware radio ready
    }
  } else {
    Serial.println("WiFi Disconnected! Reconnecting...");
    WiFi.begin(ssid, password);
  }
  delay(3000); // 3-second sync for true real-time
}
