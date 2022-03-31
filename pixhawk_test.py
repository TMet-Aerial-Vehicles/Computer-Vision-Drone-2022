from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

port = "/dev/ttyACM0"
baud_rate = 115200

vehicle = connect(port, baud=baud_rate, wait_ready=True)

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

def arm_and_takeoff(tgt_altitude):
    print("Arming motors")

    while not vehicle.is_armable:
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed: time.sleep(1)

    print("Takeoff")
    vehicle.simple_takeoff(tgt_altitude)

    #-- wait to reach the target altitude
    while True:
        altitude = vehicle.location.global_relative_frame.alt

        if altitude >= tgt_altitude -1:
            print("Altitude reached")
            break

        time.sleep(1)


#------ MAIN PROGRAM ----
arm_and_takeoff(10)

#-- set the default speed
vehicle.airspeed = 7

#-- Go to position
print ("Moving to Position 1")
wp1 = LocationGlobalRelative(35.9872609, -95.8753037, 10)

vehicle.simple_goto(wp1)

time.sleep(30)

#--- Coming back
print("Coming back")
vehicle.mode = VehicleMode("RTL")

time.sleep(20)

#-- Close connection
vehicle.close()
