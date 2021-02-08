import numpy as np
import random

from operator import itemgetter

MUTATION = 0.01
CROSSOVER = 0.8
ELITISM = 0.1

def crossover(a, b, mutation_rate, kind='single', t=0.5, verbose=False):
    if kind == 'average':
        new_net = (1 - t) * neural_net_a + t * neural_net_b
    elif kind == 'single':
        a_enc = a.encode()
        b_enc = b.encode()
        
        split = random.randint(0, len(a_enc)-1)
        split_a = a_enc[:split].copy()
        split_b = b_enc[:split].copy()
        
        a_enc[:split] = split_b
        b_enc[:split] = split_a
        
        if verbose:
            print("Split index:", split)
        
        new_a, new_b = a.decode(a_enc), b.decode(b_enc)
        ra, rb = random.random(), random.random()
        if ra < mutation_rate:
            new_a.mutate()
        if rb < mutation_rate:
            new_b.mutate()
        return new_a, new_b
        
    elif kind == 'uniform':
        pass


def new_generation(w):
    fitness = w.fitness()
    s = sum(fitness)
    selection_probs = [f/s for f in fitness]
    sorted_index = np.argsort(fitness)[::-1]

    elite_num = int(len(sorted_index)*ELITISM)
    elite_index = sorted_index[:elite_num]
    elites = list(itemgetter(*elite_index)(w.birds))
    elites = [b.network for b in elites]

    to_breed = int(CROSSOVER * len(w.birds)/2)

    children = [None]*(2*to_breed)
    for i in range(to_breed):
        parents = np.random.choice(w.birds, 2, p=selection_probs)
        children_nets = crossover(parents[0].network, parents[1].network, MUTATION)
        children[2*i], children[2*i+1] = children_nets[0], children_nets[1]

    missing = len(w.birds) - len(elites) - len(children)
    normals = np.random.choice(w.birds, missing)
    normals = [b.network for b in normals]

    return elites + children + normals