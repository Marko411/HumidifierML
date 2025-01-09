# HumidifierML

## 
The **ESP-32 Based ML Humidifier** is an IoT device designed to optimize room humidity levels using machine learning. By integrating **TensorFlow Lite for Microcontrollers**, the system is able to operate autonomously to maintain comfortable humidity levels without excessive strain on the components or hardware.

## Features
- **Machine Learning:**
  - A lightweight binary classification neural network achieves over 80% accuracy in controlling humidity. 
- **Efficient Water Atomization:**
  - Custom circuit drives two motors which feature a centrifugal disc, humidifying 50% faster than standard ultrasonic units.
- **Real Time Monitoring**
  - The current sensor readings and the ML prediction are displayed on the serial monitor. 

The system consists of the following major components:
1. **Sensors:**
   - Humidity and temperature sensors to monitor room conditions.
2. **Actuators**
   - Centrifugal atomizer controlled with a MOSFET driver circuit and powered by DC motors.
3. **Processing Unit:**
   - ESP-32 running the TensorFlow Lite ML model deployed as a C array into the Arduino IDE.
4. **PCB**
   - PCB designed for compactness which also features a switch if the user chooses to control the humidifier manually. 

