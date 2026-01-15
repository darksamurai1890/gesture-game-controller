import csv
import math
import statistics

radii = []

with open("mpu_normalized.txt") as f:
    reader = csv.reader(f)
    next(reader)
    for _, x, y in reader:
        r = math.sqrt(float(x)**2 + float(y)**2)
        radii.append(r)

mean_r = statistics.mean(radii)
std_r  = statistics.stdev(radii)

deadzone = mean_r + 3 * std_r

print("Deadzone analysis:")
print(f"Mean radius : {mean_r:.4f}")
print(f"Std dev     : {std_r:.4f}")
print(f"Deadzone    : {deadzone:.4f}")
