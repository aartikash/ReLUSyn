import csv
from attacksynthesis_7 import find_delta

inputs_to_change = [[0,1,2]]

with open("attacksynthesis_7C.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing input ' + str(i))
        output = find_delta(i)
        writer.writerows(output)
