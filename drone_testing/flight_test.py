import sys
sys.path.append("..")
from pixhawk import PixHawk
from time import sleep

sleep(30)

pixhawk = PixHawk(min_altitude=2, max_altitude=10,
                  boundary_circle=True, boundary_radius=10)

try:
    print("Setting Guided")
    pixhawk.set_guided_mode()

    print("Take off")
    pixhawk.takeoff()
    sleep(5)

    print("Loiter")
    pixhawk.set_loiter_mode()
    sleep(5)

    print("Setting Guided")
    pixhawk.set_guided_mode()

    print("Move 1m north and 1m east")
    pixhawk.move_relative(1, 1)
    sleep(5)

    print("Move 1m south")
    pixhawk.move_relative(-1, 0)
    sleep(5)

    print("Returning home")
    pixhawk.return_home()
    sleep(5)

    print("Land")
    pixhawk.land()
    sleep(5)
except:
    pixhawk.close_connection()
