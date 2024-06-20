import subprocess
import time
from datetime import datetime

def take_picture():
    while True:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Construct the output file name
        filename = f"{timestamp}.jpg"
        
        # Construct the command with the -n flag
        command = ["rpicam-jpeg", "-o", filename, "--vflip", "-n"]
        
        # Run the command, suppressing the output
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        # Get the current time for the log message
        log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Print the log message
        print(f"[{log_time}] Picture taken and saved as {filename}")
        
        # Wait for 5 seconds before taking the next picture
        time.sleep(5)

if __name__ == "__main__":
    take_picture()

