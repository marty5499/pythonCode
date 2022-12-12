from dfplayermini import Player
from time import sleep

music = Player()
music.volume(15)
music.play(1)
sleep(5)
music.stop()
