"""
Este archivo contiene utilidades para entrenar muchas generaciones de pájaros
de una manera concurrente
"""

import neural_network as nn
import bird as fb
import genetic_algorithm as ga
import numpy as np
import multiprocess as mp # ¡multiprocess, NO multiprocessING! 

def wrapper(w): # Para poder llamar el método `play` en una pool
    return w.play()

def chunks(a, n): # Separa una lista en pedazos de tamaño n
    for i in range(0, len(a), n):
        yield a[i:i + n]
        
def best_world(birds, settings, n_birds=1):
    """
    Genera un mundo con los mejores individuos de una generación.
    
    Parámetros
    ----------
    birds : list
        Lista de objetos tipo Bird, después de haber sido ejecutados (i.e., con fitness evaluada).
        
    n_birds : int = 1
        Número de pájaros que el nuevo mundo tendrá.
        
    Salida
    ------
    final_world : World
        Mundo nuevo con `n_birds` pájaros con la mayor fitness.
    """
    fit = [b.fitness for b in birds]
    final_birds = np.array(birds)[np.argsort(fit)[:-n_birds-1:-1]]
    final_networks = [b.network for b in final_birds]
    final_world = fb.World(final_networks, settings)
    return final_world
        
class Trainer:
    """
    Clase utilizada para realizar simulaciones de entrenamiento con distinto número de pájaros, procesadores
    y generaciones.
    
    Atributos
    ---------
    settings : dict
        Diccionario con las configuraciones para todos los objetos dependientes.
        
    processes : int
        Número de procesos a crear. Cada proceso se encarga de simular un mundo separado, después de lo cual
        se unen los resultados y se selecciona la nueva generación
    
    birds : int
        Número de pájaros que tendrá cada mundo. Esto significa que si se crean `p` procesos, habrá un total
        de `p * birds` pájaros simulados. 
    """
    def __init__(self, settings, birds, processes):
        self.settings = settings
        self.birds = birds
        self.processes = processes
        
    def random_nets(self):
        """
        Inicializa redes neurales aleatorias que sean compatibles con los parámetros dados.
        
        Salida
        ------
        nets : list
            Lista de `self.birds` redes aleatorias.
        """
        LAYER_SIZES = self.settings['LAYER_SIZES']
        ACTIVATION_FUNCTIONS = self.settings['ACTIVATION_FUNCTIONS']
        LAST_ACTIVATION = self.settings['LAST_ACTIVATION']
        tot = int(self.birds//self.processes)
        return [nn.NeuralNet(LAYER_SIZES, ACTIVATION_FUNCTIONS, LAST_ACTIVATION) 
                for _ in range(tot)]
    
    def run_generation(self, nets=None):
        """
        Ejecuta una generación de pájaros de manera concurrente.
        
        Parámetros
        ----------
        nets : list = None
            Lista de redes a usar para los pájaros. Si es `None`, se generan redes aleatorias.
            
        Salida
        ------
        final_birds : list
            Lista de pájaros correspondientes a la última generación.
        """
        LAYER_SIZES = self.settings['LAYER_SIZES']
        ACTIVATION_FUNCTIONS = self.settings['ACTIVATION_FUNCTIONS']
        LAST_ACTIVATION = self.settings['LAST_ACTIVATION']
        if nets is None:
            nets = [[nn.NeuralNet(LAYER_SIZES, ACTIVATION_FUNCTIONS, LAST_ACTIVATION)] for _ in range(self.birds)]
        worlds = [fb.World(n, self.settings) for n in nets]
        pool = mp.Pool(self.processes)
        birds_split = pool.map(wrapper, worlds)
        pool.close()
        final_birds = [b for birds in birds_split for b in birds]
        return final_birds
    
    def run_generation_old(self, nets=None):
        LAYER_SIZES = self.settings['LAYER_SIZES']
        ACTIVATION_FUNCTIONS = self.settings['ACTIVATION_FUNCTIONS']
        LAST_ACTIVATION = self.settings['LAST_ACTIVATION']
        
        if nets is None:
            nets = [self.random_nets() for _ in range(self.processes)]
        worlds = [fb.World(n, self.settings) for n in nets]
        pool = mp.Pool(self.processes)
        birds_split = pool.map(wrapper, worlds)
        pool.close()
        final_birds = [b for birds in birds_split for b in birds]
        return final_birds

    def split_nets(self, gens):
        """
        Divide las redes de una nueva generación en partes iguales para asignarlas a cada proceso.
        
        Parámetros
        ----------
        nets : list
            Lista de redes a distribuir
        
        Salida
        ------
        final_nets : list
            Lista de listas de tamaño `self.processes`, con la misma proporción de pájaros élite, hijos y normales.
            Cada sub-lista contiene `self.birds` redes.
        """
        final_nets = gens[0] + gens[1] + gens[2]
        return [[n] for n in final_nets]
    
    def split_nets_old(self, gens):
        elites = list(chunks(gens[0], len(gens[0])//self.processes))
        children = list(chunks(gens[1], len(gens[1])//self.processes))
        normals = list(chunks(gens[2], len(gens[2])//self.processes))
        return [elites[i] + children[i] + normals[i] for i in range(self.processes)]

    def train(self, generations, max_fitness=None, verbose=False, method='new'):
        """
        Crea una población nueva de pájaros y los entrena.
        
        Parámetros
        ----------
        generations : int
            Número de generaciones a simular
        
        Salida
        ------
        out : tuple
            Tupla de dos elementos. El primero contiene la última población simulada, y el segundo
            una historia de los fitness de cada individuo para cada generación.
        """
        nets = None
        fit = []
        for i in range(generations):           
            if method == 'new':
                birds = self.run_generation(nets)
            elif method == 'old':
                birds = self.run_generation_old(nets)
            fit.append([b.fitness for b in birds])
            avg = np.mean(fit[-1])
            if max_fitness is not None and avg > max_fitness:
                return birds, fit
            nets_bundled = ga.new_generation(birds, self.settings)
            if method == 'new':
                nets = self.split_nets(nets_bundled)
            elif method == 'old':
                nets = self.split_nets_old(nets_bundled)
            if verbose:
                print("Generation: {} Average fitness: {}".format(i, avg), end='\r')
        return birds, fit
