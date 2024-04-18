import time
import math
import seeed_dht
from adc import ADC

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
    
    print('Entering analog reads')
    try:
        while True:
            humi, temp = tempHumidSensor.read()
            if not humi is None:
                temp_fahrenheit = (temp * 1.8) + 32
                print('DHT{0}, humidity {1:.1f}%, temperature {2:.1f}°F'.format(tempHumidSensor.dht_type, humi, temp_fahrenheit))
            else:
                print('DHT{0}, humidity & temperature: {1}°F'.format(tempHumidSensor.dht_type, (temp * 1.8) + 32))
            time.sleep(1)
            print('Sound value: {0}'.format(soundSensor.analogRead))
            time.sleep(.3)
            print('Light value: {0}'.format(lightSensor.analogRead))
            time.sleep(.8)
    except KeyboardInterrupt:
        print("Exiting Program")
    
if __name__ == '__main__':
    main()
