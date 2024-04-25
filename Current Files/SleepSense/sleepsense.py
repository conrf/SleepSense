from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import seeed_dht
import math
from adc import ADC
import netifaces as ni

app = Flask(__name__)

""" Global variables """
# Boolean to control start and stop of sensor reading
scriptRunning = False
# Array to hold output for terminal in HTML
terminalOutput = []
# Dictionary to 
iconStatus = {}

# Preset preferred metrics based on research
user_preferences = {
        'temperature': 66.0,
        'humidity': 40.0,
        'noise_level': 35.0,
        'light_intensity': 800.0,
        'air_quality': 100.0
}


# Ports for sensors
soundPin = 2
lightPin = 0
airQualityPin = 6

# Function to get the private local IP address of Flask website
def get_local_ip_address():
    interfaces = ni.interfaces()
    for interface in interfaces:
        try:
            if interface != 'lo':
                addresses = ni.ifaddresses(interface)
                ip_address = addresses[ni.AF_INET][0]['addr']
                return ip_address
        except:
            pass
    return None

# Class for reading analog values from sensors
class AnalogSensor():

    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()

    @property
    def analogRead(self):
        value = self.adc.read(self.channel)
        return value

# Main algorithm for SleepSense
def run_script():
    global scriptRunning, terminalOutput
    # Clear terminal output
    terminalOutput =[]
    # Initialize sensors
    soundSensor = AnalogSensor(soundPin)
    lightSensor = AnalogSensor(lightPin)
    airSensor = AnalogSensor(airQualityPin)
    tempHumidSensor = seeed_dht.DHT("11", 12)
    
    # Get functions for each value
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
        return airSensor.analogRead
    
    # Function to compare the current values to the thresholds and set status
    def compare_values(current_values, user_preferences):
        status = {}
        if set(current_values.keys()) != set(user_preferences.keys()):
            return None
        
        thresholds = {
            'temperature': (user_preferences['temperature'] - 1, user_preferences['temperature'] + 2), # [65-68]
            'humidity': (user_preferences['humidity'] - 10, user_preferences['humidity'] + 10), # [30-50%]
            'noise_level': (0, user_preferences['noise_level']), # [< 35]
            'light_intensity': (user_preferences['light_intensity'], 1000), # [> 800]
            'air_quality': (0, user_preferences['air_quality']) # [< 100]
        }
        
        # Compare current values with user preferences and assign status
        for condition, value in current_values.items():
            if condition == 'light_intensity':
                if value < thresholds[condition][0]:
                    status[condition] = 'High'
                else:
                    status[condition] = 'Good'  
            elif condition == 'air_quality':
                if value < thresholds[condition][1]:
                    status[condition] = 'Good'
                else:
                    status[condition] = 'High Pollution'           
            else:
                if value < thresholds[condition][0]:
                    status[condition] = 'Low'
                elif value > thresholds[condition][1]:
                    status[condition] = 'High'
                else:
                    status[condition] = 'Good'
        
        return status
            
    # Function that calls the get functions for sensor reads, calls compare_values, then updates iconStatus and terminal output
    def analyze_environment():
        global iconStatus, user_preferences
        
        # Collect current environment conditions
        conditions = {
            'temperature': get_temperature(),
            'humidity': get_humidity(),
            'noise_level': get_noise_level(),
            'light_intensity': get_light_intensity(),
            'air_quality': get_air_quality()
        }
        
        # Get status for current conditions
        status = compare_values(conditions, user_preferences)
        iconStatus = status

        # Update terminal output with status and current values
        terminalOutput.extend([f"{condition.capitalize()}: {value} ({conditions[condition]})" for condition, value in status.items()])
        terminalOutput.extend(" ")

    # Analyze the environment every 2 seconds
    while scriptRunning:
        analyze_environment()
        time.sleep(2)
    

""" Flask Routes """
# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get terminal output
@app.route('/get_terminal_output')
def get_terminal_output():
    global terminalOutput
    return jsonify(terminalOutput)

# Route to start script
@app.route('/start_script', methods=['POST'])
def start_script():
    global scriptRunning
    if not scriptRunning:
        scriptRunning = True
        run_script()
    return redirect(url_for('index'))


# Route to stop script
@app.route('/stop_script', methods=['POST'])
def stop_script():
    global scriptRunning
    if scriptRunning:
        scriptRunning = False
    return redirect(url_for('index'))

# Route to render Update Preferences Page
@app.route('/update_page')
def render_update_page():
    global user_preferences
    # Pass current user preferences to update page
    return render_template('update_preferences.html', user_preferences=user_preferences)

# Route to update user preferences
@app.route('/update_preferences', methods=['POST'])
def update_preferences():
    # Update global user preferences from form submission
    user_preferences['temperature'] = float(request.form['temperature'])
    user_preferences['humidity'] = float(request.form['humidity'])
    user_preferences['noise_level'] = float(request.form['noise'])
    user_preferences['light_intensity'] = float(request.form['light'])
    user_preferences['air_quality'] = float(request.form['air'])
    
    return render_template('index.html')

# Route to update sensor icons based on status
@app.route('/update_sensor_icons', methods=['GET'])
def update_sensor_icons():
    global scriptRunning, iconStatus
    if not scriptRunning:
        return jsonify({})  # Return empty status if the script is not running

    return jsonify(iconStatus)
    

if __name__ == '__main__':
    local_ip_address = get_local_ip_address()
    # Only run the website if it gets the local IP Address
    if local_ip_address:
        print("Flask application running at:", local_ip_address)
        app.run(debug=True, host=local_ip_address)
    else:
        print("Failed to retrieve local IP address.")
