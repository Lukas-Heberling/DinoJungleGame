from os import supports_effective_ids
import pygame
import random
import sys
from pygame.locals import *

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


def showtext(text, x, y, fontSize):
    # Display Text on Screen
    font = pygame.font.Font(None, fontSize)
    text_surface = font.render(text, True, colors["white"])
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)


def drawOnScreen(picture, x, y):
    # Draw Images on the screen
    screen.blit(picture, (x, y))


def getGameMap(path):
    # Building the Map out of the Level.txt file
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
        self.playerX = 50
        self.playerY = -200
        self.playerWidth = 40
        self.playerHeight = 50
        self.speed = 5
        # Player jump
        self.jumpvar = 0
        self.velocityDown = 3
        self.jump = False
        # Player Vita
        self.runAnimation = 0
        self.idleAnimation = 0
        # direction = [walkRight, walkLeft, Jump, stand]
        # TODO mayby add the ability to duck ...
        self.direction = [0, 0, 0, 1]
        self.vitaRunRight = [
            pygame.image.load('Graphics/Vita/vita_05.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_06.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_07.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_08.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_09.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_10.png').convert_alpha(),
        ]
        self.vitaRunLeft = [
            pygame.image.load('Graphics/Vita/vita_05left.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_06left.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_07left.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_08left.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_09left.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_10left.png').convert_alpha(),
        ]
        self.vitaIdle = [
            pygame.image.load('Graphics/Vita/vita_00.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_01.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_02.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_03.png').convert_alpha(),
            pygame.image.load('Graphics/Vita/vita_04.png').convert_alpha(),
        ]

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
            drawOnScreen(layer[0], -150 - self.scroll[0] * layer[1], 0)

    def drawMap(self):
        # Calc scroll player movement
        # Scrolling ist the Value that the tiles move so the player is standing in the middle of the screen
        self.mapScroll[0] += (self.playerX - self.mapScroll[0]-330) / 15
        self.mapScroll[1] += (self.playerY - self.mapScroll[1]-310) / 15
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
        # Checking if the player is colliding with the world
        collision = False
        # player rect
        playerRect = pygame.Rect(
            newX, newY, self.playerWidth, self.playerHeight)
        y = 0
        for row in self.map:
            x = 0
            for block in row:
                mapBlock = pygame.Rect(
                    x*self.tileHeight, y*self.tileHeight, self.tileHeight, self.tileHeight)
                if mapBlock.colliderect(playerRect) and block != "0":
                    collision = True
                x += 1
            y += 1
        return collision

    def movePlayer(self, playerX, playerY):
        if not self.collide(playerX, playerY):
            self.playerX = playerX
            self.playerY = playerY

    def resetPLayer(self):
        self.playerX = 50
        self.playerY = -150

    def setDirection(self, direction):
        self.direction = direction

    def updatePlayer(self):
        # Getting the pressed key
        pressed = pygame.key.get_pressed()
        self.direction = [0, 0, 0, 1]
        self.idleAnimation += 1
        # Set the Variables to initialize a jump
        if pressed[pygame.K_UP] and not self.jump and self.collide(self.playerX, self.playerY + 1):
            self.direction = [0, 0, 1, 0]
            self.jump = True
            self.jumpvar = 15
        # Moving the player left
        elif pressed[pygame.K_LEFT]:
            self.direction = [0, 1, 0, 0]
            self.movePlayer(self.playerX - self.speed, self.playerY)
        # Moving the player to the right
        elif pressed[pygame.K_RIGHT]:
            self.direction = [1, 0, 0, 0]
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
        # Reset the player to the starting point if he has fallen from the map
        if self.playerY > 900:
            self.resetPLayer()

    def drawPlayer(self, picture):
        drawOnScreen(
            picture,
            self.playerX - self.scroll[0] - 17,
            self.playerY - self.scroll[1] - 11
        )

    def getPlayerImage(self):
        # Drawing the player to the screen
        if self.direction[0]:
            self.drawPlayer(self.vitaRunRight[self.runAnimation // 5])
        elif self.direction[1]:
            self.drawPlayer(self.vitaRunLeft[self.runAnimation // 5])
        else:
            self.drawPlayer(self.vitaIdle[self.idleAnimation // 10])
        if self.idleAnimation > 48:
            self.idleAnimation = 0
        if self.runAnimation < 24:
            self.runAnimation += 1
        else:
            self.runAnimation = 0


game = mainClass()
# Game Loop
while (1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(colors["black"])
    game.updatePlayer()
    game.drawMap()
    game.getPlayerImage()
    pygame.display.flip()
    clock.tick(60)
