import subprocess
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
from hx711 import HX711

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the HX711
DT_PIN = 5
SCK_PIN = 6

# Initialize the HX711
hx = HX711(dout_pin=DT_PIN, pd_sck_pin=SCK_PIN)

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\r[{log_time}] {message}", end="", flush=True)

def clean_and_exit():
    log_message("Cleaning...")
    GPIO.cleanup()
    log_message("Bye!\n")
    sys.exit()

def zero_scale():
    log_message("Taring scale...")
    hx.reset()  # Reset the HX711
    log_message("Tare done!\n")

def get_weight():
    try:
        measures = hx.get_raw_data(num_measures=5)
        average_measure = sum(measures) / len(measures)
        weight = average_measure  # Adjust as per your calibration
        return weight
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

def take_picture():
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct the output file name
    filename = f"/home/pi/foodpod/{timestamp}.jpg"
    
    # Construct the command with the -n flag
    command = ["raspistill", "-o", filename, "--vflip", "-n"]
    
    # Run the command, suppressing the output
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Log the picture taken message
    log_message(f"\nPicture taken and saved as {filename}\n")
    log_message("Waiting for weight change...")

def monitor_weight():
    prev_weight = get_weight()
    time.sleep(1)  # Initial delay to allow for any transient readings
    log_message("\nWaiting for weight change...")
    x = 0
    while True:
        log_message(f"\rWaiting for weight change ({x} times)...")
        current_weight = get_weight()
        
        # Check if there's a significant change in weight
        if abs(current_weight - prev_weight) > 0.01:  # Adjust the threshold as needed
            take_picture()
            prev_weight = current_weight
        
        # Wait for a short time before checking again
        time.sleep(1)
        x += 1

if __name__ == "__main__":
    zero_scale()  # Tare the scale to zero
    log_message("Starting weight monitoring...\n")
    
    try:
        monitor_weight()
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

