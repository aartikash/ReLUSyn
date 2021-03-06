import csv


with open('aggregate_results_3A.csv', 'w') as out_f:
    for i in range(1, 202):
        with open('attacksynthesis_3A_input_{}.csv'.format(i), 'r') as results_f:
            successful_attacks = 0
            successful_input_deviations = []
            output_deviations = []
            times = [] 
            max_time_per_successful_attack = 0
            for j in range(2701):
                line_one = results_f.readline().split(',')
                if 'Y' in line_one:
                    successful_attacks += 1
                    times.append(float(line_one[-1][:-1]))
                    successful_input_deviations.append(float(line_one[1]))
                    output_deviations.append(float(line_one[2]))
                    for k in range(73):
                        line_one = results_f.readline().split(',')
                        successful_input_deviations.append(float(line_one[1]))
            out_f.write('input {}: successful attacks = {}, input deviations = {}, output change = {}, times = {}, max_time = {}\n'.format(i, successful_attacks, successful_input_deviations, output_deviations, times, max(times) if len(times) > 0 else 0))
