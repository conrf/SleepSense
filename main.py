import random
import time
import seeed_dht
import math
from adc import ADC


# Placeholder Preferences
user_preferences = {
        'temperature': 68.0,
        'humidity': 50.0,
        'noise_level': 40.0,
        'light_intensity': 200.0,
        'air_quality': 50.0
}

soundPin = 2
lightPin = 0

class AnalogSensor():

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def analogRead(self):
        value = self.adc.read(self.channel)
        return value
    
def main():

    soundSensor = AnalogSensor(soundPin)
    lightSensor = AnalogSensor(lightPin)
    tempHumidSensor = seeed_dht.DHT("11", 12)
    
    def get_temperature():
        humi, temp = tempHumidSensor.read()
        temp_fahrenheit = (temp * 1.8) + 32
        return temp_fahrenheit
    
    def get_humidity():
        humi, temp = tempHumidSensor.read()
        return humi

    def get_noise_level():
        return {0}.format(soundSensor.analogRead)

    def get_light_intensity():
        return {0}.format(lightSensor.analogRead)

    def get_air_quality():
        return random.uniform(0.0, 150.0)  # Simulating air quality index

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
        #conditions_met = sum(1 for k in conditions if abs(conditions[k] - prefs[k]) <= 5)
        
        # Provide feedback
        # Display a picture to the LCD
        # Implement Different Pictures?
        # if conditions_met >= 4:
        #     print(":-) Conditions are optimal for sleep.")
        # elif conditions_met >= 2:
        #     print(":-| Conditions are moderate.")
        # else:
        #     print(":-( Conditions are suboptimal for sleep.")
        
        # For detailed conditions (simulating LCD output)
        print("Environmental Conditions:")
        for condition, value in conditions.items():
            print(f"{condition.capitalize()}: {value:.2f}")

    # Run the analysis periodically (example: every 5 seconds)

    while True:
        analyze_environment()
        time.sleep(2)

if __name__ == '__main__':
    main()
