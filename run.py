import subprocess
import time
from datetime import datetime
import RPi.GPIO as GPIO
from hx711 import HX711

# Initialize GPIO
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for the HX711
DT_PIN = 5
SCK_PIN = 6

# Initialize the HX711
hx = HX711(DT_PIN, SCK_PIN)

# Set the scale and offset (you may need to calibrate these values)
scale = 1
offset = 0

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{log_time}] {message}")

def clean_and_exit():
    log_message("Cleaning...")
    GPIO.cleanup()
    log_message("Bye!")
    sys.exit()

def get_weight():
    try:
        val = hx.get_weight(5)
        weight = (val - offset) / scale
        return weight
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

def take_picture():
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Construct the output file name
    filename = f"~/foodpod/{timestamp}.jpg"
    
    # Construct the command with the -n flag
    command = ["rpicam-jpeg", "-o", filename, "--vflip", "-n"]
    
    # Run the command, suppressing the output
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    
    # Log the picture taken message
    log_message(f"Picture taken and saved as {filename}")

def monitor_weight():
    prev_weight = get_weight()
    time.sleep(1)  # Initial delay to allow for any transient readings
    
    while True:
        current_weight = get_weight()
        
        # Check if there's a significant change in weight
        if abs(current_weight - prev_weight) > 0.01:  # Adjust the threshold as needed
            take_picture()
            prev_weight = current_weight
        
        # Wait for a short time before checking again
        time.sleep(1)

if __name__ == "__main__":
    hx.reset()  # reset the scale to zero
    log_message("reset done! Starting weight monitoring...")
    
    try:
        monitor_weight()
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

