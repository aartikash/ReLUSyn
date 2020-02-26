import csv
from attacksynthesis_4 import find_delta

inputs_to_change = []
for i in range(74):
    for j in range(i+1, 74):
        inputs_to_change.append([i, j])

with open("attacksynthesis_5F.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        output = find_delta('../network_files/AP_predict.nt', '../network_files/input_1.csv', i, 197, 200)
        writer.writerows(output)
