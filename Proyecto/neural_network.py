"""
Este archivo implementa clases para definir redes neuronales, y sus operaciones
relacionadas.
"""

import numpy as np
from functools import reduce
import random

from copy import copy
from itertools import islice

def evaluate(a, b):
    return b(a)

def ident(x):
    return x

class Layer:
    """
    Clase que representa una capa de la red neuronal.

    Parámetros
    ----------
    a, b : {int, numpy.array}
        - Si son enteros, `a` es el número de entradas, y b el número de salidas.
        - Si son arreglos de numpy, `a` corresponde a `self.W` y `b` a `self.b`

    f : callable
        Función de activación de la capa. 

    Atributos
    ---------
    W : numpy.array
        Arreglo de la forma  `m x n`, donde `n` es el número de entradas a la capa
        y `m` el número de salidas. La entrada W[i,j] representa el j-ésimo peso
        de la i-ésima neurona.

    b : numpy.array
        Arreglo unidimensional de tamaño `m`. La entrada b[i] representa el bias
        de la i-ésima neurona.

    f : callable
        Función de activación de la capa.
    """
    def __init__(self, a, b, f=ident):
        if isinstance(a, int):
            self.W = np.random.normal(size=(b, a))
            self.b = np.random.normal(size=b)
        else:
            self.W = a
            self.b = b
        self.f = f

    def __call__(self, x):
        return self.f(self.W @ x + self.b)
        
    def __copy__(self):
        W = copy(self.W)
        b = copy(self.b)
        f = copy(self.f)
        return Layer(W, b, f)

    def __str__(self): 
        return "weights: " + str(self.W) +"\nbias: " + str(self.b)

    def __repr__(self): 
        return str(self)
    
    def __add__(self, other):
        return Layer(self.W + other.W, self.b + other.b, self.f)
    
    def __mul__(self, other):
        return Layer(other*self.W, other*self.b, self.f)
    
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        return Layer(self.W/other, self.b/other, self.f)
    
    def __floordiv__(self, other):
        return Layer(self.W//other, self.b//other, self.f)
    
    def __len__(self):
        return self.W.shape[0]*self.W.shape[1] + len(self.b)
    
    def __eq__(self, other):
        return self.f == other.f and (self.W == other.W).all() and (self.b == other.b).all()
                    
    def encode(self):
        """
        Codifica la capa en un vector unidimensional.

        Salida
        ------
        encoded : numpy.array
            Vector unidimensional compuesto de todas las entradas de `self.W`, 
            concatenadas columna por columna, seguido de todas las entradas de
            `self.b`. 
        """
        return np.concatenate([self.W.flatten(), self.b])
        
    def decode(self, sequence):
        """
        Decodifica una capa codificada

        Parámetros
        ----------
        sequence : numpy.array
            Secuencia a decodificar. Debe tener un total de `m*n + b` entradas,
            donde `m` y `n` son las dimensiones de `self.W` y `b` la dimensión
            de `self.b`.

        Salida
        ------
        decoded : Layer
            Capa con las entradas del vector decodificado como pesos y bias.
        """
        W_size = self.W.shape[0]*self.W.shape[1]
        W = sequence[:W_size].reshape(self.W.shape).copy()
        b = sequence[W_size:].copy()
        decoded = Layer(W, b, self.f)
        return decoded
            

class NeuralNet:
    """
    Clase que representa una red neuronal.

    Parámetros
    ----------
    layers : list
        - Si es una lista de enteros, cada entrada representa el tamaño de una
          de las capas, en orden de entrada -> salida.
        - Si es una lista de objetos `Layer`, cada entrada es una capa diferente.

    activation_functions : list
        Lista de funciones de activación de cada capa, en orden entrada -> salida.

    last_activation : callable = ident
        Función de activación de la última capa.

    Atributos
    ---------
    layers : list
        Lista de objetos `Layer`. Cada uno representa una capa en orden
        entrada -> salida.

    f : callable
        Función de activación de la última capa.
    """
    def __init__(self, layers, activation_functions=None, last_activation=ident):
        if isinstance(layers[0], Layer):
            self.layers = layers
        else:
            self.layers = [Layer(conf_layer1, conf_layer2, ac_fun) \
                           for conf_layer1, conf_layer2, ac_fun \
                           in zip(layers, layers[1:], activation_functions)]
        self.f = last_activation
        
    def __call__(self, x):
        return self.f(reduce(evaluate, self.layers, x))
        
    def __str__(self):
        s = ""
        for i, layer in enumerate(self.layers):
            s = "%sLayer %d:\n%s\n\n" % (s, i, str(layer))
        return s

    def __repr__(self):
        return str(self)
    
    def __add__(self, other):
        new_layers = [a+b for a, b in zip(self.layers, other.layers)]
        return NeuralNet(new_layers, last_activation=self.f)
    
    def __mul__(self, other):
        new_layers = [l*other for l in self.layers]
        return NeuralNet(new_layers, last_activation=self.f)
    
    __rmul__ = __mul__
    
    def __truediv__(self, other):
        new_layers = [l/other for l in self.layers]
        return NeuralNet(new_layers, last_activation=self.f)
    
    def __floordiv__(self, other):
        new_layers = [l//other for l in self.layers]
        return NeuralNet(new_layers, last_activation=self.f)
    
    def __eq__(self, other):
        return self.f == other.f and all([l1 == l2 for l1, l2 in zip(self.layers, other.layers)])
            
    def encode(self):
        """
        Codifica la red neuronal en un vector unidimensional.

        Salida
        ------
        encoded : numpy.array
            Vector unidimensional obtenido al concatenar el cromosoma codificado
            de cada capa, en orden entrada -> salida. Véase `Layer.encode` para
            más detalles
        """
        layers = [l.encode() for l in self.layers]
        return np.concatenate(layers)
    
    def decode(self, sequence):
        """
        Decodifica el vector codificado de una red neuronal.

        Parámetros
        ----------
        sequence : list-like
            Vector a decodificar. Debe tener dimensión `l1 + l2 + ... + ln`, donde
            `li` es el tamaño de la i-ésima capa de la red.

        Salida
        ------
        decoded : NeuralNet
            Red neuronal con las capas detalladas en el vector codificado.
        """
        seq = iter(sequence)
        sizes = [len(l) for l in self.layers]
        layers_enc = [np.array(list(islice(seq, i))) for i in sizes]
        layers = [l.decode(e) for e,l in zip(layers_enc, self.layers)]
        return NeuralNet(layers, last_activation=self.f)