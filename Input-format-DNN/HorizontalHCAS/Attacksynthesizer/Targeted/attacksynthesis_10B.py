import csv
from attacksynthesis_10 import find_delta

inputs_to_change = [[0,1],[0,2],[1,2]]

with open("attacksynthesis_10B.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing input ' + str(i))
        output = find_delta(i)
        writer.writerows(output)
