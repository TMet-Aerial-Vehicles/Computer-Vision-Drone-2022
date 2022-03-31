from dronekit import connect, VehicleMode
import time

port = "/dev/ttyACM0"
baud_rate = 115200

vehicle = connect(port, wait_ready=True)

vehicle.wait_ready('autopilot_version')
print(f"Autopilot version: {vehicle.version}")

#- Does the firmware support the companion pc to set the attitude?
print(f"Supports set attitude from companion: {vehicle.capabilities.set_attitude_target_local_ned}")

#- Read the actual position
print(f"Position: {vehicle.location.global_relative_frame}")

#- Read the actual attitude roll, pitch, yaw
print(f"Attitude: {vehicle.attitude}")

#- Read the actual velocity (m/s)
print(f"Velocity: {vehicle.velocity}") #- North, east, down

#- When did we receive the last heartbeat
print(f"Last Heartbeat: {vehicle.last_heartbeat}")

#- Is the vehicle good to Arm?
print(f"Is the vehicle armable: {vehicle.is_armable}")

#- Which is the total ground speed?   Note: this is settable
print(f"Groundspeed: {vehicle.groundspeed}")

#- What is the actual flight mode?    Note: this is settable
print(f"Mode: {vehicle.mode.name}")

#- Is the vehicle armed               Note: this is settable
print(f"Armed: {vehicle.armed}")

#- Is thestate estimation filter ok?
print("EKF Ok: {vehicle.ekf_ok}")
