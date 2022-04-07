from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal
import serial
import time
import math


class PixHawk:

    def __init__(self, connection_port="/dev/ttyACM0", baud_rate=115200,
                 min_altitude=30, max_altitude=50,
                 boundary_circle=True, boundary_radius=1000,
                 boundary_square=None,
                 home_longitude=None, home_latitude=None):
        """

        Args:
            connection_port:
            baud_rate:
            min_altitude:
            max_altitude:
            boundary_circle:
            boundary_radius:
            boundary_square:
            home_longitude:
            home_latitude:
        """
        # target altitude = min + 10?
        # borders of where not to go, if none specified, can
        #   specify a 30min radius or square around launch location
        # takeoff position

        self.port = connection_port
        self.baud_rate = baud_rate

        if min_altitude < max_altitude:
            self.min_altitude = min_altitude
            self.altitude = min_altitude + 5
            self.max_altitude = max_altitude
        else:
            print("Altitude levels incorrectly set")
            raise ValueError

        self.boundary_circle = boundary_circle
        self.boundary_radius = boundary_radius
        self.boundary_square = boundary_square

        print("Connecting to drone")
        self.vehicle = connect(connection_port, baud=baud_rate, wait_ready=True)

        print("Downloading commands")
        self.commands = self.vehicle.commands
        self.commands.download()
        self.commands.wait_ready()

        if home_longitude and home_latitude:
            self.set_home_position()

        # Save original location
        self.original_longitude = self.vehicle.location.global_frame.lon
        self.original_latitude = self.vehicle.location.global_frame.lat

        while not self.vehicle.is_armable:
            print("Waiting for drone to initialize...")
            time.sleep(1)

    def set_guided_mode(self):
        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)

        while self.vehicle.mode != VehicleMode("GUIDED"):
            self.vehicle.mode = VehicleMode("GUIDED")
            time.sleep(0.5)

    def takeoff(self):
        if not self.check_within_boundaries():
            print("Unable to takeoff, check boundary conditions")
            return

        # Confirm ready to take off
        while not self.vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)

        print("Taking Off")
        self.vehicle.simple_takeoff(self.altitude)

        while True:
            alt = self.vehicle.location.global_relative_frame.alt
            print(f"Current Altitude: {alt}")
            # if alt >= self.altitude - 1.0:
            if alt >= self.altitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def check_within_boundaries(self):
        if self.boundary_circle:
            # Defined radius around original location

            # Get current location
            curr_long = self.vehicle.location.global_frame.lon
            curr_lat = self.vehicle.location.global_frame.lat

            # Find distance between original and current
            distance_from_orig = get_distance_metres(curr_long, curr_lat,
                                                     self.original_longitude,
                                                     self.original_latitude)

            # Compare with set radius
            if distance_from_orig < self.boundary_radius:
                return True
            else:
                return False
        else:
            # Given square boundaries list, check current position is within
            # 4 coordinates

            return True

    def set_home_position(self):
        # If the variable can potentially change on the vehicle
        # Need to re-download the Vehicle.commands to confirm the value.
        # Get Vehicle Home location is `None` until first set by autopilot
        while not self.vehicle.home_location:
            cmds = self.vehicle.commands
            cmds.download()
            cmds.wait_ready()
            if not self.vehicle.home_location:
                print("Waiting for home location...")

        # We have a home location.
        print(f"Current Home position: {self.vehicle.home_location}")

        print("Setting Home position")
        self.vehicle.home_location = self.vehicle.location.global_frame

        print(f"New Home Location: {self.vehicle.home_location}")

    def return_home(self):
        self.vehicle.mode = VehicleMode("RTL")

    def set_loiter_mode(self):
        pass

    def move(self, latitude, longitude):
        print(f"Moving to latitude: {latitude}, longitude: {longitude}")
        new_loc = LocationGlobal(latitude, longitude)
        self.vehicle.simple_goto(new_loc)

    def change_altitude(self):
        pass

    def land(self):
        self.vehicle.mode = VehicleMode("LAND")


def get_distance_metres(loc_1_long, loc_1_lat, loc_2_long, loc_2_lat):
    """
    Returns the distance in metres between two LocationGlobal objects.
    Adapted from:
    https://github.com/tizianofiorenzani/how_do_drones_work/

    Args:
        loc_1_long:
        loc_1_lat:
        loc_2_long:
        loc_2_lat:

    Returns:

    """
    delta_lat = loc_2_lat - loc_1_lat
    delta_long = loc_2_long - loc_1_long
    return math.sqrt((delta_lat ** 2) + (delta_long ** 2)) * 1.113195e5


def check_within_square(lst_lat_long, curr_lat, curr_long):
    # 4 coordinates of (lat, long)
    # Assume square box
    # x1,y1       x2,y2
    #
    #
    # x3,y3       x4,y4
    long_lst = []
    lat_lst = []
    for coord in lst_lat_long:
        lat_lst.append(coord[0])
        long_lst.append(coord[1])

    # Get min max of each to get bounds of boundary
    lat_min = min(lat_lst)
    lat_max = max(lat_lst)
    long_min = min(long_lst)
    long_max = max(long_lst)

    # TODO: Compare current position to bounds

