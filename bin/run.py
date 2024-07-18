import subprocess
import time
import sys
from datetime import datetime
import RPi.GPIO as GPIO
from hx711 import HX711
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

def log_message(message):
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"[{log_time}] {message.lower()}")

# Initialize the HX711
hx = HX711(dout=DT_PIN, pd_sck=SCK_PIN, gain=128)

def clean_and_exit():
    log_message("Cleaning...")
    GPIO.cleanup()
    log_message("Bye!")
    sys.exit()

def zero_scale():
    log_message("Taring scale...")
    hx.tare()  # Tare the HX711
    log_message("Tare done!")

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

def convert_results_to_area_dict(boxes):
    area_dict = {}

    for i in range(len(boxes.xyxy)):
        cls = int(boxes.cls[i].item())
        xyxy = boxes.xyxy[i].detach().cpu().numpy()

        area = (xyxy[2] - xyxy[0]) * (xyxy[3] - xyxy[1])

        if cls in area_dict:
            area_dict[cls] += area
        else:
            area_dict[cls] = area

    return area_dict

def monitor_weight():
    prev_weight = hx.get_weight()
    time.sleep(1)

    while True:
        current_weight = hx.get_weight()
        weight_change = current_weight - prev_weight
        log_message(f"Waiting for weight change (now {prev_weight}) (change {weight_change})...")
        
        if abs(weight_change) > 1000:
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
            cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password)
            
            with cnxn:
                cursor = cnxn.cursor()

                results = convert_results_to_area_dict(results)

                total_area = sum(results.values())
                total_weight = weight_change
                
                raw_weights_dict = {}
                total_raw_weight = 0

                for cls in results:
                    cursor.execute(f"SELECT density FROM Food WHERE id = {cls}")
                    row = cursor.fetchone()
                    if row:
                        density = float(row[0])
                        area = results[cls]
                        height = 2
                        raw_weight = area * height * density
                        total_raw_weight += raw_weight
                        raw_weights_dict[cls] = raw_weight

                conversion_factor = total_weight / total_raw_weight if total_raw_weight else 0

                adjusted_weights_dict = {cls: weight * conversion_factor for cls, weight in raw_weights_dict.items()}

                log_message(f"results: {results}")
                log_message(f"weights: {adjusted_weights_dict}")

                with open(pics[1], 'rb') as file:
                    pic_bin = file.read()

                with open(pics[0], 'rb') as file:
                    pic_new = file.read()

                time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                    INSERT INTO Logs (time, bin_id, picture_of_bin, filtered_picture_of_new_food, dictionary_of_estimated_amts_of_food, change_in_weight)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (time_now, 0, pyodbc.Binary(pic_bin), pyodbc.Binary(pic_new), str(adjusted_weights_dict), weight_change))
                cnxn.commit()

        prev_weight = current_weight

        time.sleep(0)

zero_scale()
log_message("Starting weight monitoring...")

try:
    monitor_weight()
except (KeyboardInterrupt, SystemExit):
    clean_and_exit()

