from . import core
from . import states

core.register_state('playing', states.playing_state)
core.push_state('playing')
core.loop()
