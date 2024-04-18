import random
import time
import seeed_dht
import math
from adc import ADC


# Placeholder Preferences
user_preferences = {
        'temperature': 66.0,
        'humidity': 40.0,
        'noise_level': 30.0,
        'light_intensity': 400.0,
        'air_quality': 40.0
}

# Temperature (High/Low Bounds) should be 65-68F https://www.sleepfoundation.org/bedroom-environment/best-temperature-for-sleep
# Humidity (High/Low Bounds) between 30-50% https://www.sleepfoundation.org/bedroom-environment/humidity-and-sleep#:~:text=The%20best%20relative%20humidity%20for,60%25%20is%20a%20better%20range.
# Noise (High Bound) Level below <30dB https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5187651/
# Light (High Bound) intensity less than <100lux https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6814154/
# Air Quality (High Bound) less than <50 (0-500 AQi) https://www.unep.org/news-and-stories/story/how-air-quality-measured

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
        return soundSensor.analogRead

    def get_light_intensity():
        return lightSensor.analogRead

    def get_air_quality():
        return random.uniform(0.0, 150.0)  # Simulating air quality index

    # Simulated User Preferences - could retrieve from website? Web interface?
    def fetch_user_preferences():
        global user_preferences
        return user_preferences
    
    def compare_values(current_values, user_preferences):

        status = {}

        if set(current_values.keys()) != set(user_preferences.keys()):
            return None
        
        thresholds = {
            # (Low, High)
            'temperature': (user_preferences['temperature'] - 1, user_preferences['temperature'] + 2), # [GOOD]
            'humidity': (user_preferences['humidity'] - 10, user_preferences['humidity'] + 10), # [GOOD]
            'noise_level': (0, user_preferences['noise_level'] + 15),  # [GOOD]
            'light_intensity': (user_preferences['light_intensity'], 1000), # [GOOD]
            'air_quality': (0, user_preferences['air_quality'] + 10) # [GOOD]
        }
        
        # Compare current values with user preferences
        for condition, value in current_values.items():
            if condition == 'light_intensity':
                if value < thresholds[condition][0]:
                    status[condition] = 'H'
                else:
                    status[condition] = 'G'  
            elif condition == 'air_quality':
                if value < thresholds[condition][1]:
                    status[condition] = 'G'
                else:
                    status[condition] = 'H'           
            else:
                if value < thresholds[condition][0]:
                    status[condition] = 'L'
                elif value > thresholds[condition][1]:
                    status[condition] = 'H'
                else:
                    status[condition] = 'G'
        
        return status
            

    def analyze_environment():

        prefs = fetch_user_preferences()
        
        # Collect current environment conditions
        # TODO: Set a threshold if the conditions are outside of normal range, do something to indicate. Maybe set it to 1000. 
        conditions = {
            'temperature': get_temperature(),
            'humidity': get_humidity(),
            'noise_level': get_noise_level(),
            'light_intensity': get_light_intensity(),
            'air_quality': get_air_quality()
        }
        
        status = compare_values(conditions, prefs)

        print("Environmental Conditions:")
        for condition, value in status.items():
            print(f"{condition.capitalize()}: {value}")

    # Run the analysis periodically (example: every 5 seconds)

    while True:
        analyze_environment()
        time.sleep(2)

if __name__ == '__main__':
    main()
