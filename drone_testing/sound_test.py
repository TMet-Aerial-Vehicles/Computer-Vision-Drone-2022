# from pygame import mixer
#
# mixer.init()
# # alert=mixer.Sound('../sounds/beep.wav')
# mixer.music.load('../sounds/beep.wav')
# mixer.music.play()
# mixer.music.play()
# mixer.music.play()
# mixer.music.play()
# mixer.music.play()
# alert.play()


# from beepy import beep
#
# beep(sound="ready")
# beep(sound="ready")
# beep(sound="ready")
# beep(sound="ready")

import simpleaudio as sa
from time import sleep

wave_obj = sa.WaveObject.from_wave_file("../sounds/beep.wav")
play_obj = wave_obj.play()
sleep(1)
play_obj.wait_done()
play_obj = wave_obj.play()
sleep(1)
play_obj.wait_done()

from sound import play_quick_sound
play_quick_sound(5)

