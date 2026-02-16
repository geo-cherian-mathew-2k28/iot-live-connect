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

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;
    client.setInsecure(); // Important for Cloud deployment certificates
    
    HTTPClient http;
    http.setTimeout(10000); // Increase timeout for cloud response

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

      Serial.print("Sending: ");
      Serial.println(jsonString);

      http.begin(client, serverName);
      http.addHeader("Content-Type", "application/json");
      http.addHeader("X-API-KEY", "iot_secure_key_2024_v1"); // Security Header

      int httpResponseCode = http.POST(jsonString);

      if (httpResponseCode > 0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
      } else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
    }
  }
  delay(5000);
}
