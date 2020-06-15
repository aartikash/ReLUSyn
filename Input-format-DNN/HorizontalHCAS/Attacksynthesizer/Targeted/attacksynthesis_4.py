import numpy as np
import sys
import time
import glog
from gurobipy import *

def find_delta(inputs_to_change):
    start = time.process_time()
    
    f = open("../../HCAS_rect_v6_pra0_tau00_25HU_3000.nnet", "r")
    
    in_line = f.readline()
    while in_line[0:2] == "//":
        in_line = f.readline()

    numLayers, inputSize, outputSize, _ = [int(x) for x in in_line.strip().split(",")[:-1]]

    in_line = f.readline()
    layerSizes = [int(x) for x in in_line.strip().split(",")[:-1]]

    in_line = f.readline()
    symmetric = int(in_line.strip().split(",")[0])

    in_line = f.readline()
    inputMinimums = [float(x) for x in in_line.split(",")]

    in_line = f.readline()
    inputMaximums = [float(x) for x in in_line.split(",")]

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
            in_line = f.readline()
            aux = [float(x) for x in in_line.strip().split(",")[:-1]]
            for j in range(previousLayerSize):
                weights[layernum][i][j] = aux[j]
        biases[layernum] = np.zeros(currentLayerSize)
        for i in range(currentLayerSize):
            in_line = f.readline()
            x = float(in_line.strip().split(",")[0])
            biases[layernum][i] = x

    f.close()
    nn = Model()
    
    inputs = nn.addVars(inputSize, name="inputs", lb=inputMinimums, ub=inputMaximums)
    deltas = nn.addVars(inputSize, name="deltas")
    absDeltas = nn.addVars(inputSize, name="absDeltas")
    inputsN = nn.addVars(inputSize, name="inputsN")

    input_vals = [3919.704054253667, 0.0, 2.2683915791388873]
    
    for i in range(inputSize):
        nn.addConstr(inputs[i] == input_vals[i] + deltas[i])
        nn.addConstr(absDeltas[i] == abs_(deltas[i]))
        if i not in inputs_to_change:
            nn.addConstr(deltas[i] == 0)
  
    for i in inputs_to_change:
        #bound = (inputMaximums[i] - inputMinimums[i]) / 2
        #final_bound = min(bound, max_deltas)
        #deltas[i].lb = -1.0 * final_bound
        #deltas[i].ub = final_bound
        deltas[i].lb = inputMinimums[i] - input_vals[i]
        deltas[i].ub = inputMaximums[i] - input_vals[i]

    for i in range(inputSize):
        nn.addConstr(inputsN[i] == (inputs[i]-inputMeans[i])/inputRanges[i])

    layerOuts = {}
    layerOuts[1] = nn.addVars(layerSizes[1], name="layerOuts[1]", lb=-GRB.INFINITY, ub=GRB.INFINITY)

    layerReluOuts = {}
    layerReluOuts[1] = nn.addVars(layerSizes[1], name="layerReluOuts[1]", lb=0, ub=GRB.INFINITY)
    
    nn.update()
    
    temp = []
    for i in range(layerSizes[1]):
        expr = LinExpr()
        for j in range(layerSizes[0]):
            expr.add(inputsN[j], weights[0][i][j])
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

    nn.addConstr(denormalizedOuts[0] <= denormalizedOuts[1])
    nn.addConstr(denormalizedOuts[0] <= denormalizedOuts[2])
    nn.addConstr(denormalizedOuts[0] <= denormalizedOuts[3])
    nn.addConstr(denormalizedOuts[0] <= denormalizedOuts[4])

    nn.setObjective(quicksum(absDeltas))
    
    nn.Params.OutputFlag = False
    
    middle = time.process_time()
    nn.optimize()
    end = time.process_time()
    
    if nn.status == GRB.Status.OPTIMAL:
        glog.info([inputs[i].X for i in range(inputSize)])
        glog.info([denormalizedOuts[i].X for i in range(outputSize)])
        output = []
        output.append([denormalizedOuts[i].X for i in range(outputSize)])
        for i in inputs_to_change:
            output.append([i, deltas[i].X, 'Y', end-middle])
        return output
    else:
        output = []
        for i in inputs_to_change:
            output.append([i, 0, 0, 'N', end-middle])
        return output
