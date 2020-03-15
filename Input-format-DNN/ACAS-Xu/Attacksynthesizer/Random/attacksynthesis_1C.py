import csv
from attacksynthesis_1 import find_delta

outputs_to_change = [i for i in range(5)]
inputs_to_change = []
for i in range(5):
    for j in range(i+1, 5):
        for k in range(j+1, 5):
            inputs_to_change.append([i, j, k])

with open("attacksynthesis_1C.csv", 'w') as f:
    writer = csv.writer(f)
    for i in outputs_to_change:
        print('Choosing output ' + str(i))
        for j in inputs_to_change:
            print('Choosing inputs ' + str(j))
            output = find_delta(j, i, 5)
            writer.writerows(output)
