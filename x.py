total = 0
positive = 0
with open('x') as f:
    lines = f.readlines()
    for line in lines:
        x = line.split()
        if len(x) == 5:
            if x[4] == 'MISS':
                continue
            total += 1
            if float(x[4]) > 0:
                positive += 1
        if len(x) == 6:
            if x[5] == 'MISS':
                continue
            total += 1
            if float(x[5]) > 0:
                positive += 1
print(total, positive, "%.2f%%" % (positive/total*100))