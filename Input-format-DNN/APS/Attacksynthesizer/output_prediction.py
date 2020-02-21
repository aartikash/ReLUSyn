import sys
from gurobipy import *

#Takes in the network file
network_file = sys.argv[1]
#Takes in the input file to the network
input_file = sys.argv[2]
#This points to the index of the files we want to change
input_to_change = sys.argv[3]

#Opens the network file
f = open(network_file, "r")

count = 0

num_inputs = int(f.readline())
num_outputs = int(f.readline())
num_layers = int(f.readline())
num_neurons = []

for i in range(num_layers):
    num_neurons.append(int(f.readline()))

weights = []
for i in range(num_layers):
    weights.append([])
    weights[i] = [[] for j in range(num_neurons[i])]
weights.append([])
weights[-1] = [[] for i in range(num_outputs)]

biases = []
for i in range(num_layers):
    biases.append([])
biases.append([])

for i in range(num_neurons[0]):
    for j in range(num_inputs):
        weights[0][i].append(float(f.readline()))
        count += 1
    biases[0].append(float(f.readline()))
    count += 1

for i in range(1, num_layers):
    for j in range(num_neurons[i]):
        for k in range(num_neurons[i-1]):
            weights[i][j].append(float(f.readline()))
            count += 1
        biases[i].append(float(f.readline()))
        count += 1

for i in range(num_outputs):
    for j in range(num_neurons[-1]):
        weights[-1][i].append(float(f.readline()))
        count += 1
    biases[-1].append(float(f.readline()))
    count += 1

# This checks that the correct number of lines were parsed
print(count)
f.close()

nn = Model()

inputs = nn.addVars(num_inputs, lb=-GRB.INFINITY)
deltas = nn.addVars(num_inputs, lb=-GRB.INFINITY)
absDeltas = nn.addVars(num_inputs)

f = open(input_file, 'r')

for i in range(num_inputs):
    nn.addConstr(inputs[i] == float(f.readline()))
    nn.addConstr(deltas[i] == 0)
    nn.addConstr(absDeltas[i] == abs_(deltas[i]))

f.close()

layerOuts = {}
layerReluOuts = {}

expr = LinExpr()

for i in range(num_layers):
    layerOuts[i] = nn.addVars(num_neurons[i], lb=-GRB.INFINITY)
    layerReluOuts[i] = nn.addVars(num_neurons[i])

outputs = nn.addVars(num_outputs, lb=-GRB.INFINITY)

for i in range(num_neurons[0]):
    expr = LinExpr()
    for j in range(num_inputs):
        expr.add(inputs[j], weights[0][i][j])
        expr.add(deltas[j], weights[0][i][j])
    expr.addConstant(biases[0][i])
    nn.addConstr(layerOuts[0][i] == expr)
    nn.addConstr(layerReluOuts[0][i] == max_(0, layerOuts[0][i]))

for i in range(1, num_layers):
    for j in range(num_neurons[i]):
        expr = LinExpr()
        for k in range(num_neurons[i-1]):
            expr.add(layerReluOuts[i-1][k], weights[i][j][k])
        expr.addConstant(biases[i][j])
        nn.addConstr(layerOuts[i][j] == expr)
        nn.addConstr(layerReluOuts[i][j] == max_(0, layerOuts[i][j]))

for i in range(num_outputs):
    expr = LinExpr()
    for j in range(num_neurons[-1]):
        expr.add(layerReluOuts[num_layers-1][j], weights[num_layers][i][j])
    expr.addConstant(biases[num_layers][i])
    nn.addConstr(outputs[i] == expr)

nn.optimize()

if nn.status == GRB.Status.OPTIMAL:
    print('Output for the given inputs is ' + str(outputs[0].X))
