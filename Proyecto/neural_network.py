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
        return Layer(W.shape[1], W.shape[0], f, W, b)

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
        return np.concatenate([self.W.flatten(), self.b])
        
    def decode(self, sequence):
        W_size = self.W.shape[0]*self.W.shape[1]
        W = sequence[:W_size].reshape(self.W.shape).copy()
        b = sequence[W_size:].copy()
        return Layer(W, b, self.f)
            

class NeuralNet:
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

    def __invert__(self): # ~NN
        return mutation(self)
    
    def __copy__(self):
        pass
    
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
        layers = [l.encode() for l in self.layers]
        return np.concatenate(layers)
    
    def decode(self, sequence):
        seq = iter(sequence)
        sizes = [len(l) for l in self.layers]
        layers_enc = [np.array(list(islice(seq, i))) for i in sizes]
        layers = [l.decode(e) for e,l in zip(layers_enc, self.layers)]
        return NeuralNet(layers, last_activation=self.f)