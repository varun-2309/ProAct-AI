import time
import random
import pandas as pd
from datetime import datetime

def generate_sensor_data():
    """
    Simulates sensor readings with occasional failure events.
    """
    temperature = random.normalvariate(65, 2)
    vibration = random.normalvariate(0.5, 0.05)
    pressure = random.normalvariate(30, 1.5)
    rpm = random.normalvariate(1500, 50)

    # Inject rare failure event
    if random.random() > 0.95:
        temperature += random.uniform(15, 25)
        vibration += random.uniform(0.6, 1.2)
        pressure += random.uniform(5, 10)

    return {
        "timestamp": datetime.utcnow(),
        "temperature": round(temperature, 2),
        "vibration": round(vibration, 3),
        "pressure": round(pressure, 2),
        "rpm": int(rpm)
    }

if __name__ == "__main__":
    print("Starting sensor simulation... Press CTRL+C to stop.\n")
    try:
        while True:
            data = generate_sensor_data()
            df = pd.DataFrame([data])
            print(df)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")
