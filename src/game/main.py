from . import core
from . import states

core.push_state(states.playing_state)
core.loop()
