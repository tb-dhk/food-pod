import subprocess
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
import cv2
import os
import numpy as np
from ultralytics import YOLO
import pyodbc
import dotenv

dotenv.load_dotenv(".env")

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for the HX711
DT_PIN = 5
SCK_PIN = 6

def createBoolList(size=8):
    return [False] * size

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = pd_sck
        self.DOUT = dout

        GPIO.setup(self.PD_SCK, GPIO.OUT)
        GPIO.setup(self.DOUT, GPIO.IN)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        self.set_gain(gain)

    def is_ready(self):
        return GPIO.input(self.DOUT) == 0

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        GPIO.output(self.PD_SCK, False)
        self.read()

    def read(self):
        while not self.is_ready():
            pass

        dataBits = [createBoolList(), createBoolList(), createBoolList()]

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                GPIO.output(self.PD_SCK, True)
                dataBits[j][i] = GPIO.input(self.DOUT)
                GPIO.output(self.PD_SCK, False)

        GPIO.output(self.PD_SCK, True)
        GPIO.output(self.PD_SCK, False)

        if all(item == True for item in dataBits[0]):
            return self.lastVal

        bits = []
        for i in range(2, -1, -1):
            bits += dataBits[i]

        self.lastVal = int(''.join(map(str, bits)), 2)
        return self.lastVal

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        GPIO.output(self.PD_SCK, False)
        GPIO.output(self.PD_SCK, True)

    def power_up(self):
        GPIO.output(self.PD_SCK, False)

# Initialize the HX711
hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN)

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\r[{log_time}] {message.lower()}")

def clean_and_exit():
    log_message("Cleaning...")
    GPIO.cleanup()
    log_message("Bye!\n")
    sys.exit()

def zero_scale():
    log_message("Taring scale...")
    hx.tare()  # Tare the HX711
    log_message("Tare done!\n")

def get_weight():
    try:
        weight = hx.get_units(5)
        return weight
    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

def take_picture():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"images/{timestamp}.jpg"
    command = ["libcamera-still", "-o", filename, "--vflip", "-n"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    log_message(f"Picture taken and saved as {filename}")
    log_message("Waiting for weight change...")

def get_latest_pictures(directory, num_pictures=2):
    files = sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg") and "-diff" not in f], key=os.path.getmtime, reverse=True)
    return files[:num_pictures]

def find_differences(image1, image2):
    diff = cv2.absdiff(image1, image2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    
    # Create an image to hold only the different pixels from image2
    diff_pixels = np.zeros_like(image2)
    diff_pixels[thresh != 0] = image2[thresh != 0]
    
    return diff_pixels

def detect_food(image_path):
    model_weights = "../model/models/food-detection/yolo_v8_v0.2.pt"
    model = YOLO(model_weights)
    results = model(image_path)
    results[0].save(filename=image_path.split(".")[0] + "-detected.jpg")
    return results[0].boxes

def convert_results_to_area_dict(results):
    area_dict = {}

    # Iterate over the range of boxes
    for i in range(len(results[0].boxes.xyxy)):
        cls = int(results[0].boxes.cls[i].item())  # Extract the class ID as an integer
        xyxy = results[0].boxes.xyxy[i].detach().cpu().numpy()  # Extract bounding box coordinates

        # Calculate area of the bounding box
        area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])

        # Accumulate the area for the corresponding class ID
        if cls in area_dict:
            area_dict[cls] += area
        else:
            area_dict[cls] = area

    return area_dict

def monitor_weight():
    prev_weight = get_weight()
    time.sleep(1)  # Initial delay to allow for any transient readings
    log_message("\nWaiting for weight change...")
    
    while True:
        log_message(f"\rWaiting for weight change (now {prev_weight/17145})...")
        current_weight = get_weight()
        
        if abs(current_weight - prev_weight) > 0.1:  # Adjust the threshold as needed
            weight_change = current_weight - prev_weight  # Calculate the change in weight
            
            pics = get_latest_pictures("images") 
            if len(pics) >= 2:
                log_message(f"Found {len(pics)} latest pictures.")
                image1 = cv2.imread(pics[1])
                image2 = cv2.imread(pics[0])
                
                log_message(f"Calculating difference mask between {pics[0]} and {pics[1]}...")
                diff_mask = find_differences(image1, image2)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                diff_filename = f"images/{timestamp}-diff.jpg"
                cv2.imwrite(diff_filename, diff_mask)
                
                log_message(f"Detecting food from differences image ({diff_filename})...")
                results = detect_food(diff_filename)
            else:
                log_message("Less than two pictures available, detecting food from new picture...")
                results = detect_food(cv2.imread(pics[0]))

            server = 'food-pod.database.windows.net'
            database = 'food-pod'
            username = 'foodpod'
            password = os.getenv("SQL_PASSWORD")
            driver = '{ODBC Driver 18 for SQL Server}'
            print(server, database, username, password, driver)
            cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
            
            with cnxn:
                cursor = cnxn.cursor()

                results = convert_results_to_area_dict(results)

                total_area = sum(results.values())
                total_weight = weight_change  # Assume this is the weight change in grams
                
                raw_weights_dict = {}
                total_raw_weight = 0

                for cls in results:
                    # Step 1: Query the Food table to find density of food given id
                    cursor.execute(f"SELECT density FROM Food WHERE id = {cls}")
                    row = cursor.fetchone()
                    if row:
                        density = float(row[0])
                        area = results[cls]
                        height = 2  # average height of food in cm
                        # Calculate the raw weight for this food item
                        raw_weight = area * height * density
                        raw_weights_dict[cls] = raw_weight
                        total_raw_weight += raw_weight
                    else:
                        raw_weights_dict[cls] = None  # Handle case where density is not found for the given class ID

                # Distribute the total weight change proportionally
                weights_dict = {cls: (raw_weights_dict[cls] / total_raw_weight) * total_weight if raw_weights_dict[cls] is not None else 0 for cls in raw_weights_dict}
                log_message(f"obtained results: {weights_dict}")
            
            prev_weight = current_weight
        
zero_scale() 
log_message("Starting weight monitoring...\n")

try:
    monitor_weight()
except (KeyboardInterrupt, SystemExit):
    clean_and_exit()
        
zero_scale() 
log_message("Starting weight monitoring...\n")

try:
    monitor_weight()
except (KeyboardInterrupt, SystemExit):
    clean_and_exit()

