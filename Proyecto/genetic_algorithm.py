import numpy as np
from neural_network import neural_network

def fitness(neural_net):
    pass

def mutation_layer(W, sigma, I):
    e = np.random.normal(0, I)
    return W + sigma * e

def mutation_neural_net(neural_net, num_generation, I = 2):
    F = fitness(neural_net)
    sigma = np.max(10 / np.log(num_generation * F), 1)
    W = [mutation_layer(layer.W, sigma, I) for layer in neural_net.layers]
    bias = [mutation_layer(layer.b, sigma, I) for layer in neural_net.layers]
    activation_functions = [layer.f for layer in neural_net.layers]
    return neural_network(W, bias, activation_functions, neural_net.f)

def crossover_product(neural_net_a, neural_net_b, t = 0.5):
    return ~ ((1 - t) * neural_net_a + t * neural_net_b )
