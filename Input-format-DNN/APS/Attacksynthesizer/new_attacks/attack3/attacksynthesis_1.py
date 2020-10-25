#import csv
import sys
import time
from gurobipy import *

def find_delta(net_file, in_file, inputs_to_change, out_file, out_ub):
    start = time.time()
    
    f = open(net_file, "r")
    
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
    # print(count)
    f.close()
    
    nn = Model()
    
    inputs = nn.addVars(num_inputs)
    deltas = nn.addVars(num_inputs, ub=5)
    absDeltas = nn.addVars(num_inputs)
    
    f = open(in_file, 'r')
    
    for i in range(num_inputs):
        input_val = float(f.readline())
        nn.addConstr(inputs[i] == input_val)
        deltas.lb = max(-input_val, -5)
        nn.addConstr(absDeltas[i] == abs_(deltas[i]))
        if i not in inputs_to_change:
            nn.addConstr(deltas[i] == 0)
    
    f.close()
    
    layerOuts = {}
    layerReluOuts = {}
    
    expr = LinExpr()
    
    for i in range(num_layers):
        layerOuts[i] = nn.addVars(num_neurons[i], lb=-GRB.INFINITY)
        layerReluOuts[i] = nn.addVars(num_neurons[i])
    
    outputs = nn.addVars(num_outputs)
    outputs[0].ub = out_ub
    
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
    
    output_val = 0
    with open(out_file, 'r') as temp:
        output_val = float(temp.readline())
        nn.addConstr(outputs[0] >= output_val + 20)

    nn.setObjectiveN(-outputs[0], 0, priority=1)
    nn.setObjectiveN(quicksum(absDeltas), 1, priority=0)
    
    nn.Params.OutputFlag = False
    
    middle = time.time()
    nn.optimize()
    end = time.time()
    
    if nn.status == GRB.Status.OPTIMAL:
        #print('Output for the given inputs is ' + str(outputs[0].X))
        #print('Delta ' + str(input_to_change) + ' is ' + str(deltas[input_to_change].X))
        #print('Time to solve model is ' + str(end-middle) + ' seconds')
        #with open(result_file + str(input_to_change) + ".csv", 'w') as f:
        #    writer = csv.writer(f)
        #    writer.writerow([deltas[input_to_change].X, outputs[0].X, 'Y', end-middle])
        output = []
        for i in inputs_to_change:
            output.append([i, deltas[i].X, outputs[0].X-output_val, 'Y', end-middle])
        return output
    else:
        #nn.computeIIS()
        #nn.write('model.ilp')
        #with open('attacksynthesis_1_input0.csv', 'w') as f:
        #    writer = csv.writer(f)
        #    writer.writerow([0, 0, 'N', end-middle])
        output = []
        for i in inputs_to_change:
            output.append([i, 0, 0, 'N', end-middle])
        return output
