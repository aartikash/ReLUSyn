import csv
from attacksynthesis_1 import find_delta

inputs_to_change = [[i for i in range(74)]]

for i in range(1, 202):
    with open("attacksynthesis_3A_input_{}.csv".format(i), 'w') as f:
        writer = csv.writer(f)
        for j in inputs_to_change:
            output = find_delta('../../../network_files/AP_predict.nt', '../../../network_files/input_{}.csv'.format(i), j, '../../../network_files/output_{}.csv'.format(i), 300)
            writer.writerows(output)
