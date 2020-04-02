import csv
from attacksynthesis_1 import find_delta

outputs_to_change = [i for i in range(5)]
inputs_to_change = [i for i in range(3)]

with open("attacksynthesis_1A.csv", 'w') as f:
    writer = csv.writer(f)
    for i in outputs_to_change:
        print('Choosing output ' + str(i))
        for j in inputs_to_change:
            print('Choosing input ' + str(j))
            output = find_delta([j], i, 5)
            writer.writerows(output)
