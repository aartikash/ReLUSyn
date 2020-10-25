from gurobipy import *

def get_output_APS(input_values, in_file, out_file):
    f = open("../network_files/AP_predict.nt", "r")

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
    #deltas = nn.addVars(num_inputs)

    for i in range(74):
        nn.addConstr(inputs[i] == float(input_values[73-i]))

    layerOuts = {}
    layerReluOuts = {}

    expr = LinExpr()

    for i in range(num_layers):
        layerOuts[i] = nn.addVars(num_neurons[i], lb=-GRB.INFINITY)
        layerReluOuts[i] = nn.addVars(num_neurons[i])

    outputs = nn.addVars(num_outputs)

    for i in range(num_neurons[0]):
        expr = LinExpr()
        for j in range(num_inputs):
            expr.add(inputs[j], weights[0][i][j])
            #expr.add(deltas[j], weights[0][i][j])
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

    nn.optimize()

    with open('../network_files/{}'.format(in_file), 'w') as temp:
        for i in reversed(input_values):
            temp.write(i + '\n')

    with open('../network_files/{}'.format(out_file), 'w') as temp:
        temp.write(str(outputs[0].X))

f = open('/home/syed/data.csv', 'r')

for i in range(200):
    line = f.readline()
    line_vals = line.split(',')
    line_vals = line_vals[:-2]

    get_output_APS(line_vals, '../network_files/input_{}.csv'.format(i + 2), '../network_files/output_{}.csv'.format(i + 2))
