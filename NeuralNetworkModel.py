import numpy
import random


def ReLU(x):
    return x * (x > 0)
VReLU = numpy.vectorize(ReLU)


class NeuralNetwork:

    def __init__(self, inputs, hidden_layers, nodes_per_layer, nodes_in_output, order=None):
        self.hidden_layers = hidden_layers
        self.nodes_per_layer = nodes_per_layer

        if order is None:
            self.weights_hidden_layers = [numpy.random.randn(inputs, nodes_per_layer)/10]\
                                         + [numpy.random.randn(nodes_per_layer, nodes_per_layer)/10 for i in range(hidden_layers-1)]\
                                         + [numpy.random.randn(nodes_per_layer, nodes_in_output)/10]

            self.biases_hidden_layers = [numpy.random.randn(1, nodes_per_layer)/10 for i in range(hidden_layers)]\
                                         + [numpy.random.randn(1, nodes_in_output)/10]
        else:

            self.weights_hidden_layers = []
            self.biases_hidden_layers = []
            self.weights_hidden_layers.append(numpy.array(order[0:inputs * nodes_per_layer]).reshape(inputs, nodes_per_layer))

            start = inputs * nodes_per_layer
            nodes_per_layer_squared = nodes_per_layer * nodes_per_layer
            for i in range(hidden_layers):
                self.biases_hidden_layers.append(numpy.array(order[start:start+nodes_per_layer]))
                start += nodes_per_layer
                if i < hidden_layers-1:
                    self.weights_hidden_layers.append(numpy.array(order[start:start+nodes_per_layer_squared]).reshape(nodes_per_layer, nodes_per_layer))
                    start += nodes_per_layer_squared
                else:
                    self.weights_hidden_layers.append(numpy.array(order[start:start+nodes_in_output*nodes_per_layer]).reshape(nodes_per_layer, nodes_in_output))
                    start += nodes_per_layer* nodes_in_output

            self.biases_hidden_layers.append(numpy.array(order[start:start+nodes_in_output]))



    def predict(self, inputs):
        currvals = numpy.array(inputs)

        for i in range(self.hidden_layers):
            currvals = numpy.tanh((numpy.add(numpy.dot(currvals,self.weights_hidden_layers[i]), self.biases_hidden_layers[i]).reshape(1,self.nodes_per_layer)))
        return numpy.tanh((numpy.add(numpy.dot(currvals, self.weights_hidden_layers[self.hidden_layers]), self.biases_hidden_layers[self.hidden_layers]).tolist()[0]))