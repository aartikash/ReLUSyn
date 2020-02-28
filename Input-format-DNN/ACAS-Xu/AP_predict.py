#This code parses the .nt files for further progress
import sys
import numpy as np
from gurobipy import *

#read from the nt files

f = open("nnet/ACASXU_run2a_1_1_batch_2000.nnet", "r")

count = 0

in_line = f.readline()

while in_line[0:2] == "//":
    in_line = f.readline()
    #if in_line.startswith('//'):
    #    in_line = f.readline()
    #else:
    #    break

numLayers, inputSize, outputSize, _ = [int(x) for x in in_line.strip().split(",")[:-1]]

in_line = f.readline()
layerSizes = [int(x) for x in in_line.strip().split(",")[:-1]]

in_line = f.readline()
symmetric = int(in_line.strip().split(",")[0])

in_line = f.readline()
inputMinimums = [float(x) for x in in_line.split(",")[:-1]]

in_line = f.readline()
inputMaximums = [float(x) for x in in_line.split(",")[:-1]]

in_line = f.readline()
inputMeans = [float(x) for x in in_line.split(",")[:-1]]

in_line = f.readline()
inputRanges = [float(x) for x in in_line.strip().split(",")[:-1]]

weights = []
biases = []

for layernum in range(numLayers):
    previousLayerSize = layerSizes[layernum]
    currentLayerSize = layerSizes[layernum+1]
    weights.append([])
    biases.append([])
    weights[layernum] = np.zeros((currentLayerSize, previousLayerSize))
    for i in range(currentLayerSize):
        in_line=f.readline()
        aux = [float(x) for x in in_line.strip().split(",")[:-1]]
        for j in range(previousLayerSize):
            weights[layernum][i,j] = aux[j]
    biases[layernum] = np.zeros(currentLayerSize)
    for i in range(currentLayerSize):
        in_line = f.readline()
        x = float(in_line.strip().split(",")[0])
        biases[layernum][i] = x



"""read_nums = in_line.split(',')
read_nums = read_nums[0:-1]

num_inputs = int(read_nums[1])
num_outputs = int(read_nums[2])
num_layers = int(read_nums[0]) - 1

in_line = f.readline()
read_nums = in_line.split(',')
read_nums = read_nums[0:-1]

num_neurons = []
for i in range(1, len(read_nums)-1):
    num_neurons.append(int(read_nums[i]))

inputs_min = []
inputs_max = []

in_line = f.readline()

in_line = f.readline()
read_nums = in_line.split(',')
read_nums = read_nums[0:-1]

#print(num_inputs)
#print(read_nums)
for i in range(num_inputs):
    inputs_min.append(float(read_nums[i]))

in_line = f.readline()
read_nums = in_line.split(',')
read_nums = read_nums[0:-1]

for i in range(num_inputs):
    inputs_max.append(float(read_nums[i]))

in_line = f.readline()
in_line = f.readline()

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

with open('temp.txt', 'w') as out:
    for in_line in f:
        read_nums = in_line.split(',')
        read_nums = read_nums[0:-1]
        for num in read_nums:
            out.write(num + '\n')

f.close()

f = open('temp.txt', 'r')

for i in range(num_inputs):
    for j in range(num_neurons[0]):
        weights[0][j].append(float(f.readline()))

#for i in range(num_neurons[0]):
#    for j in range(num_inputs):
#        weights[0][i].append(float(f.readline()))

for i in range(num_neurons[0]):
    biases[0].append(float(f.readline()))


for i in range(1, num_layers):
    for j in range(num_neurons[i-1]):
        for k in range(num_neurons[i]):
           weights[i][k].append(float(f.readline()))
    for j in range(num_neurons[i]):
        biases[i].append(float(f.readline()))

#for i in range(1, num_layers):
#    for j in range(num_neurons[i]):
#        for k in range(num_neurons[i-1]):
#            weights[i][j].append(float(f.readline()))
#    for j in range(num_neurons[i]):
#        biases[i].append(float(f.readline()))

for i in range(num_neurons[-1]):
    for j in range(num_outputs):
        weights[-1][j].append(float(f.readline()))

for i in range(num_outputs):
    biases[-1].append(float(f.readline()))


#for i in range(num_outputs):
#    for j in range(num_neurons[-1]):
#        weights[-1][i].append(float(f.readline()))
#        count += 1

#for i in range(num_outputs):    
#    biases[-1].append(float(f.readline()))

# This checks that the correct number of lines were parsed
# print(count)

f.close()"""
nn = Model()

#inputs = nn.addVars(num_inputs, name="inputs")
#deltas = nn.addVars(num_inputs, lb=-GRB.INFINITY, name="deltas")

inputsM = nn.addMVar(num_inputs, name="inputs", lb=-GRB.INFINITY, ub=GRB.INFINITY)
deltasM = nn.addMVar(num_inputs, name="deltas", lb=0, ub=0)

#for i in range(num_inputs):
    #inputs[i].lb = inputs_min[i]
    #inputs[i].ub = inputs_max[i]
    #nn.addConstr(deltas[i] == 0)

#for i in range(1, num_inputs):
#    nn.addConstr(inputs[i] == 0)

#layerOuts = {}
#layerReluOuts = {}

layerReluOuts = {}

layerReluOuts[1] = nn.addMVar(layerSizes[1], name="layerReluOuts[1]", lb=0, ub=GRB.INFINITY)
nn.addConstr(layerReluOuts[1] == np.maximum(np.dot(weights[0], inputsM+deltasM)+biases[0],0))

for layernum in range(1, numLayers-1):
    layerReluOuts[layernum+1] = nn.addMVar(layerSizes[layernum+1], name="layerReluOuts[" + str(layernum+1) + "]", lb=0, ub=GRB.INFINITY)
    nn.addConstr(layerReluOuts[layernum+1] == np.maximum(np.dot(weights[layernum-1], layerReluOuts[layernum])+deltas[layernum-1], 0))

outputs = nn.addMVar(layerSizes[-1], name="outputs", lb=0, ub=GRB.INFINITY)
nn.addConstr(outputs == np.dot(weights[-1], layerReluOuts[numLayers-1])+biases[-1])

#expr = LinExpr()

#layerOuts = nn.addVars(num_layers, num_neurons[0], name="layerOuts")
#layerReluOuts = nn.addVars(num_layers, num_neurons[0], name="layerReluOuts")

#for i in range(numLayers-1):
#    layerReluOuts = 

#for i in range(num_layers):
#    layerOuts[i] = nn.addVars(num_neurons[i], name="layerOuts")
#    layerReluOuts[i] = nn.addVars(num_neurons[i], name="layerReluOuts")

#print(layerOuts)

#outputs = nn.addVars(num_outputs, lb=-GRB.INFINITY, name="outputs")

#absSlacks = nn.addVars(sum(num_neurons) + num_outputs)
#slacks = nn.addVars(sum(num_neurons) + num_outputs, lb=-GRB.INFINITY)

#f = open('output.txt', 'r')

#for i in range(num_inputs):
#    f.readline()
#    f.readline()

#for i in range(num_outputs):
#    f.readline()

#for i in range(sum(num_neurons) + num_outputs):
#    nn.addConstr(slacks[i] == float(f.readline()))
#    nn.addConstr(absSlacks[i] == abs_(slacks[i]))

#for i in range(sum(num_neurons) + num_outputs):
#    nn.addConstr(absSlacks[i] == abs_(slacks[i]))

#sum_neurons = [sum(num_neurons[0:i]) for i in range(len(num_neurons)+1)]

#"""for i in range(num_neurons[0]):
#    expr = LinExpr()
#    for j in range(num_inputs):
#        expr.add(inputs[j], weights[0][i][j])
#        expr.add(deltas[j], weights[0][i][j])
#    expr.addConstant(biases[0][i])
#    nn.addConstr(layerOuts[0,i] + slacks[sum_neurons[0] + i] == expr)
#    nn.addConstr(layerReluOuts[0,i] == max_(0, layerOuts[0,i]))

#for i in range(1, num_layers):
#    for j in range(num_neurons[i]):
#        expr = LinExpr()
#        for k in range(num_neurons[i-1]):
#            expr.add(layerReluOuts[i-1,k], weights[i][j][k])
#        expr.addConstant(biases[i][j])
#        nn.addConstr(layerOuts[i,j] + slacks[sum_neurons[i] + j] == expr)
#        nn.addConstr(layerReluOuts[i,j] == max_(0, layerOuts[i,j]))
#
#for i in range(num_outputs):
#    expr = LinExpr()
#    for j in range(num_neurons[-1]):
#        expr.add(layerReluOuts[num_layers-1,j], weights[num_layers][i][j])
#    expr.addConstant(biases[num_layers][i])
#    nn.addConstr(outputs[i] + slacks[sum_neurons[-1] + i] == expr)

#TODO: Add code here that allows us to set values for inputs
#nn.setObjective(quicksum(absSlacks))"""

nn.Params.OutputFlag = False
#nn.update()
#print(nn.getVars())
#nn.write('model.lp')

#nn.Params.DualReductions = 0

nn.optimize()

#print(nn.status)

#f = open('output.txt', 'w')

if nn.status == GRB.Status.OPTIMAL:
    print('optimal solution found!')
    """for i in range(num_inputs):
        #print('Input ' + str(i) + ' is ' + str(inputs[i].X))
        #f.write(str(inputs[i].X) + '\n')
    for i in range(num_inputs):
        #print('Delta ' + str(i) + ' is ' + str(deltas[i].X))
        #f.write(str(deltas[i].X) + '\n')
    for i in range(num_outputs):
        #print('Output ' + str(i) + ' is ' + str(outputs[i].X))
        #f.write(str(outputs[i].X) + '\n')
    for i in range(sum(num_neurons) + num_outputs):
        #print('Slack ' + str(i) + ' is ' + str(slacks[i].X))
        #f.write(str(slacks[i].X) + '\n')"""

#f.close()

#else:
#    nn.computeIIS()
#    nn.write('model.ilp')
