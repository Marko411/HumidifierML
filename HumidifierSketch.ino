#include <Arduino.h>
#include "DHT.h"

#include <MicroTFLite.h>
#include "humidifierMLVer2.h" 

const int vrx = 34;  
const int vry = 35;  
const int sw  = 32;  

const int motor1Pin = 25;
const int motor2Pin = 26;
const int motor3Pin = 27;

#define DHTPIN  33
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

#define HUMIDITY_MEAN 36.1823f
#define HUMIDITY_STD  10.5734f

constexpr int tensorArenaSize = 4 * 1024;  //4kb, should be enough as the C array is 2.7kb
alignas(16) byte tensorArena[tensorArenaSize];

void setup() {
  Serial.begin(115200);

  pinMode(sw, INPUT_PULLUP); //this is HIGH when it is not pressed

  pinMode(motor1Pin, OUTPUT);
  digitalWrite(motor1Pin, LOW);
  pinMode(motor2Pin, OUTPUT);
  digitalWrite(motor2Pin, LOW);
  pinMode(motor3Pin, OUTPUT);
  digitalWrite(motor3Pin, LOW);

  dht.begin();

  Serial.println("\nStarting the ML model");
  if (!ModelInit(humidifierMl1, tensorArena, tensorArenaSize)) {
    Serial.println("Error likely due to memory issue");
    while (true) {

    }
  }
  Serial.println("ML model initialized successfully.");
  
  delay(1000);
}

void loop() {

  int x = analogRead(vrx);  //0 to 4095
  int y = analogRead(vry);  
  int buttonState = digitalRead(sw);

  float humidity    = dht.readHumidity();
  float temp = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Sensor error");
  } else {

    //Serial.print("X: ");   Serial.print(x);
  //  Serial.print(" | Y: ");   Serial.print(y);
    Serial.print(" | Button: ");
    Serial.print(buttonState == LOW ? "Pressed" : "Released");
    Serial.print(" | Humidity: ");   Serial.print(humidity);   Serial.print(" %");
    //Serial.print(" | Temperature: ");Serial.print(temp);Serial.println(" *C");
  }


  if (buttonState == LOW) {

    if (x <= 50) {

      digitalWrite(motor1Pin, HIGH);
      digitalWrite(motor2Pin, LOW);
      digitalWrite(motor3Pin, LOW);
    }
    else if (x >= 4000) {

      digitalWrite(motor2Pin, HIGH);
      digitalWrite(motor3Pin, HIGH);
      digitalWrite(motor1Pin, LOW);
    }
    else {

      digitalWrite(motor1Pin, LOW);
      digitalWrite(motor2Pin, LOW);
      digitalWrite(motor3Pin, LOW);
    }
  } 
  else {

    if (!isnan(humidity)) {
      float scaledHumidity = (humidity - HUMIDITY_MEAN) / HUMIDITY_STD;

      ModelSetInput(scaledHumidity, 0);

      if (!ModelRunInference()) {
        Serial.println("No prediction from ML model");
      } else {
        float prediction = ModelGetOutput(0);
        
        Serial.print("  >> ML Prediction: ");
        Serial.println(prediction);

        if (prediction >= 0.5f) {
          digitalWrite(motor2Pin, HIGH);
          digitalWrite(motor3Pin, HIGH);
        } else {
          digitalWrite(motor2Pin, LOW);
          digitalWrite(motor3Pin, LOW);
        }
      }

      digitalWrite(motor1Pin, LOW);
    }
  }

  delay(200);
}
