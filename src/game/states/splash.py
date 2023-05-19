import pygame

from .. import const
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
        surface.fill("#181818")
        surface.fill("#232323", const.GAME_AREA_RECT)
        
        texts = [_logo_text, _press_to_play_text]
        height = 50
        for text in texts:
            surface.blit(text, (const.GAME_AREA_RECT.centerx - text.get_width() / 2, height))
            height += 5 + text.get_height()


font_big = pygame.font.Font(None, 50)
font_normal = pygame.font.Font(None, 25)

_logo_text = font_big.render("BallFall", True, "#eeeeee")
_press_to_play_text = font_normal.render("Pressione \"R\" para jogar", True, "#eeeeee")
