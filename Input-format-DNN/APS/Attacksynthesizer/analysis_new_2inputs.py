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

f = open("./attacksynthesis_2G.csv")
while True:
    line1 = f.readline()
    if not line1:
        break
    line2 = f.readline()
    total += 1
    contents1 = line1.strip().split(',')
    contents2 = line2.strip().split(',')
    if contents1[-2] == 'Y': 
        times.append(float(contents1[-1]))
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
