import pygame

from . import const
from . import states

def loop():
    while not const.OVER:
        delta_time_seconds: int = const.TARGET_FPS * __clock.tick(const.TARGET_FPS) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            
            __current_state.process_event(event)

        pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")
        __current_state.update(delta_time_seconds)
        __current_state.render(__display)
        pygame.display.update()

def push_state(state_object: states.GameState):
    global __states
    
    if not isinstance(state_object, states.GameState):
        raise TypeError(f"Tipo incorreto. Esperado: {states.GameState} | Recebido: {type(state_object)}.")

    __states.append(state_object)
    _update_state()

def pop_state():
    global __states
    
    if __states:
        __states.pop()
        _update_state()

def _update_state():
    global __current_state
    
    try:
        __current_state = __states[-1]
    except IndexError:
        __current_state = None

def get_current_state():
    return __current_state

__current_state: states.GameState = None

__display = pygame.display.set_mode(const.WINDOW_SIZE)
__clock = pygame.time.Clock()

pygame.display.set_icon(pygame.Surface((0, 0)))
pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")

__states = []
