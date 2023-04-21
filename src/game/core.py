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
            
            get_current_state().process_event(event)

        pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")
        get_current_state().update(delta_time_seconds)
        get_current_state().render(__display)
        pygame.display.update()

def register_state(name: str, state_object: states.GameState):
    global __states
    
    if name in __states:
        raise KeyError(f"Um state já foi registrado com o nome \"{name}\".")
    
    __states[name] = state_object
    
def push_state(name: str):
    global __state_stack
    
    if not name in __states:
        raise KeyError(f"Nenhum state foi registrado com o nome \"{name}\".")
    
    __state_stack.append(__states[name])

def pop_state():
    global __state_stack
    
    if __state_stack:
        __state_stack.pop()

def get_current_state():
    try:
        return __state_stack[-1]
    except IndexError:
        return None

__display = pygame.display.set_mode(const.WINDOW_SIZE)
__clock = pygame.time.Clock()

pygame.display.set_icon(pygame.Surface((0, 0)))
pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")

__states = {}
__state_stack = []
