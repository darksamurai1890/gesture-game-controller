import csv
import math
import matplotlib.pyplot as plt

xs, ys = [], []

with open("mpu_normalized.txt") as f:
    reader = csv.reader(f)
    next(reader)
    for _, x, y in reader:
        xs.append(float(x))
        ys.append(float(y))

plt.figure(figsize=(6,6))
plt.scatter(xs, ys, s=2)
plt.axhline(0)
plt.axvline(0)
plt.gca().set_aspect("equal", adjustable="box")
plt.title("Normalized MPU Output (Center Noise)")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()
