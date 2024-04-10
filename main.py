import random
import time
import seeed_dht

def main():

    # for DHT11/DHT22
    sensor = seeed_dht.DHT("11", 12)
    # for DHT10
    # sensor = seeed_dht.DHT("10")
    
    while True:
        humi, temp = sensor.read()
        if not humi is None:
            print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}*'.format(sensor.dht_type, humi, temp))
        else:
            print('DHT{0}, humidity & temperature: {1}'.format(sensor.dht_type, temp))
        time.sleep(1)


if __name__ == '__main__':
    main()

    # Simulated sensor data collection functions
    def get_temperature():
        return random.uniform(18.0, 30.0)  # Simulating temperature in Celsius

    def get_humidity():
        return random.uniform(30.0, 70.0)  # Simulating humidity percentage

    def get_noise_level():
        return random.uniform(30.0, 80.0)  # Simulating noise level in dB

    def get_light_intensity():
        return random.uniform(100.0, 800.0)  # Simulating light intensity in lux

    def get_air_quality():
        return random.uniform(0.0, 150.0)  # Simulating air quality index

    # Placeholder for user preferences
    user_preferences = {
        'temperature': 24.0,
        'humidity': 50.0,
        'noise_level': 40.0,
        'light_intensity': 300.0,
        'air_quality': 50.0
    }

    # Simulated User Preferences - could retrieve from website? Web interface?
    def fetch_user_preferences():
        global user_preferences
        return user_preferences

    def analyze_environment():
        prefs = fetch_user_preferences()
        
        # Collect current environment conditions
        conditions = {
            'temperature': get_temperature(),
            'humidity': get_humidity(),
            'noise_level': get_noise_level(),
            'light_intensity': get_light_intensity(),
            'air_quality': get_air_quality()
        }
        
        # Simple analysis (placeholder for proprietary algorithm)
        conditions_met = sum(1 for k in conditions if abs(conditions[k] - prefs[k]) <= 5)
        
        # Provide feedback
        # Display a picture to the LCD
        # Implement Different Pictures?
        if conditions_met >= 4:
            print(":-) Conditions are optimal for sleep.")
        elif conditions_met >= 2:
            print(":-| Conditions are moderate.")
        else:
            print(":-( Conditions are suboptimal for sleep.")
        
        # For detailed conditions (simulating LCD output)
        print("Environmental Conditions:")
        for condition, value in conditions.items():
            print(f"{condition.capitalize()}: {value:.2f}")

    # Run the analysis periodically (example: every 5 seconds)
    while True:
        analyze_environment()
        time.sleep(2)