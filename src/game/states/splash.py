import pygame

from .. import core
from . import state


class SplashState(state.GameState):
    def process_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                core.push_state('playing')
    
    def update(self, delta_time_seconds: float):
        pass
    
    def render(self, surface: pygame.Surface):
        surface.fill("#232323")
        
        texts = [_gameover_text, _continue_text]
        height = 50
        for text in texts:
            surface.blit(text, (surface.get_width() / 2 - text.get_width() / 2, height))
            height += 5 + text.get_height()


font_big = pygame.font.Font(None, 50)
font_normal = pygame.font.Font(None, 25)

_gameover_text = font_big.render("BallFall", True, "#eeeeee")
_continue_text = font_normal.render("Pressione \"R\" para jogar", True, "#eeeeee")
