import pygame
from bullet import Bullet

class Spaceship():

    def __init__(self, width, height, x, y, color, image, sound):
        self.hit_points = 1
        self.width      = width
        self.height     = height
        self.x          = x
        self.y          = y
        self.color      = color
        self.image      = image
        self.sound      = sound
        self.alive      = True
        self.name       = ""
        return

    def setHitPoints(self, hit_points):
        self.hit_points = hit_points

    def getHitPoints(self):
        return self.hit_points

    def setName(self, name):
        self.name = name
        return

    def getName(self):
        return self.name

    def decreaseHitPoints(self, damage):
        self.hit_points = self.hit_points - damage
        if self.hit_points <= 0:
            self.setAlive(False)

    def moveLeft(self, dx):
        self.x -= dx
        # check the wall
        if self.x < 0:
            self.x = 0
        return

    def moveRight(self, dx, upper_limit):
        self.x += dx
        # check the wall
        if self.x > upper_limit:
            self.x = upper_limit
        return

    def moveUp(self, dy):
        self.y -= dy
        # check the wall
        if self.y < 0:
            self.y = 0
        return

    def moveDown(self, dy, board_height):
        self.y += dy
        # check the wall
        if self.y > board_height - self.height:
            self.y = board_height - self.height
        return

    def fire(self,width,height,color):
        return Bullet(width,height,(self.x + self.width) , 
                      (self.y + (self.height/2) - (height/2+25)),color)
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        return
        
    def setAlive(self, alive):
        self.alive = alive

    def getAlive(self):
        return self.alive
    
    def getDimensions(self):
        return self.x, self.y, self.width, self.height

    def setImage(self, newImage):
        self.image = pygame.image.load(newImage)

    def getImage(self):
        return self.image

    def setWidth(self, width):
        self.width = width
        return

    def getWidth(self):
        return self.width

    def setHeight(self, height):
        self.height = height
        return

    def getHeight(self):
        return self.height
