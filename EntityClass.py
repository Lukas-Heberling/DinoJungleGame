import pygame


class entityClass:
    def __init__(self, x, y, width, height, speed, lives, velocityDown, direction):
        # Position
        self.x = x
        self.y = y
        # Hitbox
        self.width = width
        self.height = height
        # Stats
        self.speed = speed
        self.lives = lives
        self.score = 0
        # Jumping
        self.jumpvar = 0
        self.velocityDown = velocityDown
        self.jump = False
        # Animation
        # direction = [walkRight, walkLeft, Jump, stand]
        # TODO mayby add the ability to duck ...
        self.direction = direction
        # Backup
        self.backup = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "speed": speed,
            "lives": lives,
            "velocityDown": velocityDown,
        }

    def move(self, newX, newY):
        self.x = newX
        self.y = newY

    def dmg(self, dmg):
        self.lives -= dmg

    def getRect(self, values):
        if "x" in values and "y" in values:
            return pygame.Rect(values["x"], values["y"], self.width, self.height)
        else:
            return pygame.Rect(self.x, self.y, self.width, self.height)

    def reset(self, resetType, resetValues):
        if resetType == "completeBackup":
            self.x = self.backup["x"]
            self.y = self.backup["y"]
            self.width = self.backup["width"]
            self.height = self.backup["height"]
            self.speed = self.backup["speed"]
            self.lives = self.backup["lives"]
            self.velocityDown = self.backup["velocityDown"]
        elif resetType == "player":
            self.velocityDown = 3
            self.x = 50
            self.y = -150
        elif resetType == "custom":
            if "x" in resetValues:
                self.x = resetValues["x"]
            if "y" in resetValues:
                self.y = resetValues["y"]
            if "width" in resetValues:
                self.width = resetValues["width"]
            if "height" in resetValues:
                self.height = resetValues["height"]
            if "speed" in resetValues:
                self.speed = resetValues["speed"]
            if "lives" in resetValues:
                self.lives = resetValues["lives"]
            if "velocityDown" in resetValues:
                self.velocityDown = resetValues["velocityDown"]
