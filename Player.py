import pygame
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 38, 40)
        self.image = pygame.image.load("GameImages/bucketsmall.png")

    def drawCharacter(self, canvas):
        self.hitbox = (self.x, self.y, 38, 40)
        canvas.blit(self.image, (self.x, self.y))
        #pygame.draw.rect(canvas, (255, 0, 0), self.hitbox, 2)

    def controlPlayer(self, speed, boundary):
        if self.x + speed >= 0 and self.x + speed <= boundary:
            self.x += speed
            self.hitbox = (self.x, self.y, 38, 40)

    def checkCollision(self, sprite):
        return pygame.Rect(self.hitbox).colliderect(sprite.hitbox)