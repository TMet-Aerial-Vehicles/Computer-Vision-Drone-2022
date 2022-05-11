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


def play_quick_sound(times):
    wave_obj = sa.WaveObject.from_wave_file("../sounds/beep.wav")
    count = 0
    while count < times:
        play_obj = wave_obj.play()
        sleep(0.25)
        play_obj.wait_done()
        count += 1
