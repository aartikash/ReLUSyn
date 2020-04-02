import numpy as np
import sys

times = []
success = 0
fail = 0
total = 0

f = open("attacksynthesis_5G.csv")

#l1 = f.readline()
#l2 = f.readline()

#print(l1.strip().split(','))
#print(l2)

while True:
    line1 = f.readline()
    line2 = f.readline()
    if not line2:
        break
    total += 1
    contents = line1.strip().split(',')
    times.append(float(contents[-1]))
    if contents[-2] == 'Y':
        success += 1
    elif contents[-2] == 'N':
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
    print('Maximum time: ' + str(max(times)))
