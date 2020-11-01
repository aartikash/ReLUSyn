import numpy as np
import sys

times = []
success = 0
fail = 0
total = 0

#f = open("attacksynthesis_1A.csv")
f = open("../network_files/input_1.csv")

#l1 = f.readline()
#l2 = f.readline()

#print(l1.strip().split(','))
#print(l2)

f = open("./attacksynthesis_3G.csv")
lines = [None] * 74

while True:
    lines[0] = f.readline()
    if not lines[0]:
        break
    lines[0] = lines[0].strip().split(',')

    for i in range(1, 74):
        lines[i] = f.readline()
        lines[i] = lines[i].strip().split(',')

    total += 1
    if lines[0][-2] == 'Y': 
        times.append(float(lines[0][-1]))
        success += 1
    elif contents1[-2] == 'N':
        fail += 1

print('Total: ' + str(total))
print('Successful: ' + str(success))
print('Fail: ' + str(fail))
if total != (success + fail):
    print('There was counting error when tallying number of failed and successful experiments')
    sys.exit(0)
else:
    print('Mean time: ' + str(np.mean(times)))
    print('Median time: ' + str(np.median(times)))
    print('Maximum time: ' + str(max(times)) if len(times) > 0 else 0)
