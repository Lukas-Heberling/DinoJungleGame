import pygame

# This is a help package with helpful functions to facilitate the programming of a game ;)
# TODO add the calculation of jumping!


def showtext(screen, text, x, y, fontSize):
    # Display Text on Screen
    font = pygame.font.Font(None, fontSize)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def drawOnScreen(screen, picture, x, y):
    # Draw Images on the screen
    screen.blit(picture, (x, y))
