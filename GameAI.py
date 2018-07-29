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
        self.generationCount = 1
        self.fontName = pygame.font.match_font('arial')
        self.loadedImages = [pygame.image.load("GameImages/background.jpg")]
        self.players = [Player(430, 550) for i in range(0, 500)]
        self.clock = pygame.time.Clock()
        self.stopgen = False


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
    
    def moveAllPlayersBasedOnPredictions(self):
        if self.lastObstacle != None:
                for player in self.players:
                    prediction = player.predict(np.array([self.lastObstacle.x, self.lastObstacle.x - player.x]))
                    maxIndex = prediction.index(max(prediction))

                    if maxIndex == 0:
                        player.controlPlayer(self.movementSpeed * -1, 850)
                    elif maxIndex == 1:
                        player.controlPlayer(self.movementSpeed, 850)
    
    def drawAllPlayers(self, canvas):
        for player in self.players:
            player.drawCharacter(canvas)

    def checkCollision(self):
        if self.lastObstacle != None:
            for player in self.players:
                if player.checkCollision(self.lastObstacle):
                    player.score += 1

    def BuildNextGeneration(self):
        self.generationCount += 1
        newPlayers = []
        self.players.sort(key=lambda x: x.score, reverse = True)

        if len(self.players) < 5:
            with open('inputWeights', 'wb') as fp:
                pickle.dump(self.players[0].inputWeights.tolist(), fp)

            with open('outputWeights', 'wb') as fp:
                pickle.dump(self.players[0].outputWeights.tolist(), fp)
            self.stopgen = True
            
            


        # Keep 1 top scorer as it is
        self.players[0].x = 430
        #self.players[1].x = 430
        self.players[0].score = 0
        #self.players[1].score = 0
        newPlayers.append(self.players[0])
        #newPlayers.append(self.players[1])
        if not self.stopgen:
            bestTwo = Player(430, 550)
            bestTwo.crossOver(self.players[0], self.players[1])
            newPlayers.append(bestTwo)

            bestAndWorst = Player(430, 550)
            bestAndWorst.crossOver(self.players[0], self.players[len(self.players) - 1])
            newPlayers.append(bestAndWorst)

            for i in range(0, len(self.players) - 53):
                par1 = self.players[random.randint(0, len(self.players)-1)]
                par2 = self.players[random.randint(0, len(self.players)-1)]

                child = Player(430, 550)
                child.crossOver(par1, par2)
                newPlayers.append(child)
        
            self.players = newPlayers
            self.restart()
    
    def getMaxScoreForGeneration(self):
        max_score = 0
        for player in self.players:
            if player.score > max_score:
                max_score = player.score
        return max_score

    def restart(self):
        self.lastObstacle = None
        self.lives = 3


    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(self.dimensions)
        pygame.display.flip()

        while self.running:
            # Frame Rate
            self.clock.tick(1000)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.moveAllPlayersBasedOnPredictions()
                    

            # Draw game background
            self.drawBackground(screen)

            # Generate obstacles if no obstacles are present on screen
            if self.lastObstacle == None:
                self.generateObstacles()
            else:
                self.lastObstacle.propagate(self.obstacleSpeed)

                # If obstacle hits ground, decrement life
                if self.lastObstacle.checkOutOfBoundary(self.dimensions[1]):
                    self.lives -= 1
                    self.destroyObstacle()
                else:
                    self.lastObstacle.drawCharacter(screen)
            
            self.checkCollision()
            # Exit Game if lives = 0
            #if self.lives == 0:
            #    self.running = False;
            if self.lives < 0 and self.stopgen == False:
                self.BuildNextGeneration()
            # Draw character on screen
            self.drawAllPlayers(screen)
            self.drawText(screen, "Generation: " + str(self.generationCount), 20, 700, 100)
            self.drawText(screen, "Lives: " + str(self.lives), 20, 100, 100)
            pygame.display.update()


game = EggGame();
game.main()
