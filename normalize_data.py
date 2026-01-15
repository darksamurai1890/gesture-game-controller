import csv

# ---- CALIBRATION VALUES ----
PITCH_MIN = -27.33
PITCH_MAX =  50.73
ROLL_MIN  = -42.02
ROLL_MAX  =  29.44

def normalize(v, vmin, vmax):
    if v > 0:
        return v / vmax
    else:
        return v / abs(vmin)

with open("mpu_angle_log.txt") as infile, open("mpu_normalized.txt", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    next(reader)
    writer.writerow(["time", "x", "y"])

    for t, pitch, roll in reader:
        x = normalize(float(roll),  ROLL_MIN,  ROLL_MAX)
        y = normalize(float(pitch), PITCH_MIN, PITCH_MAX)

        writer.writerow([t, x, y])
