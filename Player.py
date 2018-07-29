import pygame
import numpy as np
import random
class Player(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, 38, 40)
        self.image = pygame.image.load("GameImages/bucketsmall.png")

        # Define the Neural Network
        self.inputNodes = 2
        self.outputNodes = 3
        self.hiddenNodes = 6

        self.inputWeights = np.random.rand(self.inputNodes, self.hiddenNodes)
        self.outputWeights = np.random.rand(self.hiddenNodes, self.outputNodes)

        self.score = 0
    
    def predict(self, userInput):
        
        hiddenLayer = np.dot(userInput, self.inputWeights)
        hiddenLayer =  1.0 / (1.0 + np.exp(-1.0 * hiddenLayer))
        outputLayer = np.matmul(hiddenLayer, self.outputWeights)
        outputLayer =  1.0 / (1.0 + np.exp(-1.0 * outputLayer))
        return outputLayer.tolist()

    def crossOver(self, parent1, parent2):
        parent1InputWeights = parent1.inputWeights.tolist()
        parent2InputWeights = parent2.inputWeights.tolist()

        parent1OutputWeights = parent1.outputWeights.tolist()
        parent2OutputWeights = parent1.outputWeights.tolist()

        # Fix Input inputWeights
        self.inputWeights = []

        for i in range(0, self.inputNodes):
            arrayChooser = random.randint(0, 1)
            if arrayChooser == 0:
                self.inputWeights.append(parent1InputWeights[i])
            else:
                self.inputWeights.append(parent2InputWeights[i])


        self.inputWeights = np.array(self.mutate(self.inputWeights))

        # Fix Output Weights

        self.outputWeights = []

        for i in range(0, self.hiddenNodes):
            arrayChooser = random.randint(0, 1)
            if arrayChooser == 0:
                self.outputWeights.append(parent1OutputWeights[i])
            else:
                self.outputWeights.append(parent2OutputWeights[i])

        self.outputWeights = np.array(self.mutate(self.outputWeights))

    def mutate(self, array):
        mutateProb = 0.7
        if random.uniform(0, 1) > mutateProb:
            first = random.randint(0, len(array)-1)
            second = random.randint(0, len(array)-1)
            temp = array[first]
            array[first] = array[second]
            array[second] = temp


            first = random.randint(0, len(array)-1)
            second = random.randint(0, len(array)-1)
            temp = array[first]
            array[first] = array[second]
            array[second] = temp
        return array

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