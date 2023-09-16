from os import supports_effective_ids
import pygame
import random
import sys
from pygame.locals import *
from EntityClass import entityClass
from GameHelper import *

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
    "lightBlue": (0, 255, 255),
    "green": (0, 255, 0),
}


# INIT
pygame.init()
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
pygame.display.set_caption("RunningHolliday ~Lukas")


gameIcon = pygame.image.load("Graphics/Vita/vita_00.png")
pygame.display.set_icon(gameIcon)


# Some layers to create the Background
# [LayerPicture, multiplier how fast the background moves]
layers = [
    [pygame.image.load("Graphics/Background/Layers/1.png").convert_alpha(), 0.1],
    [pygame.image.load("Graphics/Background/Layers/2.png").convert_alpha(), 0.2],
    [pygame.image.load("Graphics/Background/Layers/3.png").convert_alpha(), 0.3],
    [pygame.image.load("Graphics/Background/Layers/4.png").convert_alpha(), 0.4],
    [pygame.image.load("Graphics/Background/Layers/5.png").convert_alpha(), 0.5],
]
tiles = {
    "down": pygame.image.load("Graphics/Tiles/Down.png").convert(),
    "left": pygame.image.load("Graphics/Tiles/Left.png").convert(),
    "right": pygame.image.load("Graphics/Tiles/Right.png").convert(),
    "up": pygame.image.load("Graphics/Tiles/Up.png").convert(),
    "no": pygame.image.load("Graphics/Tiles/No.png").convert(),
    "downLeft": pygame.image.load("Graphics/Tiles/downLeft.png").convert(),
    "downRight": pygame.image.load("Graphics/Tiles/DownRight.png").convert(),
    "upLeft": pygame.image.load("Graphics/Tiles/UpLeft.png").convert(),
    "upRight": pygame.image.load("Graphics/Tiles/UpRight.png").convert(),
}
flag = [
    pygame.image.load("Graphics/Objects/Flag/Flag_0.png").convert_alpha(),
    pygame.image.load("Graphics/Objects/Flag/Flag_1.png").convert_alpha(),
    pygame.image.load("Graphics/Objects/Flag/Flag_2.png").convert_alpha(),
    pygame.image.load("Graphics/Objects/Flag/Flag_3.png").convert_alpha(),
]

vitaRunRight = [
    pygame.image.load("Graphics/Vita/vita_05.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_06.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_07.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_08.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_09.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_10.png").convert_alpha(),
]

vitaRunLeft = [
    pygame.image.load("Graphics/Vita/vita_05left.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_06left.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_07left.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_08left.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_09left.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_10left.png").convert_alpha(),
]
vitaIdle = [
    pygame.image.load("Graphics/Vita/vita_00.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_01.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_02.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_03.png").convert_alpha(),
    pygame.image.load("Graphics/Vita/vita_04.png").convert_alpha(),
]

heartImage = pygame.image.load("Graphics/heart.png").convert_alpha()


def getGameMap(path):
    # Building the Map out of the Level.txt file
    f = open(path + ".txt", "r")
    data = f.read()
    f.close()
    data = data.split("\n")
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


def menu():
    layerX = -150
    while 1:
        layerX -= 0.5
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
        mousePos = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mousePos[0], mousePos[1], 20, 20)
        buttonRect = pygame.Rect(300, 320, 100, 60)
        buttonSelected = False
        if mouseRect.colliderect(buttonRect):
            buttonSelected = True
        if buttonSelected:
            buttonColor = colors["lightBlue"]
        else:
            buttonColor = colors["darkGrey"]
        if clicked and buttonSelected:
            gameLoop()
        screen.fill(colors["black"])
        for layer in layers:
            drawOnScreen(screen, layer[0], layerX * layer[1], 0)
        pygame.draw.rect(screen, buttonColor, (300, 320, 100, 60))
        showtext(screen, "Running Holliday", 350, 50, 80)
        showtext(screen, "Play", 350, 350, 50)
        showtext(screen, "created by ~Lukas Heberling", 150, 680, 30)
        pygame.display.update()

def gameOverScreen(score, level):
    while 1:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
        mousePos = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mousePos[0], mousePos[1], 20, 20)
        menuButton = pygame.Rect(50, 520, 200, 60)
        tryAgainButton = pygame.Rect(450, 520, 200, 60)
        tryAgainButtonSelected = False
        menuButtonSelected = False
        if mouseRect.colliderect(tryAgainButton):
            tryAgainButtonSelected = True
        elif mouseRect.colliderect(menuButton):
            menuButtonSelected = True
        if tryAgainButtonSelected:
            tryAgainButtonColor = colors["lightBlue"]
        else:
            tryAgainButtonColor = colors["darkGrey"]
        if menuButtonSelected:
            menuButtonColor = colors["lightBlue"]
        else:
            menuButtonColor = colors["darkGrey"]
        if tryAgainButtonSelected and clicked:
            gameLoop()
        if menuButtonSelected and clicked:
            menu()
        screen.fill(colors["black"])
        pygame.draw.rect(screen, tryAgainButtonColor, (450, 520, 200, 60))
        pygame.draw.rect(screen, menuButtonColor, (50, 520, 200, 60))
        showtext(screen, "Game Over", 350, 50, 80)
        showtext(screen, "Score: " + str(score), 350, 200, 50)
        showtext(screen, "Level: " + str(level), 350, 400, 50)
        showtext(screen, "Try Again", 550, 550, 50)
        showtext(screen, "Menu", 150, 550, 50)
        pygame.display.update()

class mainClass:
    def __init__(self):
        # LEVEL
        self.level = 1
        # MAP
        self.map = getGameMap("Level" + str(self.level))
        self.scroll = [0, 0]
        self.mapScroll = [0, 0]
        self.flagAnimation = 0
        self.flagPosition = [2600, 175]
        self.tileHeight = 32

        # Player
        self.player = entityClass(50, -150, 40, 50, 5, 3, 3, [0, 0, 0, 1])
        # Player Vita
        self.runAnimation = 0
        self.idleAnimation = 0

    def drawTile(self, tile, x, y):
        # Drawing the Blocks of the map
        drawOnScreen(
            screen,
            tile,
            x * self.tileHeight - self.scroll[0],
            y * self.tileHeight - self.scroll[1],
        )

    def drawLayers(self):
        # Drawing the layers of the Background
        for layer in layers:
            layerXValue = -150 - self.scroll[0] * layer[1]
            layerPositions = [layerXValue]
            # Length image = 1400
            if (1400 + layerXValue) < 700:
                layerPositions.append(layerXValue + 1400)
            for layerPosition in layerPositions:
                drawOnScreen(screen, layer[0], layerPosition, 0)

    def drawInterface(self):
        showtext(screen, "Score: " + str(self.player.score), 600, 30, 50)
        showtext(screen, "Level: " + str(self.level), 350, 30, 40)
        for live in range(self.player.lives):
            screen.blit(heartImage, ((live * 50), 0))

    def drawMap(self):
        # Calc scroll player movement
        # Scrolling ist the Value that the tiles move so the player is standing in the middle of the screen
        self.mapScroll[0] += (self.player.x - self.mapScroll[0] - 330) / 20
        self.mapScroll[1] += (self.player.y - self.mapScroll[1] - 310) / 20
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
                            self.tileHeight,
                        ),
                    )
                    if block == "1":
                        self.drawTile(tiles["up"], x, y)
                    if block == "2":
                        self.drawTile(tiles["down"], x, y)
                    if block == "3":
                        self.drawTile(tiles["left"], x, y)
                    if block == "4":
                        self.drawTile(tiles["right"], x, y)
                    if block == "5":
                        self.drawTile(tiles["upLeft"], x, y)
                    if block == "6":
                        self.drawTile(tiles["upRight"], x, y)
                    if block == "7":
                        self.drawTile(tiles["downLeft"], x, y)
                    if block == "8":
                        self.drawTile(tiles["downRight"], x, y)
                    if block == "9":
                        self.drawTile(tiles["no"], x, y)
                x += 1
            y += 1
        drawOnScreen(
            screen,
            flag[0],
            self.flagPosition[0] - self.scroll[0],
            self.flagPosition[1] - self.scroll[1],
        )

    # PLAYER
    def checkforwin(self):
        flagRect = pygame.Rect(self.flagPosition[0], self.flagPosition[1], 48, 48)
        playerRect = self.player.getRect({})
        if playerRect.colliderect(flagRect):
            if self.player.lives < 5:
                self.player.lives += 1
            self.level += 1
            self.player.score += 100
            self.map = getGameMap("Level" + str(self.level))
            self.player.reset("player", {})

    def collide(self, newX, newY):
        # Checking if the player is colliding with the world
        collision = False
        # player rect
        playerRect = self.player.getRect({"x": newX, "y": newY})
        y = 0
        for row in self.map:
            x = 0
            for block in row:
                if block != "0":
                    mapBlock = pygame.Rect(
                        x * self.tileHeight,
                        y * self.tileHeight,
                        self.tileHeight,
                        self.tileHeight,
                    )
                    if mapBlock.colliderect(playerRect):
                        collision = True
                x += 1
            y += 1
        return collision

    def movePlayer(self, playerX, playerY):
        if not self.collide(playerX, playerY):
            self.player.move(playerX, playerY)

    def checkForDeath(self):
        if self.player.lives < 1:
            level = self.level
            score = self.player.score
            self.level = 1
            self.player.score = 0
            self.player.reset("player", {})
            self.map = getGameMap("Level" + str(self.level))
            self.player.lives = 3
            self.scroll = [0, 0]
            gameOverScreen(score, level)

    def escape(self):
        self.level = 1
        self.scroll = [0, 0]
        self.mapScroll = [0, 0]
        self.player.reset("player", {})
        self.map = getGameMap("Level" + str(self.level))
        self.player.lives = 3
        self.player.score = 0
        menu()

    def updatePlayer(self):
        # Checking if the player is dead
        self.checkForDeath()
        # Checking if the player has won
        self.checkforwin()
        # If nothing is pressed set the players direction to idle
        self.player.direction = [0, 0, 0, 1]
        self.idleAnimation += 1
        # Getting the pressed key
        pressed = pygame.key.get_pressed()
        # Escape the game
        if pressed[pygame.K_ESCAPE]:
            self.escape()
        # Set the Variables to initialize a jump
        if (
            pressed[pygame.K_UP]
            and not self.player.jump
            and self.collide(self.player.x, self.player.y + 1)
        ):
            self.player.direction = [0, 0, 1, 0]
            self.player.jump = True
            self.player.jumpvar = 15
        # Moving the player left
        elif pressed[pygame.K_LEFT]:
            self.player.direction = [0, 1, 0, 0]
            self.movePlayer(self.player.x - self.player.speed, self.player.y)
        # Moving the player to the right
        elif pressed[pygame.K_RIGHT]:
            self.player.direction = [1, 0, 0, 0]
            self.movePlayer(self.player.x + self.player.speed, self.player.y)
        # Gravity
        if (
            not self.collide(self.player.x, self.player.y + self.player.velocityDown)
            and self.player.jumpvar == 0
        ):
            self.player.y += self.player.velocityDown
            self.player.velocityDown += 0.5
        elif self.player.jumpvar == 0:
            self.player.velocityDown -= 1

        # Jumping
        if self.player.jump and self.player.jumpvar > 0:
            if not self.collide(
                self.player.x, self.player.y - (self.player.jumpvar ** 2) * 0.17
            ):
                self.player.y -= (self.player.jumpvar ** 2) * 0.12
            else:
                self.player.jumpvar = 0
                self.player.jump = False
            self.player.jumpvar -= 1

        # Touching the ground
        if self.collide(self.player.x, self.player.y + 1):
            self.player.jumpvar = 0
            self.player.velocityDown = 3
            self.player.jump = False

        # Reset the player to the starting point if he has fallen from the map
        if self.player.y > 900:
            self.player.lives -= 1
            self.player.reset("player", {})

    def drawPlayer(self, picture):
        drawOnScreen(
            screen,
            picture,
            self.player.x - self.scroll[0] - 17,
            self.player.y - self.scroll[1] - 11,
        )

    def getPlayerImage(self):
        # Drawing the player to the screen
        if self.player.direction[0]:
            self.drawPlayer(vitaRunRight[self.runAnimation // 5])
        elif self.player.direction[1]:
            self.drawPlayer(vitaRunLeft[self.runAnimation // 5])
        else:
            self.drawPlayer(vitaIdle[self.idleAnimation // 10])
        if self.idleAnimation > 48:
            self.idleAnimation = 0
        if self.runAnimation < 24:
            self.runAnimation += 1
        else:
            self.runAnimation = 0


game = mainClass()


def gameLoop():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(colors["lightBlue"])
        game.updatePlayer()
        game.drawMap()
        game.getPlayerImage()
        game.drawInterface()
        pygame.display.flip()
        clock.tick(60)


menu()
