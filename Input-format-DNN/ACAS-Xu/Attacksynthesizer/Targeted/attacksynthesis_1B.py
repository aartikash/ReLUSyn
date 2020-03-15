import csv
from attacksynthesis_1 import find_delta

inputs_to_change = []
for i in range(5):
    for j in range(i+1, 5):
        inputs_to_change.append([i, j])

with open("attacksynthesis_1B.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing inputs ' + str(i))
        output = find_delta(i, 5)
        writer.writerows(output)
