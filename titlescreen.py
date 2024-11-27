import pygame
import sys

def title_screen(screen, font, clock):
    screen.fill("black")
    title_text = font.render("Unfair Pong", True, "white")
    instructions_text = font.render("press space to START", True, "white")

    title_rect = title_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3))
    instructions_rect = instructions_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

        clock.tick(60)