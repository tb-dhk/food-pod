import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the HX711
DT_PIN = 5
SCK_PIN = 6

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{log_time}] {message.lower()}")

# Initialize the HX711
hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN, gain=128)

def clean_and_exit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

def zero_scale():
    print("Taring scale...")
    hx.tare()  # Tare the HX711
    print("Tare done!")
    print(f"offset set to {hx.OFFSET}.")

def calibrate_scale():
    zero_scale()
    input("Place a known weight on the scale and press Enter.")
    known_weight = float(input("Enter the weight of the known object in grams: "))

    print("Reading the current value from HX711...")
    reading = hx.get_value()

    print(f"Current reading: {reading}")
    calibration_factor = reading / known_weight
    print(f"Calibration factor: {calibration_factor}")

    hx.set_scale(calibration_factor)
    print("Calibration factor set.")

    # Save the calibration factor to a file
    with open("calibration_factor.txt", "w") as f:
        f.write(str(calibration_factor))
    
    print("Calibration factor saved to 'calibration_factor.txt'.")
    print("Calibration completed.")

zero_scale()
print("Starting calibration process...")

try:
    calibrate_scale()
except (KeyboardInterrupt, SystemExit):
    clean_and_exit()
