import csv
from attacksynthesis_4 import find_delta

inputs_to_change = [[0,1,2]]

with open("attacksynthesis_4C.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing inputs ' + str(i))
        output = find_delta(i)
        writer.writerows(output)
