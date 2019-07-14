import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# Main loop.

def get_values_solar(adc,GAIN):
    list_val = []
    while True:
        # Read all the ADC channel values in a list.
        values = [0]*4
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)
        # Print the ADC values.
        values[0]= values[0]*4.09/32767
        # Pause for half a second.
        time.sleep(0.5)
        list_val.append(values[0])
        if(len(list_val) >= 10):
            return list_val

def main():
    adc = Adafruit_ADS1x15.ADS1115(address=0x49, busnum=1)
    # Choose a gain of 1 for reading voltages from 0 to 4.09V.
    # Or pick a different gain to change the range of voltages that are read:
    #  - 2/3 = +/-6.144V
    #  -   1 = +/-4.096V
    #  -   2 = +/-2.048V
    #  -   4 = +/-1.024V
    #  -   8 = +/-0.512V
    #  -  16 = +/-0.256V
    # See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
    GAIN = 1 
    values = get_values_solar(adc,GAIN)
    print(values)
    return values 
    
if __name__ == "__main__":
    main() 
