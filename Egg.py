import pygame
class Egg(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 20, 20)
        self.image = pygame.image.load("egg.png")

    def drawCharacter(self, canvas):
        self.hitbox = (self.x, self.y, 20, 20)
        canvas.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(canvas, (255, 0, 0), self.hitbox, 2)

    def propagate(self, speed):
        self.y += speed
        self.hitbox = (self.x, self.y, 20, 20)

    def checkOutOfBoundary(self, boundary):
        if self.y > boundary:
            return True
        else:
            return False
