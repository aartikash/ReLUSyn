from gurobipy import *

f = open("toynn.nt", "r")

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

nn = Model()

inputs = nn.addVars(num_inputs)
deltas = nn.addVars(num_inputs)
absDeltas = nn.addVars(num_inputs)

layerOuts = {}
layerReluOuts = {}

expr = LinExpr()

for i in range(num_layers):
    layerOuts[i] = nn.addVars(num_neurons[i])
    layerReluOuts[i] = nn.addVars(num_neurons[i])

outputs = nn.addVars(num_outputs)

for i in range(num_neurons[0]):
    expr = LinExpr()
    for j in range(num_inputs):
        expr.add(inputs[j], weights[0][i][j])
        expr.add(deltas[j], weights[0][i][j])
    #expr.addTerms(weights[0][i], inputs.values())
    #expr.addTerms(weights[0][i], deltas.values())
    expr.addConstant(biases[0][i])
    nn.addConstr(layerOuts[0][i] == expr)
    nn.addConstr(layerReluOuts[0][i] == max_(0, layerOuts[0][i]))

for i in range(1, num_layers):
    for j in range(num_neurons[i]):
        expr = LinExpr()
        for k in range(num_neurons[i-1]):
            expr.add(layerReluOuts[i-1][k], weights[i][j][k])
        #expr = LinExpr()
        #expr.addTerms(weights[i][j], layerReluOuts[i-1].values())
        expr.addConstant(biases[i][j])
        nn.addConstr(layerOuts[i][j] == expr)
        nn.addConstr(layerReluOuts[i][j] == max_(0, layerOuts[i][j]))

for i in range(num_outputs):
    expr = LinExpr()
    for j in range(num_neurons[-1]):
        expr.add(layerReluOuts[num_layers-1][j], weights[num_layers][i][j])
    #expr.addTerms(weights[num_layers][i], layerReluOuts[num_layers-1].values())
    expr.addConstant(biases[num_layers][i])
    nn.addConstr(outputs[i] == expr)

#for i in range(num_inputs):
#    nn.addConstr(absDeltas[i] == abs_(deltas[i]))


#TODO: Add code here that allows us to set values for inputs



for i in range(num_inputs):
    nn.addConstr(deltas[i] == 0)


nn.setParam('PoolSearchMode', 2)
nn.setParam('PoolSolutions', 2)
nn.write('task2.lp')
nn.optimize()

if nn.status == GRB.Status.OPTIMAL:
    print('SolCount: ' + str(nn.Params.SolCount))
    if nn.Params.SolCount != None:
        for i in range(nn.Params.SolCount):
            nn.Params.SolutionNumber = i
            for j in range(num_inputs):
                print('Input ' + str(j) + ': ' + str(inputs[j].Xn))

            for j in range(num_outputs):
                print('Output ' + str(j) + ': ' + str(outputs[j].Xn))
    else:
        for i in range(num_inputs):
            print('Input ' + str(i) + ': ' + str(inputs[i].X))

        for i in range(num_outputs):
            print('Output ' + str(i) + ': ' + str(outputs[i].X))

