import csv
import math

DEADZONE = 0.078
ALPHA = 0.15  # smoothing

fx = 0.0
fy = 0.0

with open("mpu_normalized.txt") as infile, open("mpu_refined.txt", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    next(reader)
    writer.writerow(["time", "x_refined", "y_refined"])

    for t, x, y in reader:
        x = float(x)
        y = float(y)

        r = math.sqrt(x*x + y*y)

        if r < DEADZONE:
            x = 0.0
            y = 0.0
        else:
            scale = (r - DEADZONE) / (1.0 - DEADZONE)
            x = (x / r) * scale
            y = (y / r) * scale

        # smoothing
        fx += ALPHA * (x - fx)
        fy += ALPHA * (y - fy)

        writer.writerow([t, fx, fy])
