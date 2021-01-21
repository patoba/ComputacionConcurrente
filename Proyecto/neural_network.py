import numpy as np
from functools import reduce
from genetic_algorithm import mutation, crossover_product
from copy import copy
from multipledispatch import multifunction, multimethod


evaluate = lambda a, b : b(a)
id = lambda x : x

class Layer:

    @multimethod(None, int, int, None)
    def __init__(self, num_in, num_out, f = id):
        self.W = np.random.normal(size=(num_out, num_in))
        self.b = np.random.normal(size=num_out)
        self.f = f

    @__init__.dispatch(None, np.ndarray, np.ndarray, None)
    def __init__(self, W, b, f):
        self.W = W
        self.b = b
        self.f = f

    def __call__(self, x):
        return self.f(self.W @ x + self.b)

    def __invert__(self): # ~NN
        return mutation(self)
        
    def __copy__(self):
        W = copy(self.W)
        b = copy(self.b)
        f = copy(self.f)
        return Layer(W.shape[1], W.shape[0], f, W, b)

    def __str__(self): # falta definir
        pass

    def __repr__(self): # falta definir
        pass

class NeuralNet:
    def __init__(self, configuration_layers, activiation_functions, last_activation_funct = id):
        """
        configuration_layers: list of the numbers of neurons in each layer. Must contain the number of features of the input vector.
        activation_functions: list of the activations functions of each layer. 
        """
        self.layers = [Layer(conf_layer1, conf_layer2, ac_fun) for conf_layer1, conf_layer2, ac_fun in zip(configuration_layers, configuration_layers[1:], activiation_functions)]
        self.f = last_activation_funct
        
    def __call__(self, x):
        return self.f(reduce(evaluate, self.layers, x))

    def __invert__(self): # ~NN
        return mutation(self)

    def __matmul__(self, other): # NN1 @ NN2
        return crossover_product(self, other)

    def __copy__(self):
        pass
    
    def __str__(self):
        s = ""
        for i, layer in enumerate(self.layers):
            s = "%slayer #%d\n%s\n" % (s, i, str(layer))
        return s

    def __repr__(self):
        s = ""
        for i, layer in enumerate(self.layers):
            s = "%slayer #%d\n%s\n" % (s, i, repr(layer))
        return s

if __name__ == "__main__":
    sigmoide = lambda x : 1 / (1 + np.exp(-x)) 
    configuration_layers = [2, 6, 1]
    activiation_functions = [sigmoide] * 2
    last_activiation = lambda x : x[0] > 0.5
    nn = NeuralNet(configuration_layers, activiation_functions, last_activiation)
    x = np.random.rand(configuration_layers[0])
    print(x)
    print(nn(x))

