import simpleaudio as sa
from time import sleep


def countdown(time):
    wave_obj = sa.WaveObject.from_wave_file("../sounds/beep.wav")
    count = 0
    while count < time:
        play_obj = wave_obj.play()
        sleep(1)
        play_obj.wait_done()
        count += 1
