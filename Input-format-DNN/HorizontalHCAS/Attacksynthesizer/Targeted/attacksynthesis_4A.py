import csv
from attacksynthesis_4 import find_delta

inputs_to_change = [i for i in range(3)]

with open("attacksynthesis_4A.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing input ' + str(i))
        output = find_delta([i])
        writer.writerows(output)
