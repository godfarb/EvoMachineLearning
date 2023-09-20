import random

import numpy
import pygame
from NeuralNetworkModel import *
from GeneticPopulationModel import *
import time

global screen
global start_of_prog
global fitness
fitness = []
start_of_prog = time.time()

#def fitness_func():
#    fitness.append(10 - start + time.time())
#    print("hey" , fitness)




class dot:

    def __init__(self, target, starting_pos, order, screen_size):
        self.velocity = 3

        self.brain = NeuralNetwork(4, 4, 8, 4, order=order)
        self. screen_size = screen_size
        self.x = starting_pos[0]
        self.y = starting_pos[1]
        self.pos = (self.x, self.y)
        self.target = target
        self.surface = pygame.Surface((4,4))
        self.surface.fill((0,0,0))

        self.distance_from_target = numpy.sqrt(pow(target[0] - self.x, 2) + pow(target[1] - self.y, 2))
        self.alive = True
        self.xdif = (target[0] - self.x)
        self.ydif = target[1] - self.y
    def changeTarget(self, target):
        self.target = target


    def update(self):
        if self.alive:
            #angle = self.brain.predict([float(self.distance_from_target)])
            chois = self.brain.predict([self.x,self.y, target[0], target[1]])

            pred = max(chois)
            for i in range(4):
                if chois[i] == pred:
                    self.des = [[1,0],[0,1],[-1,0],[0,-1]][i]

                    break



            self.x+=self.des[0] * self.velocity
            self.y+=self.des[1] * self.velocity







            if self.x < 0:
                  self.x = 4
            elif self.x > self.screen_size[0]:
                  self.x = self.screen_size[0] - 4

            if self.y < 0:
                  self.y = 4

            elif self.y > self.screen_size[1]:
                  self.y = self.screen_size[1] - 4

            self.xdif = target[0] - self.x
            self.ydif = target[1] - self.y
            self.pos = (int(self.x), int(self.y))
            self.distance_from_target = numpy.sqrt(self.xdif**2 + self.ydif**2)
            #if self.pos == self.target:
            #     print(fitness)
            #     fitness_func()
            #     self.alive = False

            screen.blit(self.surface, self.pos)

SIZE = 500
dots_pop = Population(SIZE, 292)
dots = [dot((350, 230), (250, 490), dots_pop.chromosomes[i].genes, (500, 500)) for i in range(SIZE)]






screen = pygame.display.set_mode((500,500))
screen.fill((255,255,255))

win_dot = pygame.Surface((5,5))
win_dot.fill((255,0,0))


target = (350, 230)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((255,255,255))

    screen.blit(win_dot, target)
    fitness = [0 for i in range(SIZE)]
    timecounter = 0
    steps = 0
    start = time.time()
    for a in range(5):
        steps = 0
        screen.blit(win_dot, target)
        while steps < 300:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            screen.fill((255,255,255))

            screen.blit(win_dot, target)
            for i in range(SIZE):
                dots[i].update()

            pygame.display.flip()
            steps += 1
        fitness = [fitness[i] + 771 - dots[i].distance_from_target for i in range(SIZE)]


        target = (random.randint(0, 500), random.randint(0, 500))
        dots = [dot(target, target, dots_pop.chromosomes[i].genes, [500, 500]) for i in range(SIZE)]
        print("a")



    sorted_fitness = fitness
    sorted_fitness.sort()
    print(sorted_fitness)
    dots_pop.nextGenByBest(fitness)
    dots = [dot(target, (250, 490), dots_pop.chromosomes[i].genes, [500, 500]) for i in range(SIZE)]

