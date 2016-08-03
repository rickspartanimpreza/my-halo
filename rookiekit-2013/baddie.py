import time
import pygame
import random

class Baddie():

    def __init__(self,width,height,x,y,image,sound):
        self.hit_points = 1
        self.width  = width
        self.height = height
        self.x      = x
        self.y      = y
        self.new_x  = x
        self.new_y  = y
        self.speed  = 3
        self.image  = image
        self.sound  = sound
        self.alive  = True
        self.hit    = False
	self.name   = ""
        return

    def setHitPoints(self, hit_points):
        self.hit_points = hit_points

    def decreaseHitPoints(self, damage):
        self.hit_points = self.hit_points - damage
        if self.hit_points <= 0:
            self.setAlive(False)

    def checkHitPlayer(self, x, y, w, h):
        if self.hitRectangle(x, y, w, h):
            self.setAlive(False)
            self.hit = True
			
    def setName(self, name):
	self.name = name
	return
		
    def getName(self):
	return self.name

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def getHit(self):
        return self.hit

    def hitRectangle(self, x, y, w, h):
        if( ((self.x + self.width) >= x) and
            (self.x <= x + w) ):
            if( ((self.y + self.height) >= y) and
                (self.y <= y + h)):
                return True
        return False

    def tick(self,back_wall,upper_wall,lower_wall):
        self.new_x = self.x - self.speed
        self.new_y = self.y + random.randint(-1,1)
        if self.new_x < back_wall:
            self.setAlive(False)
        else:
            self.x = self.new_x
        if self.new_y < upper_wall:
            self.new_y = upper_wall
        elif self.new_y + self.height > lower_wall:
            self.new_y = lower_wall - self.height
        self.y = self.new_y
        return self.alive

    def getAlive(self):
        return self.alive

    def getDimensions(self):
        return self.x,self.y,self.width,self.height

    def setAlive(self,alive):
        self.alive = alive
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))
        return
        
