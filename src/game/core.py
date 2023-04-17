import pygame

from . import const
from . import game

__display = pygame.display.set_mode(const.__WINDOW_SIZE)
__clock = pygame.time.Clock()

pygame.display.set_icon(pygame.Surface((0, 0)))
pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")

def update(delta_time_seconds: float):
    pygame.display.set_caption(f"FPS: {round(__clock.get_fps(), 2)}")
    game.update(delta_time_seconds)
    

def render(surface: pygame.Surface):
    surface.fill("#232323")
    game.render(surface)

def loop():
    while not const.__OVER:
        delta_time_seconds: int = const.__TARGET_FPS * __clock.tick(const.__TARGET_FPS) / 1000
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_w:
                    game.spawn_target()
                elif event.key == pygame.K_a:
                    game.decrease_level()
                elif event.key == pygame.K_d:
                    game.increase_level()

        update(delta_time_seconds)
        render(__display)
        pygame.display.update()
        