import numpy as np
import random

from operator import itemgetter

def crossover(a, b, verbose=False):
    a_enc = a.encode()
    b_enc = b.encode()

    split = random.randint(0, len(a_enc)-1)
    split_a = a_enc[:split].copy()
    split_b = b_enc[:split].copy()

    a_enc[:split] = split_b
    b_enc[:split] = split_a

    if verbose:
        print("Split index:", split)

    return a_enc, b_enc


def roulette_selection(birds, to_breed):
    fitness = [b.fitness for b in birds]
    s = sum(fitness)
    if s == 0:
        selection_probs = [1/len(birds) for _ in range(len(birds))]
    else:
        selection_probs = [f/s for f in fitness]

    parents = [[None,None] for _ in range(to_breed)] 
    for i in range(to_breed):
        parent_birds = np.random.choice(birds, 2, p=selection_probs)
        parents[i][0], parents[i][1] = parent_birds[0].network, parent_birds[1].network
    
    return parents


def tournament_selection(birds, to_breed, k):
    parents = [[None,None] for _ in range(to_breed)]
    for i in range(to_breed):
        contestants = np.random.choice(birds, k)
        fitness = [b.fitness for b in contestants]
        best_index = np.argsort(fitness)[:-3:-1]
        parents[i][0], parents[i][1] = contestants[best_index[0]].network, contestants[best_index[1]].network
    return parents
    
    
def breed_parents(birds, to_breed, selection='tournament', k=None):
    if selection == 'roulette':
        parents = roulette_selection(birds, to_breed)
    elif selection == 'tournament':
        parents = tournament_selection(birds, to_breed, k=k)
    
    children = [None] * (2*to_breed)
    for i, p in enumerate(parents):
        children[2*i], children[2*i+1] = crossover(p[0], p[1])

    return children
        
def new_generation(birds, settings):

    MUTATION = settings['MUTATION'] 
    CROSSOVER = settings['CROSSOVER']
    ELITISM = settings['ELITISM']
    SELECTION = settings['SELECTION']
    CONTESTANTS = settings['CONTESTANTS']
    fitness = [b.fitness for b in birds]
    sorted_index = np.argsort(fitness)[::-1] 

    # Élites
    num_elite = int(len(sorted_index)*ELITISM)
    elite_index = sorted_index[:num_elite]
    if num_elite == 1:
        elites = [birds[elite_index[0]]]
    else:
        elites = list(itemgetter(*elite_index)(birds))
    elites = [b.network.encode() for b in elites]
    
    # Hijos
    to_breed = int(CROSSOVER * len(birds)/2)
    children = breed_parents(birds, to_breed, SELECTION, CONTESTANTS)
    num_children = len(children)
    
    # Normales
    missing = len(birds) - num_elite - num_children
    normals = np.random.choice(birds, missing)
    normals = [b.network.encode() for b in normals]
    
    # Mutación
    to_mutate = children + normals

    mutation_number = int(MUTATION * len(to_mutate) * len(to_mutate[0]))

    mutated_inds = np.random.randint(0, len(to_mutate)-1, mutation_number)
    mutated_genes = np.random.randint(0, len(to_mutate[0])-1, mutation_number)
    for i,j in zip(mutated_inds, mutated_genes):
        to_mutate[i][j] += np.random.normal()
        
    # Unión
    return [birds[0].network.decode(b) for b in elites], \
           [birds[0].network.decode(b) for b in to_mutate[:num_children]], \
           [birds[0].network.decode(b) for b in to_mutate[num_children:]]