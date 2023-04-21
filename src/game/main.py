from . import core
from . import states

core.register_state('splash', states.splash_state)
core.register_state('playing', states.playing_state)
core.register_state('gameover', states.gameover_state)
core.push_state('splash')
core.loop()
