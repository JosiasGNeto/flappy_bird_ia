# Imports #
import random
import pygame
import os

# Screen Size #
WIDTH  = 500
HEIGHT = 800

# Images #
IMG_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'back.png')))
IMG_FLOOR      = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
IMG_PIPE       = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMG_BIRD       = [
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),        
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))), 
                    pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png'))), 
                 ]

# Game Font #
pygame.font.init()
FONT = pygame.font.SysFont('arial', 50)


class Bird:
    IMAGES = IMG_BIRD

    # Animating the rotation #

    ANIMATION_TIME = 5
    ROTATION_SPEED = 20
    ROTATION_MAX   = 25

    # Constructor Method #
    def __init__(self, x, y):
        self.x      = x
        self.y      = y
        self.time   = 0
        self.angle  = 0
        self.speed  = 0
        self.frames = 0
        self.height = self.y
        self.image  = IMAGES[0]

    # Jump Method #
    def jump(self):
        self.time   = 0
        self.speed  = -10.5
        self.height = self.y

    # Movement Method #
    def movement(self):
        self.time += 1
        self.aceleration = 1.5

        movement = self.aceleration * (self.time**2) + self.speed

        # Limit Movement #
        if movement > 16:
            movement = 16
        elif movement < 0:
            movement -= 2

        self.y += movement

        # Angle #
        if movement < 0 or self.y < (self.height + 50):
            if self.angle < self.ROTATION_MAX:
                self.angle = self.ROTATION_MAX
        else:
            if self.angle > -90:
                self.angle -= self.ROTATION_SPEED

    def draw(self, screen):
        # set what image we are gonna use 
        self.frames  += 1

        if self.frames < self.ANIMATION_TIME:
            self.image = self.IMAGES[0]
        elif self.frames < self.ANIMATION_TIME*2:
            self.image = self.IMAGES[1]
        elif self.frames < self.ANIMATION_TIME*3:
            self.image = self.IMAGES[2]
        elif self.frames < self.ANIMATION_TIME*4:
            self.image = self.IMAGES[1]
        elif self.frames < self.ANIMATION_TIME*4 + 1:
            self.image = self.IMAGES[0]

        # if bird is falling don't use the wings 
        if self.angle <= -80:
            self.image  = self.IMAGES[1]
            self.frames = self.ANIMATION_TIME*2

        # draw image 
        center_position = self.image.get_rect(topleft = (self.x, self.y)).center
        rotate_image    = pygame.transform.rotate(self.imagem, self.angle)
        hitbox          = rotate_image.get_rect(center = center_position)

        screen.blit(rotate_image, hitbox.topleft)

class Pipe:
    pass

class Floor:
    pass
