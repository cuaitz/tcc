import abc

import pygame


class GameState(abc.ABC):
    def process_event(self, event: pygame.event.Event):
        pass
    
    def update(self, delta_time_seconds: float):
        pass
    
    def render(self, surface: pygame.Surface):
        pass
