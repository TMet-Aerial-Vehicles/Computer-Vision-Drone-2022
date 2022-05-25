# Toronto Metropolitan Aerial Vehicles (formally RUAV)

This repository contains source code used for drone flight and computer vision 
detection, executed on a Raspberry Pi

## Description

The code in this repository is used to control quadcopter drones using mavlink 
connection through dronekit. It additionally contains code for creating and 
reading QR codes, along with the ability to map the drone's path and export
its binary files into csv. In progress is person detection, tracking, and 
mapping from a drone.

### Dependencies

* Python 3.6+
* The required dependencies are included in the requirements.txt file

### Installing

Install the required Python dependencies using:
```commandline
pip install -r requirements.txt
```

### Executing program

* To run the main script, which reads a QR, flies to the given longitude and 
latitude position, and then starts its person detection:
```
python main.py
```

## Authors

* [Craig Pinto](https://github.com/CraigP17)  

### File Structure
