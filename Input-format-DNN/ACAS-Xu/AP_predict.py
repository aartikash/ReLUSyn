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
            weights[layernum][i][j] = aux[j]
    biases[layernum] = np.zeros(currentLayerSize)
    for i in range(currentLayerSize):
        in_line = f.readline()
        x = float(in_line.strip().split(",")[0])
        biases[layernum][i] = x

nn = Model()

inputs = nn.addVars(inputSize, name="inputs", lb=-GRB.INFINITY, ub=GRB.INFINITY)
deltas = nn.addVars(inputSize, name="deltas", lb=0, ub=0)
deltas[1].lb = -3.141593
deltas[1].ub = 3.141593
absDeltas = nn.addVars(inputSize, name="absDeltas")
inputsM = nn.addVars(inputSize, name="inputsM", lb=-GRB.INFINITY, ub=GRB.INFINITY)

input_vals = [500.0,0.0,0.0,100.0,100.0]
for i in range(inputSize):
    nn.addConstr(inputs[i] == input_vals[i] + deltas[i])
    nn.addConstr(absDeltas[i] == abs_(deltas[i]))

for i in range(inputSize):
    #if input_vals[i] < inputMinimums[i]:
    #    nn.addConstr(inputsM[i] == (inputMinimums[i]-inputMeans[i])/inputRanges[i])
    #elif input_vals[i] > inputMaximums[i]:
    #    nn.addConstr(inputsM[i] == (inputMaximums[i]-inputMeans[i])/inputRanges[i])
    #else:
    #    nn.addConstr(inputsM[i] == (input_vals[i]-inputMeans[i])/inputRanges[i])

    #nn.addConstr(inputsM[i] == input_vals[i])
    nn.addConstr(inputsM[i] == (inputs[i]-inputMeans[i])/inputRanges[i])

layerOuts = {}
layerOuts[1] = nn.addVars(layerSizes[1], name="layerOuts[1]", lb=-GRB.INFINITY, ub=GRB.INFINITY)

layerReluOuts = {}
layerReluOuts[1] = nn.addVars(layerSizes[1], name="layerReluOuts[1]", lb=0, ub=GRB.INFINITY)

nn.update()

temp = []
for i in range(layerSizes[1]):
    expr = LinExpr()
    for j in range(layerSizes[0]):
        expr.add(inputsM[j], weights[0][i][j])
        #expr.add(deltasM[j], weights[0][i][j])
    temp.append(expr)

nn.addConstrs(layerOuts[1][i] == temp[i] + biases[0][i] for i in range(layerSizes[1]))
nn.addConstrs(layerReluOuts[1][i] == max_(layerOuts[1][i], 0) for i in range(layerSizes[1]))

for layernum in range(2, numLayers):
    layerOuts[layernum] = nn.addVars(layerSizes[layernum], name="layerOuts[" + str(layernum) + "]", lb=-GRB.INFINITY, ub=GRB.INFINITY)
    layerReluOuts[layernum] = nn.addVars(layerSizes[layernum], name="layerReluOuts[" + str(layernum) + "]", lb=0, ub=GRB.INFINITY)
    nn.update()
    temp = []
    for i in range(layerSizes[layernum]):
        expr = LinExpr()
        for j in range(layerSizes[layernum-1]):
            expr.add(layerReluOuts[layernum-1][j], weights[layernum-1][i][j])
        temp.append(expr)
    nn.addConstrs(layerOuts[layernum][i] == temp[i] + biases[layernum-1][i] for i in range(layerSizes[layernum]))
    nn.addConstrs(layerReluOuts[layernum][i] == max_(layerOuts[layernum][i], 0) for i in range(layerSizes[layernum]))

outputs = nn.addVars(layerSizes[-1], name="outputs", lb=-GRB.INFINITY, ub=GRB.INFINITY)
nn.update()

temp = []
for i in range(layerSizes[-1]):
    expr = LinExpr()
    for j in range(layerSizes[-2]):
        expr.add(layerReluOuts[numLayers-1][j], weights[-1][i][j])
    temp.append(expr)

nn.addConstrs(outputs[i] == temp[i] + biases[-1][i] for i in range(layerSizes[-1]))

denormalizedOuts = nn.addVars(outputSize, lb=-GRB.INFINITY, ub=GRB.INFINITY)
for i in range(outputSize):
    nn.addConstr(denormalizedOuts[i] == outputs[i] * inputRanges[-1] + inputMeans[-1])

nn.Params.OutputFlag = False
nn.addConstr(denormalizedOuts[0] >= 270.6)
nn.setObjective(quicksum(absDeltas))
nn.optimize()

if nn.status == GRB.Status.OPTIMAL:
    print('optimal solution found!')
    for i in range(inputSize):
        print('Input ' + str(i) + ' is ' + str(inputs[i].X))
        print('Delta ' + str(i) + ' is ' + str(deltas[i].X))
        print('InputM ' + str(i) + ' is ' + str(inputsM[i].X))
    for i in range(outputSize):
        print('Output ' + str(i) + ' is ' + str(denormalizedOuts[i].X))
