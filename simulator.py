#!/usr/bin/env python3
"""
IoT-230 Realtime Sensor Simulator
Sends simulated 7-sensor data to Firebase Realtime Database
matching ESPHome L5 architecture (PUT to /latest and POST to /history)
"""

import time
import random
import json
import urllib.request
import sys

# Force utf-8 stdout if available
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

DATABASE_URL = "https://iot-230-default-rtdb.asia-southeast1.firebasedatabase.app"
NODE_PATH = "/lab/esp32"
INTERVAL_SECONDS = 10

def generate_sensor_data():
    now = int(time.time())
    # 7 realistic agro-environmental sensor parameters:
    return {
        "temp": round(25.0 + random.uniform(0, 10.0), 1),        # 25.0 - 35.0 C
        "humi": round(50.0 + random.uniform(0, 30.0), 1),        # 50.0 - 80.0 %
        "soil": round(40.0 + random.uniform(0, 35.0), 1),        # 40.0 - 75.0 %
        "light": round(150.0 + random.uniform(0, 950.0), 0),     # 150 - 1100 lx
        "co2": round(400.0 + random.uniform(0, 500.0), 0),       # 400 - 900 ppm
        "pm25": round(12.0 + random.uniform(0, 45.0), 1),        # 12.0 - 57.0 ug/m3
        "water_level": round(45.0 + random.uniform(0, 50.0), 1), # 45.0 - 95.0 %
        "timestamp": now
    }

def send_request(url, method, payload):
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method=method
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.status, resp.read().decode("utf-8")

def main():
    print("=" * 65)
    print("  IoT-230 Firebase RTDB Sensor Simulator Started")
    print(f"  Target: {DATABASE_URL}{NODE_PATH}")
    print(f"  Interval: {INTERVAL_SECONDS} seconds | Columns: 7 sensors + timestamp")
    print("=" * 65)

    count = 0
    while True:
        count += 1
        data = generate_sensor_data()
        current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")

        print(f"\n[{current_time_str}] (Round #{count})")
        print(f"  Data: temp={data['temp']} C, humi={data['humi']}%, soil={data['soil']}%, "
              f"light={data['light']} lx, co2={data['co2']} ppm, pm25={data['pm25']} ug/m3, water={data['water_level']}%")

        # 1. PUT -> latest
        try:
            status, res = send_request(f"{DATABASE_URL}{NODE_PATH}/latest.json", "PUT", data)
            print(f"  [1] Latest PUT    -> HTTP {status} (Success)")
        except Exception as e:
            print(f"  [1] Latest PUT    -> Failed: {e}")

        # 2. POST -> history
        try:
            status, res = send_request(f"{DATABASE_URL}{NODE_PATH}/history.json", "POST", data)
            push_id = json.loads(res).get("name", "unknown") if status == 200 else "error"
            print(f"  [2] History POST  -> HTTP {status} (Key: {push_id})")
        except Exception as e:
            print(f"  [2] History POST  -> Failed: {e}")

        time.sleep(INTERVAL_SECONDS)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulator stopped by user.")
        sys.exit(0)
