"""
Este archivo contiene funciones para implementar algoritmos genéticos.
"""

import numpy as np
import random

from operator import itemgetter

def crossover(a, b, verbose=False):
    """
    Cruza dos redes neuronales y regresa los cromosomas resultantes:

    Parámetros
    ----------
    a, b : NeuralNet
        Redes neuronales a cruzar

    Salida
    ------
    a_enc, b_enc : NeuralNet
        Redes producto del crossover de un solo punto de  `a` y `b`. Están
        codificadas para facilitar mutación.

    Notas
    -----
    Esta función implementa crossover de un sólo punto. Si por ejemplo tenemos
    los cromosomas [AAAAAA, BBBBBB], los pasos que sigue son:

    1. Escoge un índice aleatorio, por ejemplo 2.
    2. Parte los cromosomas en este índice, y los intercambia:

    AAAAAA --> AA AAAA --> BB AAAA --> BBAAAA
    BBBBBB --> BB BBBB --> AA BBBB --> AABBBB

    Los cromosomas intercambiados son dos hijos nuevos.
    """
    # Codificamos las redes de ambos individuos en un vector unidimensional
    a_enc = a.encode()
    b_enc = b.encode()

    # Crossover de un solo punto: escogemos un índice aleatorio donde partir
    # los vectores
    split = random.randint(0, len(a_enc)-1)
    split_a = a_enc[:split].copy()
    split_b = b_enc[:split].copy()

    # Intercambiamos los 
    a_enc[:split] = split_b
    b_enc[:split] = split_a

    if verbose:
        print("Split index:", split)

    return a_enc, b_enc


def roulette_selection(birds, to_breed):
    """
    Método de selección por ruleta.

    Parámetros
    ----------
    birds : list
        Lista de objetos `Bird` a seleccionar.

    to_breed : int
        Número de parejas a seleccionar.

    Salida
    ------
        parents: list
            Lista de listas de la forma [[a1,a2], [b1,b2], ...]. Cada sub-lista
            representa un conjunto de padres.
    """
    fitness = [b.fitness for b in birds]
    s = sum(fitness)
    if s == 0: # Si todos los participantes son igual de malos
        selection_probs = [1/len(birds) for _ in range(len(birds))]
    else: # Pesamos las probabilidades por el fitness de cada participante
        selection_probs = [f/s for f in fitness]

    parents = [[None,None] for _ in range(to_breed)] 
    for i in range(to_breed):
        # Selección aleatoria con probabilidades pesadas
        parent_birds = np.random.choice(birds, 2, p=selection_probs) 
        parents[i][0], parents[i][1] = parent_birds[0].network, parent_birds[1].network
    
    return parents


def tournament_selection(birds, to_breed, k):
    """
    Método de selección por torneo.

    Parámetros
    ----------
    birds : list
        Lista de objetos `Bird` a seleccionar.

    to_breed : int
        Número de parejas a seleccionar.

    k : int
        Número de participantes por torneo. Valores más grandes producen más
        presión de selección.

    Salida
    ------
        parents: list
            Lista de listas de la forma [[a1,a2], [b1,b2], ...]. Cada sub-lista
            representa un conjunto de padres.
    """
    parents = [[None,None] for _ in range(to_breed)]
    for i in range(to_breed):
        contestants = np.random.choice(birds, k) # k participantes
        fitness = [b.fitness for b in contestants]
        best_index = np.argsort(fitness)[:-3:-1] # Índices ordenados por fitness descendiente
        # Escogemos los dos mejores participantes
        parents[i][0], parents[i][1] = contestants[best_index[0]].network, contestants[best_index[1]].network 
    return parents
    
    
def breed_parents(birds, to_breed, selection='tournament', k=None):
    """
    Reproduce padres y produce una nueva generación.

    Parámetros
    ----------
    birds : list
        Lista de pájaros a seleccionar y reproducir

    to_breed : int
        Número de parejas a reproducir.

    selection : str
        Método de selección
            - tournament: Selección por torneo.
            - roulette : Selección por ruleta.
    
    k : int
        Número de parejas a usar en el torneo. Sólo válido cuando `selection='tournament'`
    """
    if selection == 'roulette':
        parents = roulette_selection(birds, to_breed)
    elif selection == 'tournament':
        parents = tournament_selection(birds, to_breed, k=k)
    
    children = [None] * (2*to_breed) # 2 hijos por pareja
    for i, p in enumerate(parents):
        children[2*i], children[2*i+1] = crossover(p[0], p[1])

    return children
        
def new_generation(birds, settings):
    """
    Produce una nueva generación de pájaros.

    Parámetros
    ----------
    birds : list
        Lista de objetos `Bird` a seleccionar y reproducir.

    settings : dict
        Diccionario con parámetros de configuración.

    Salida
    ------
    children : tuple
        Tupla de la forma (e, h, n), donde e es una lista de pájaros élite,
        h de los pájaros productos de crossover, y n de pájaros normales.        
    """

    MUTATION = settings['MUTATION'] # Tasa de mutación
    CROSSOVER = settings['CROSSOVER'] # Tasa de crossover
    ELITISM = settings['ELITISM'] # Tasa de elitismo
    SELECTION = settings['SELECTION'] # Método de selección
    CONTESTANTS = settings['CONTESTANTS'] # Participantes en selección por torneo
    fitness = [b.fitness for b in birds]
    sorted_index = np.argsort(fitness)[::-1] # Índices ordenados por fitness descendiente

    # Élites
    num_elite = int(len(sorted_index)*ELITISM)
    elite_index = sorted_index[:num_elite]
    if num_elite == 0:
        elites = []
    elif num_elite == 1: # Si solo hay un índice, no podemos usar `itemgetter`
        elites = [birds[elite_index[0]]]
    else:
        elites = list(itemgetter(*elite_index)(birds))
    elites = [b.network.encode() for b in elites]
    
    # Hijos
    to_breed = int(CROSSOVER * len(birds)/2) # Número de parejas a seleccionar
    children = breed_parents(birds, to_breed, SELECTION, CONTESTANTS)
    num_children = len(children)
    
    # Normales
    missing = len(birds) - num_elite - num_children # Los normales son todos los que faltan
    normals = np.random.choice(birds, missing) # Escogidos de manera aleatoria
    normals = [b.network.encode() for b in normals]
    
    # Mutación
    to_mutate = children + normals # Los élites no mutan

    # Número de mutaciones en el **genoma total** (NO el número de individuos)
    mutation_number = int(MUTATION * len(to_mutate) * len(to_mutate[0])) 

    # Escogemos cromosomas aleatorios a mutar
    mutated_inds = np.random.randint(0, len(to_mutate)-1, mutation_number) 
    # Escogemos genes para cada cromosoma
    mutated_genes = np.random.randint(0, len(to_mutate[0])-1, mutation_number)
    for i,j in zip(mutated_inds, mutated_genes):
        to_mutate[i][j] += np.random.normal() # Ruido gaussiano
        
    # Unión
    return [birds[0].network.decode(b) for b in elites], \
           [birds[0].network.decode(b) for b in to_mutate[:num_children]], \
           [birds[0].network.decode(b) for b in to_mutate[num_children:]]