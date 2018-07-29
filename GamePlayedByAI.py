import pygame
from Player import Player
from Egg import Egg
import random
import numpy as np
import pickle

class EggGame(object):

    def __init__(self):
        pygame.display.set_caption("Egg Collector")
        self.obstacleSpeed = 2.0
        self.score = 0
        self.backgroundColor = (255, 0, 0)
        self.dimensions = (900, 600)
        self.lastObstacle = None
        self.movementSpeed = 5
        self.running = True
        self.lives = 3
        self.fontName = pygame.font.match_font('arial')
        self.loadedImages = [pygame.image.load("GameImages/background.jpg")]
        self.clock = pygame.time.Clock()


    def drawBackground(self, screen):
    	screen.blit(self.loadedImages[0], (0, 0))

    def generateObstacles(self):
    	self.lastObstacle = Egg(random.randint(25, 875), 25)

    def destroyObstacle(self):
        self.lastObstacle = None

    def drawText(self, surf, text, size, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, (0, 0, 0))
        textRect = textSurface.get_rect()
        textRect.midtop = (x, y)
        surf.blit(textSurface, textRect)

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(self.dimensions)
        pygame.display.flip()
        player = Player(430, 550)
        with open('inputWeights', 'rb') as fp:
            player.inputWts = np.array(pickle.load(fp))
            print("loaded inputweights")
        
        with open('outputWeights', 'rb') as fp:
            player.outputWts = np.array(pickle.load(fp))
            print("loaded outputWeights")


        while self.running:
            # Frame Rate
            self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False


            if self.lastObstacle != None:
                prediction = player.predict(np.array([self.lastObstacle.x, self.lastObstacle.x - player.x]))
                maxIndex = prediction.index(max(prediction))
                print(maxIndex)

                if maxIndex == 0:
                    player.controlPlayer(self.movementSpeed * -1, 850)
                elif maxIndex == 1:
                    player.controlPlayer(self.movementSpeed, 850)
                
            # Draw game background
            self.drawBackground(screen)

            # Generate obstacles if no obstacles are present on screen
            if self.lastObstacle == None:
                self.generateObstacles()
            else:
                self.lastObstacle.propagate(self.obstacleSpeed)

                # If player collides with egg increment score
                if player.checkCollision(self.lastObstacle):
                    self.score += 1
                    self.destroyObstacle()

                # If obstacle hits ground, decrement life
                elif self.lastObstacle.checkOutOfBoundary(self.dimensions[1]):
                    self.lives -= 1
                    self.destroyObstacle()
                else:
                    self.lastObstacle.drawCharacter(screen)
            
            # Exit Game if lives = 0
            if self.lives == 0:
                self.running = False;

            # Draw character on screen
            player.drawCharacter(screen)
            self.drawText(screen, "Score: " + str(self.score), 20, 700, 100)
            self.drawText(screen, "Lives: " + str(self.lives), 20, 100, 100)
            pygame.display.update()


game = EggGame();
game.main()
