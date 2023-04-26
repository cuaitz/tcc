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
        surface.fill("#181818")
        
        display = pygame.display.get_surface()
        surface.fill(
            "#232323", 
            pygame.Rect(
                20, 
                20, 
                display.get_width() - 20 * 2,
                display.get_height() - 20 * 2
            )
        )
        
        texts = [_gameover_text, _continue_text]
        height = 50
        for text in texts:
            surface.blit(text, (surface.get_width() / 2 - text.get_width() / 2, height))
            height += 5 + text.get_height()


font_big = pygame.font.Font(None, 50)
font_normal = pygame.font.Font(None, 25)

_gameover_text = font_big.render("BallFall", True, "#eeeeee")
_continue_text = font_normal.render("Pressione \"R\" para jogar", True, "#eeeeee")
