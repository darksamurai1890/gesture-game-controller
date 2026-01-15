import serial
import csv
import time

# ---- CONFIG ----
PORT = "COM12"      # change to your ESP32 port
BAUD = 115200
OUT_FILE = "mpu_angle_log.txt"
DURATION = 15       # seconds to record (None for infinite)

# ---- OPEN SERIAL ----
ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)  # wait for ESP32 reset

print("Logging started...")

start = time.time()

with open(OUT_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "pitch", "roll"])

    try:
        while True:
            if DURATION and (time.time() - start) > DURATION:
                break

            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:
                continue  # skip malformed lines

            writer.writerow(parts)
            print(line)

    except KeyboardInterrupt:
        print("\nStopped by user")

ser.close()
print("Saved to", OUT_FILE)
