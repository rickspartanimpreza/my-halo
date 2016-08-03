### This file creates a scrolling background 
### And paints it to the screen.

import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, filename, width):
        pygame.sprite.Sprite.__init__(self)   #becomes a sprite
        self.screen_width = width             #store screen width
        image = pygame.image.load("blood_gulch800x500.png")  #load the image
        image = image.convert()
        self.rect = image.get_rect()
        self.image = image
        self.flipped_image = pygame.transform.flip(self.image, 1, 0) #flip the img
        self.flipped_rect  = self.flipped_image.get_rect()
        self.flipped_rect.left = self.rect.right #set starting point of 2nd image
        self.dx = -1     # this will control how fast the background moves


    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def paint(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.flipped_image, self.flipped_rect)
    
    def update(self):
        self.rect.left += self.dx
        self.flipped_rect.left += self.dx

        if self.rect.right < 0:
            self.rect.left = self.flipped_rect.right
            
        if self.flipped_rect.right < 0:
            self.flipped_rect.left = self.rect.right

    def setSpeed(self, dx):
        self.dx = dx
        
