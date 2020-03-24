import csv
from attacksynthesis_3 import find_delta

inputs_to_change = [[0,1,2,3],[0,1,2,4],[0,1,3,4],[0,2,3,4],[1,2,3,4]]

with open("attacksynthesis_3D.csv", 'w') as f:
    writer = csv.writer(f)
    for i in inputs_to_change:
        print('Choosing inputs ' + str(i))
        output = find_delta(i)
        writer.writerows(output)
