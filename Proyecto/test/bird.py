import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from itertools import islice
from operator import itemgetter

import random
import numpy as np
import os

from time import sleep

def intersects(center, radius,
               xy, width, height):
    cdistx, cdisty = np.abs(center[0] - xy[0]), np.abs(center[1] - xy[1])
    
    if cdistx > width/2 + radius:
        return False
    if cdisty > height/2 + radius:
        return False
    
    if cdistx <= width/2:
        return True
    if cdisty <= height/2:
        return True
    
    corner = (cdistx - width/2)**2 + (cdisty - height/2)**2
    return corner <= radius**2
    
ay = -1
vx = -1
dt = 0.1
TOP = 8
RIGHT = 10
PIPE_GAP = 2.5
MINIMUM_HEIGHT = 2
PIPE_WIDTH = 1
BIRD_RADIUS = 0.3
FLAP_SPEED = 1.2
MAX_STEPS = 5000

DEATH_PENALTY = -2
ALIVE_REWARD = 0.1
PIPE_REWARD = 1.5

class Bird:
    def __init__(self, network):
        self.y = TOP/2
        self.vy = 0.
        self.alive = True
        self.fitness = 0
        self.network = network
        
    def __repr__(self):
        return 'y: ' + str(self.y) + '\n' + \
               'vy: ' + str(self.vy) + '\n' + \
               'alive: ' + str(self.alive) + '\n' + \
               'fitness: ' + str(self.fitness)
                
    def move(self, flap):
        if not self.alive:
            return
        self.y += 1/2 * ay * dt**2 + self.vy * dt
        if flap:
            self.vy = FLAP_SPEED
        else:
            self.vy += ay * dt
        if self.y > TOP:
            self.y = TOP
    
    def step(self, pipe):
        choice = self.network([self.y, self.vy, pipe.x, pipe.y+PIPE_GAP/2, pipe.y-PIPE_GAP/2])
        self.move(choice)
                
    def plot(self, ax, draw_dead=False):
        if not self.alive and not draw_dead:
            return
        c = Circle((0, self.y), BIRD_RADIUS)
        ax.add_patch(c)

        
class Pipe:
    def __init__(self, x):
        self.x = x
        self.y = MINIMUM_HEIGHT  + random.random() * (TOP-2*MINIMUM_HEIGHT)
        
    def step(self):
        self.x += vx * dt
        
    def plot(self, ax):
        r1 = Rectangle((self.x, 0), PIPE_WIDTH, self.y - PIPE_GAP/2)
        r2 = Rectangle((self.x, self.y + PIPE_GAP/2), PIPE_WIDTH, TOP)
        ax.add_patch(r1)
        ax.add_patch(r2)
        ax.scatter([self.x], [self.y])
        
class World:
    def __init__(self, nets):
        self.birds = [Bird(n) for n in nets]
        self.pipes = [Pipe((RIGHT-PIPE_WIDTH)/2), Pipe(RIGHT)]
        self.steps = 0
        self.alive = True
        
    def check_collision(self):
        i = 0
        killed = [False]*len(self.birds)
        while i < len(self.birds):
            b = self.birds[i]
            
            if not b.alive:
                i += 1
                continue
                
            if b.y - BIRD_RADIUS <= 0:
                b.alive = False
                killed[i] = True
                i += 1
                continue
                
            for p in self.pipes:
                height_bot = p.y - PIPE_GAP/2
                height_top = TOP - p.y - PIPE_GAP/2
                cx = p.x + PIPE_WIDTH/2
                cy_bot = height_bot/2
                cy_top = p.y + PIPE_GAP/2 + height_top/2
                if intersects([0, b.y], BIRD_RADIUS, [cx, cy_bot], PIPE_WIDTH, height_bot) \
                or intersects([0, b.y], BIRD_RADIUS, [cx, cy_top], PIPE_WIDTH, height_top):
                    b.alive = False
                    killed[i] = True
                    break
            i += 1
        return killed
            
    def step_pipes(self):
        passed_pipe = False
        if not self.alive:
            return [0]*len(self.birds)
        for i,p in enumerate(self.pipes):
            p.step()
            if p.x + PIPE_WIDTH + BIRD_RADIUS < 0:
                self.pipes.pop(i)
                self.pipes.append(Pipe(RIGHT))
                passed_pipe = True
        return passed_pipe
    
    def step_birds(self):
        for b in self.birds:
            b.step(self.pipes[0])
        
    def step(self):
        passed_pipe = self.step_pipes()
        self.step_birds()

        killed = self.check_collision()
        self.steps += 1
        if not any([b.alive for b in self.birds]) or self.steps > MAX_STEPS:
            self.alive = False
            
        for i,(b,k) in enumerate(zip(self.birds, killed)):
            if b.alive:
                b.fitness += b.alive*(ALIVE_REWARD + passed_pipe*PIPE_REWARD)
                
    def fitness(self):
        return [b.fitness for b in self.birds]
        
    def plot(self, ax, draw_dead=False):
        for p in self.pipes:
            p.plot(ax)
        for b in self.birds:
            b.plot(ax, draw_dead=draw_dead)
            
    def play(self, draw=False, path="./"):
        i = 0
        while self.alive:
            self.step()
            if draw:
                fig, ax = plt.subplots(figsize=(10,10))
                ax.set_xlim(-1, RIGHT)
                ax.set_ylim(0, TOP)
                ax.set_aspect('equal')
                self.plot(ax)
                name = str(i).rjust(5,'0') + ".png"
                fig.savefig(os.path.join(path, name))
                plt.close()
            i += 1