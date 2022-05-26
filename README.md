# Toronto Metropolitan Aerial Vehicles (formally RUAV)

This repository contains source code used for drone flight and computer vision 
detection, executed on a Raspberry Pi

## Description

The code in this repository is used to control quadcopter drones using mavlink 
connection through dronekit. It additionally contains code for creating and 
reading QR codes, along with the ability to map the drone's path and export
its binary files into csv. In progress is person detection, tracking, and 
mapping from a drone.

## Dependencies

* Python 3.6+
* The required dependencies are included in the requirements.txt file

## Installing

Install the required Python dependencies using:
```commandline
pip install -r requirements.txt
```

## Executing program

* To run the main script, which reads a QR, flies to the given longitude and 
latitude position, and then starts its person detection:
```
python main.py
```

## Creating a Script

* Important imports:
  * For standardized logging across different scripts:
  ```python
  import logging
  from logging_script import start_logging
  start_logging()
  ```
  * For drone control and connection:
  ```python
  from pixhawk import Pixhawk
  ```
  * For sound notifications:
  ```python
  from sound import countdown, play_quick_sound
  ```
For method utilization, see main.py and backup.py
  


## Authors

* [Craig Pinto](https://github.com/CraigP17)  

## File Structure

* drone_testing/: testing scripts for different components
  * depthai_yolo_test.py: Detection using YOLO through DepthAI camera
  * flight_test.py: Flight test for drone, testing movement
  * pixhawk_test.py: Drone connection test 
  * ryerson_test.py: Flight test dor drone, testing rotation 
  * sound_test.py: Sound test 
  * stabilize_test.py: Stabilize mode test
  * video_test.py: Video recording from input camera test
* gps_log_extraction/
  * gps_plotter.py: Plots longitude, latitude coordinates onto a given map
  * mavlogdump.py: Converts drone bin log file into csv 
* images/
* models/: ML Detection models
* qr/
  * qr_creator.py: Creates QR codes
  * qr_reader.py: Reads QR and decodes into given competition format
* sampleQR/
  * Sample competition QR codes
* sounds/
* venv/
* videos/
* backup.py: Contains QR reading, drone flight, and video recording
* calculations.py: Methods for calculating position
* logging_script: Logging method to standardize logging to the same file
* detection.py: Detection class using HOG
* main.py: Encapsulates entire sequence with reading QR, controlling drone, person detection (Incomplete)
* pixhawk.py: Pixhawk class with methods to control drone flight
* requirements.txt: Package dependencies
* serial_communication: Serial Port communication to Arduino
* sound.py: Methods for playing sound files

## Acknowledgements

* [GPS Visualization](https://github.com/tisljaricleo/GPS-visualization-Python)
* [ArduPilot Pymavlink](https://github.com/ArduPilot/pymavlink/blob/master/tools/mavlogdump.py)
* [Dronekit](https://github.com/dronekit/dronekit-python)
