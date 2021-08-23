from os import supports_effective_ids
import pygame
import random
import sys

from pygame import color

# Game made by ~lukas Heberling
# Hope you enjoy!
# I will try to document as much as i can but i also have to figure out python to myself XD
# Im writing this game during my Summerbreak from work
# Sooo i dont't know if i will have enought time XD


# Dino images(vita) by Arks
# https://arks.itch.io/dino-characters
# @ScissorMarks

# CONSTANT VARIABLES
screenSize = (700, 700)
# colors
colors = {
    "darkGrey": (50, 50, 50),
    "paleYellow": (203, 219, 29),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "neonGreen": (37, 247, 30),
}


# INIT
pygame.init()
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("RunningHolliday ~Lukas")

# DisplayText


def showtext(text, x, y, fontSize):
    font = pygame.font.Font(None, fontSize)
    text_surface = font.render(text, True, colors["white"])
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Getting the MAp


def getGameMap(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


class mainClass():
    def __init__(self):
        # MAP
        self.map = getGameMap("Level1")
        self.scroll = [0, 0]
        self.mapScroll = [0, 0]
        self.tiles = {
            "down": pygame.image.load('Graphics/Tiles/Down.png').convert(),
            "left": pygame.image.load('Graphics/Tiles/Left.png').convert(),
            "right": pygame.image.load('Graphics/Tiles/Right.png').convert(),
            "up": pygame.image.load('Graphics/Tiles/Up.png').convert(),
            "no": pygame.image.load('Graphics/Tiles/No.png').convert(),
            "downLeft": pygame.image.load('Graphics/Tiles/downLeft.png').convert(),
            "downRight": pygame.image.load('Graphics/Tiles/DownRight.png').convert(),
            "upLeft": pygame.image.load('Graphics/Tiles/UpLeft.png').convert(),
            "upRight": pygame.image.load('Graphics/Tiles/UpRight.png').convert(),
        }
        # Some layers to create the Background
        self.layers = [
            [pygame.image.load(
                'Graphics/Background/Layers/1.png').convert_alpha(), 0.1],
            [pygame.image.load(
                'Graphics/Background/Layers/2.png').convert_alpha(), 0.2],
            [pygame.image.load(
                'Graphics/Background/Layers/3.png').convert_alpha(), 0.3],
            [pygame.image.load(
                'Graphics/Background/Layers/4.png').convert_alpha(), 0.4],
            [pygame.image.load(
                'Graphics/Background/Layers/5.png').convert_alpha(), 0.5],
        ]
        self.tileHeight = 32

        # Player
        self.playerX = 350
        self.playerY = -200
        self.playerWidth = 40
        self.playerHeight = 50
        self.speed = 5
        # Player jump
        self.jumpvar = 0
        self.velocityDown = 3
        self.jump = False
        # Player Vita
        self.vita = pygame.image.load(
            'Graphics/Vita/vita_00.png').convert_alpha()

    def drawTile(self, tile, x, y):
        # Drawing the Blocks of the map
        screen.blit(
            tile,
            (
                x * self.tileHeight - self.scroll[0],
                y * self.tileHeight - self.scroll[1]
            )
        )

    def drawLayers(self):
        # Drawing the layers of the Background
        #  screen.blit(self.layers["3"][0],
        #             (-150 - self.scroll[0] * self.layers["3"][1], 0))
        for layer in self.layers:
            screen.blit(
                layer[0],
                (
                    -150 - self.scroll[0] * layer[1],
                    0
                )
            )

    def drawMap(self):
        # true_scroll[0] += (player_rect.x-true_scroll[0]-152)/20
        # Calc scroll player movement
        self.mapScroll[0] += (self.playerX - self.mapScroll[0]-330)/15
        self.mapScroll[1] += (self.playerY - self.mapScroll[1]-310)/15
        self.scroll = self.mapScroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])
        # Drawing the map
        # This function will take a lot of power
        self.drawLayers()

        y = 0
        for row in self.map:
            x = 0
            for block in row:
                if block != "0":
                    pygame.draw.rect(
                        screen,
                        colors["neonGreen"],
                        (
                            x * self.tileHeight - self.scroll[0],
                            y * self.tileHeight - self.scroll[1],
                            self.tileHeight,
                            self.tileHeight
                        )
                    )
                if block == "1":
                    self.drawTile(self.tiles["up"], x, y)
                if block == "2":
                    self.drawTile(self.tiles["down"], x, y)
                if block == "3":
                    self.drawTile(self.tiles["left"], x, y)
                if block == "4":
                    self.drawTile(self.tiles["right"], x, y)
                if block == "5":
                    self.drawTile(self.tiles["upLeft"], x, y)
                if block == "6":
                    self.drawTile(self.tiles["upRight"], x, y)
                if block == "7":
                    self.drawTile(self.tiles["downLeft"], x, y)
                if block == "8":
                    self.drawTile(self.tiles["downRight"], x, y)
                if block == "9":
                    self.drawTile(self.tiles["no"], x, y)
                x += 1
            y += 1

    # PLAYER
    def collide(self, newX, newY):
        collision = False
        # player rect
        playerRect = pygame.Rect(
            newX, newY, self.playerWidth, self.playerHeight)
        y = 0
        for row in self.map:
            x = 0
            for block in row:
                mapBlock = pygame.Rect(x*self.tileHeight,
                                       y*self.tileHeight,
                                       self.tileHeight,
                                       self.tileHeight
                                       )
                if mapBlock.colliderect(playerRect) and block != "0":
                    collision = True
                x += 1
            y += 1
        return collision

    def movePlayer(self, playerX, playerY):
        if not self.collide(playerX, playerY):
            self.playerX = playerX
            self.playerY = playerY

    def updatePlayer(self):
        # Getting the pressed key
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and not self.jump and self.collide(self.playerX, self.playerY + 1):
            self.jump = True
            self.jumpvar = 15
        elif pressed[pygame.K_LEFT]:
            self.movePlayer(self.playerX - self.speed, self.playerY)
        elif pressed[pygame.K_RIGHT]:
            self.movePlayer(self.playerX + self.speed, self.playerY)

        if not self.collide(self.playerX, self.playerY + self.velocityDown) and self.jumpvar == 0:
            self.playerY += self.velocityDown
            self.velocityDown += 0.5
        elif self.jumpvar == 0:
            self.velocityDown -= 1
        if self.jump and self.jumpvar > 0:
            if not self.collide(self.playerX, self.playerY - (self.jumpvar ** 2) * 0.17):
                self.playerY -= (self.jumpvar ** 2) * 0.17
            else:
                self.jumpvar = 0
                self.jump = False
            self.jumpvar -= 1
        if self.collide(self.playerX, self.playerY + 1):
            self.jumpvar = 0
            self.velocityDown = 3
            self.jump = False

    def drawPlayer(self):
        screen.blit(
            self.vita,
            (
                self.playerX - self.scroll[0] - 17,
                self.playerY - self.scroll[1] - 11
            )
        )


game = mainClass()
# Game Loop
while (1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(colors["black"])
    game.updatePlayer()
    game.drawMap()
    game.drawPlayer()
    pygame.display.flip()
    clock.tick(60)
